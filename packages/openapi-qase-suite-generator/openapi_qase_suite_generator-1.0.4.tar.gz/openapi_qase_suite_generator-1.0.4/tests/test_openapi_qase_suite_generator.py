# pylint: disable=missing-module-docstring

import pytest
from unittest import TestCase, mock

from openapi_qase_suite_generator import \
    Config, \
    QASE_BASE_URL, \
    parse_args, \
    create_qase_suite, \
    get_all_suites, \
    insert_into_api_tree, \
    load_tree_from_openapi_struct, \
    build_qase_suite_tree, \
    sync_api_tree_with_qase_tree, \
    ApiTreeNode, \
    QaseSuite, \
    QaseSuiteTreeNode


class TestParseArgs(TestCase):
    def test_parse_args(self):
        args = [
            "--api-definition", "openapi_file",
            "--qase-api-token", "qase_api_token",
            "--qase-project-id", "qase_project_id",
            "--qase-root-suite-id", "1"
        ]
        config = parse_args(args)
        self.assertEqual(config.file, "openapi_file")
        self.assertEqual(config.qase_api_token, "qase_api_token")
        self.assertEqual(config.qase_project_id, "qase_project_id")
        self.assertEqual(config.qase_root_suite_id, 1)


class MockResponse:
    def __init__(self, json_data, status_code):
        self.json_data = json_data
        self.status_code = status_code

    def json(self):
        return self.json_data


def mocked_requests_post_create_suite(*args, **kwargs) -> MockResponse:
    return MockResponse(json_data={
        "result": {
            "id": 1
        }
    }, status_code=200)


def mocked_requests_get_all_suites(*args, **kwargs) -> MockResponse:
    return MockResponse(json_data={
        "result": {
            "total": 1,
            "entities": [
                {
                    "id": 1,
                    "parent_id": 0,
                    "title": "test",
                    "description": "test123"
                }
            ]
        }
    }, status_code=200)


class TestOpenApiTree(TestCase):

    def test_insert_into_api_tree(self):
        root = ApiTreeNode("path", "API")
        node = ApiTreeNode("operation", "Operation")
        insert_into_api_tree(root, ["path1", "path2"], node)
        self.assertEqual(len(root.children), 1)
        self.assertEqual(root.children[0].type, "path")
        self.assertEqual(root.children[0].path, "path1")
        self.assertEqual(len(root.children[0].children), 1)
        child1 = root.children[0].children[0]
        self.assertEqual(child1.type, "path")
        self.assertEqual(child1.path, "path2")
        self.assertEqual(len(child1.children), 1)
        child2 = child1.children[0]
        self.assertEqual(child2.type, "operation")
        self.assertEqual(child2.path, "Operation")

    def test_load_tree_from_openapi_struct(self):
        openapi_struct = {
            "paths": {
                "/path1/path2": {
                    "get": {
                        "operationId": "operation1"
                    },
                    "post": {
                        "operationId": "operation2"
                    }
                },
                "/path3/path4": {
                    "get": {
                        "operationId": "operation3"
                    }
                }
            }
        }
        tree = load_tree_from_openapi_struct(openapi_struct)
        self.assertEqual(len(tree.children), 2)
        child1 = tree.children[0]
        self.assertEqual(child1.type, "path")
        self.assertEqual(child1.path, "path1")
        self.assertEqual(len(child1.children), 1)


class TestQaseSuite(TestCase):
    @mock.patch("requests.post", side_effect=mocked_requests_post_create_suite)
    def test_create_qase_suite(self, mock_requests_post):
        config = Config(
            file="openapi_file",
            qase_api_token="qase_api_token",
            qase_project_id="qase_project_id",
            qase_root_suite_id=1
        )
        create_qase_suite(
            config,
            1,
            "test",
            "test123"
        )
        self.assertIn(
            mock.call(
                f"{QASE_BASE_URL}/suite/{config.qase_project_id}",
                headers={
                    "Token": config.qase_api_token
                },
                json={
                    "title": "test",
                    "parent_id": 1,
                    "description": "test123"
                }
            ),
            mock_requests_post.call_args_list
        )

    @mock.patch("requests.get", side_effect=mocked_requests_get_all_suites)
    def test_get_all_suites(self, mock_requests_get):
        config = Config(
            file="openapi_file",
            qase_api_token="qase_api_token",
            qase_project_id="qase_project_id",
            qase_root_suite_id=1
        )
        suites = get_all_suites(config)
        self.assertEqual(len(suites), 1)
        expected_url = (
            f"{QASE_BASE_URL}" +
            "/suite/" +
            f"{config.qase_project_id}?" +
            "limit=100&offset=0"
        )
        self.assertIn(
            mock.call(
                expected_url,
                headers={
                    "Token": config.qase_api_token
                }
            ),
            mock_requests_get.call_args_list
        )

    def test_build_qase_suite_tree(self):
        suite_id = 1
        suites = {
            1: QaseSuite(1, "test", 0, "test123"),
            2: QaseSuite(2, "test2", 1, "test1232"),
            3: QaseSuite(3, "test3", 1, "test1233"),
            4: QaseSuite(4, "test4", 1, "test1234"),
            5: QaseSuite(5, "test5", 1, "test1235"),
            6: QaseSuite(6, "test6", 2, "test1236"),
            7: QaseSuite(7, "test7", 2, "test1237"),
            8: QaseSuite(8, "test8", 3, "test1238"),
            9: QaseSuite(9, "test9", 3, "test1239"),
            10: QaseSuite(10, "test10", 3, "test12310")
        }
        tree = build_qase_suite_tree(
            suite_id,
            suites
        )
        self.assertEqual(len(tree.children), 4)
        child1 = tree.children[0]
        self.assertEqual(child1.suite.title, "test2")
        self.assertEqual(child1.suite, suites[2])
        self.assertEqual(len(child1.children), 2)

        child2 = tree.children[1]
        self.assertEqual(child2.suite.title, "test3")
        self.assertEqual(child2.suite, suites[3])
        self.assertEqual(len(child2.children), 3)


class TestSyncSuites(TestCase):

    @mock.patch("requests.post", side_effect=mocked_requests_post_create_suite)
    def test_sync_api_tree_with_qase_tree(self, mock_requests_post):
        config = Config(
            file="openapi_file",
            qase_api_token="qase_api_token",
            qase_project_id="qase_project_id",
            qase_root_suite_id=1
        )
        api_tree = ApiTreeNode()
        api_tree_child1 = ApiTreeNode("path", "path1")
        api_tree_child2 = ApiTreeNode("path", "path2")
        api_tree_child3 = ApiTreeNode("path", "test4")
        api_tree.children = [
            api_tree_child1,
            api_tree_child2,
            api_tree_child3
        ]
        api_tree_child3.children = [
            ApiTreeNode("operation", "test3")
        ]

        qase_tree = QaseSuiteTreeNode(QaseSuite(1, "test", 0, "test123"))
        qase_tree.children = [
            QaseSuiteTreeNode(QaseSuite(2, "test2", 1, "test1232")),
            QaseSuiteTreeNode(QaseSuite(3, "test3", 1, "test1233")),
            QaseSuiteTreeNode(QaseSuite(4, "test2", 1, "test1233")),
            QaseSuiteTreeNode(QaseSuite(6, "test4", 1, "test1233")),
            QaseSuiteTreeNode(QaseSuite(5, "test4", 1, "test1233"))
        ]
        sync_api_tree_with_qase_tree(
            config,
            api_tree,
            qase_tree,
            0
        )
