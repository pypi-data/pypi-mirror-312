# coding: utf-8
#
# This script generates a Qase suite from an OpenAPI spec YAML file.
# This is useful for keeping the consistency between the API and the test
# cases. In my company we use Qase for API testing.
# For every Operation (Endpoint + Method) we create a new Qase suite.
# Every suite contains testcases for the given operation, whether it is
# Unit Test or API Test, manual or automated.
# Consistency naming for the test cases and the Operations is a good practice
# for maintenance.
#
# For example, the following OpenAPI spec contains 3 operations:
# ```
# paths:
#   /api/v1/users:
#     get:
#       operationId: ApiV1UsersGet
#       description: Get all available users
#     post:
#       operationId: ApiV1UsersPost
#       description: Create a new user
#   /api/v1/users/{id}:
#     get:
#       operationId: ApiV1UsersIdGet
#       description: Get a user by ID
# ```
#
# This script will generate 3 suites:
# - Suite: ApiV1UsersGet under directory "api", "v1", "users"
# - Suite: ApiV1UsersPost under directory "api", "v1", "users"
# - Suite: ApiV1UsersIdGet under directory "api", "v1", "users", "{id}"
#
# The tester can add test cases to the generated suites.
# The script will generate a new Qase suite only if it does not exist yet.
#
# Usage:
# ```
#   ./generate_qase_suites.py \
#     --api-definition <path-to-openapi-spec> \
#     --qase-api-token <qase-api-token> \
#     --qase-project-id <qase-project-id> \
#     --qase-root-suite-id <qase-root-suite-id>
# ```
# Where:
# - <path-to-openapi-spec> is the path to the OpenAPI spec YAML file
# - <qase-api-token> is the Qase API token
# - <qase-project-id> is the Qase project ID
# - <qase-root-suite-id> is the Qase root suite ID

import sys
import requests
import argparse
import yaml
import os

###############################################################################
# CONFIG
###############################################################################


class Config:
    """
    Configuration for the script
    """
    file: str
    qase_api_token: str
    qase_project_id: str
    qase_root_suite_id: int

    def __init__(
            self,
            file: str,
            qase_api_token: str,
            qase_project_id: str,
            qase_root_suite_id: int
    ):
        self.file = file
        self.qase_api_token = qase_api_token
        self.qase_project_id = qase_project_id
        self.qase_root_suite_id = qase_root_suite_id


def get_version() -> str:
    """Get version from git or version file"""
    from .__version import __version__
    version = __version__
    name = "openapi_qase_suite_generator"
    return f"{name} {version}"


def parse_args(args: list[str]) -> Config:
    """
    Parse the command line arguments
    """
    parser = argparse.ArgumentParser(
        description="Generate a Qase suite from an OpenAPI spec"
    )

    parser.add_argument(
        "--version",
        action="version",
        version=get_version()
    )

    parser.add_argument(
        "--api-definition",
        type=str,
        required=True,
        help="Path to the API definition file."
    )
    parser.add_argument(
        "--qase-api-token",
        type=str,
        required=True,
        help="Qase API token."
    )
    parser.add_argument(
        "--qase-project-id",
        type=str,
        required=True,
        help="Qase project ID."
    )
    parser.add_argument(
        "--qase-root-suite-id",
        type=str,
        required=True,
        help="Qase root suite ID."
    )
    args = parser.parse_args(args)

    return Config(
        file=args.api_definition,
        qase_api_token=args.qase_api_token,
        qase_project_id=args.qase_project_id,
        qase_root_suite_id=int(args.qase_root_suite_id)
    )

###############################################################################
# API TREE NODE
###############################################################################


class ApiTreeNode:
    """
    A tree node for the API YAML file.

    We will use it to compare the OpenAPI spec with the Qase suites.
    The tree will look like this:
    api
    ├─ v1
    │  ├─ users
    │  │  ├─ {id}
    │  │  │  ├─ ApiV1UsersIdGet
    │  │  │  └─ ApiV1UsersIdPost
    """
    type: str
    path: str
    description: str
    children: list["ApiTreeNode"]

    def __init__(
            self,
            type: str = "path",
            path: str = None,
            description: str = None
    ):
        self.type = type
        self.path = path
        self.description = description
        self.children = []


def insert_into_api_tree(
        root: ApiTreeNode,
        paths: list[str],
        node: ApiTreeNode
        ):
    """
    Insert a new node into the API tree.
    """
    current_node = root
    for path in paths:
        found = False
        for child in current_node.children:
            if child.path == path:
                current_node = child
                found = True
                break
        if not found:
            new_node = ApiTreeNode("path", path, None)
            current_node.children.append(new_node)
            current_node = new_node
    current_node.children.append(node)


def debug_api_tree(root: ApiTreeNode, level: int = 0):
    """
    Debug the API tree
    """
    for child in root.children:
        print("  " * level + child.path)
        debug_api_tree(child, level + 1)


def load_tree_from_openapi_file(file_path: str) -> ApiTreeNode:
    """
    Load the API tree from the OpenAPI file
    """
    with open(file_path, "r") as file:
        api_definition = yaml.safe_load(file)

    return load_tree_from_openapi_struct(api_definition)


def load_tree_from_openapi_struct(api_definition: any) -> ApiTreeNode:
    """
    Load the API tree from the OpenAPI structure
    """
    paths = api_definition["paths"]
    if not paths:
        raise ValueError("No paths found in the API definition.")

    root = ApiTreeNode()
    for path, methods in paths.items():
        for method, operation in methods.items():
            operation_id = operation.get("operationId")
            if not operation_id:
                raise ValueError(f"Operation ID not found for {path} {method}")
            operation_paths = path.split("/")[1:]  # Skip first `/`
            description = f"URL: {path} {method.upper()}" + \
                f"\nOperationId: {operation_id}"
            node = ApiTreeNode("operation", operation_id, description)
            insert_into_api_tree(root, operation_paths, node)

    return root


###############################################################################
# QASE
###############################################################################


QASE_BASE_URL = "https://api.qase.io/v1"


class QaseSuite:
    """
    A Qase suite
    """
    id: int
    title: str
    parent_id: int
    description: str

    def __init__(self, id: int, title: str, parent_id: int, description: str):
        self.id = id
        self.title = title
        self.parent_id = parent_id
        self.description = description


class QaseSuiteTreeNode:
    """
    A Qase suite tree node
    """
    suite: QaseSuite
    children: list["QaseSuiteTreeNode"]

    def __init__(self, suite: QaseSuite):
        self.suite = suite
        self.children = []


class QaseSuiteException(Exception):
    """
    A Qase suite exception
    """
    def __init__(self, message: str):
        super().__init__(message)


def get_all_suites(config: Config) -> dict[int, QaseSuite]:
    """
    Get all suites from Qase.

    Since Qase does not provide a way to get children suites, we need to fetch
    all suites to build the tree of suites.
    Will return map of suites indexed by id.
    """
    end = False
    offset = 0
    limit = 100
    project_id = config.qase_project_id
    suites = {}
    while not end:
        url = f"{QASE_BASE_URL}/suite/{project_id}?limit=100&offset={offset}"
        response = requests.get(url, headers={"Token": config.qase_api_token})
        if response.status_code != 200:
            raise QaseSuiteException(
                f"Failed to get suites: {response.status_code} {response.text}"
            )
        data = response.json()
        data_result = data["result"]
        if offset + limit > data_result["total"]:
            end = True
        for suite in data_result["entities"]:
            suite_id = int(suite["id"])
            suites[suite_id] = QaseSuite(
                suite_id,
                suite["title"],
                suite["parent_id"],
                suite["description"]
            )
        offset += limit
    # sort by id to have a stable order
    # suites = dict(sorted(suites.items(), key=lambda x: x[0]))

    return suites


def debug_qase_suites(suites: dict[int, QaseSuite]):
    """
    Debug the Qase suites
    """
    for suite in suites.values():
        print(suite.id, suite.title, suite.parent_id, suite.description)


def build_qase_suite_tree(
        root_suite_id: int,
        suites: dict[int, QaseSuite]
        ) -> QaseSuiteTreeNode:
    """
    Build the Qase suite tree
    """
    root_suite = suites[root_suite_id]
    root_node = QaseSuiteTreeNode(root_suite)
    for suite in suites.values():
        print(root_suite_id, suite.id, suite.title, suite.parent_id)
        if suite.parent_id == root_suite_id:
            print(f"Appending {suite.title} to {root_suite.title}")
            node = build_qase_suite_tree(suite.id, suites)
            root_node.children.append(node)
    return root_node


def debug_qase_suite_tree(
        root: QaseSuiteTreeNode,
        level: int = 0
        ):
    """
    Debug the Qase suite tree
    """
    print("  " * level + root.suite.title)
    for child in root.children:
        debug_qase_suite_tree(child, level + 1)


###############################################################################
# API TREE & QASE TREE COMPARISON
###############################################################################

def sync_api_tree_with_qase_tree(
        config: Config,
        api_tree: ApiTreeNode,
        qase_tree: QaseSuiteTreeNode,
        level: int = 0
        ):
    """
    Compare the API tree with the Qase tree.

    This will create missing suites in Qase and compare the API tree with the
    Qase tree recursively.
    """
    api_tree_children = api_tree.children
    api_tree_children.sort(key=lambda x: x.path)
    qase_tree_children = qase_tree.children
    # sort by title and id to have a stable order rather than random
    qase_tree_children.sort(key=lambda x: (x.suite.title, x.suite.id))
    # qase_tree_children.sort(key=lambda x: x.suite.id)

    for api_tree_child in api_tree_children:
        found = False
        for qase_tree_child in qase_tree_children:
            if api_tree_child.path == qase_tree_child.suite.title:
                found = True
                print("  " * level +
                      f"Suite {api_tree_child.path} found in Qase"
                      )
                sync_api_tree_with_qase_tree(
                    config,
                    api_tree_child,
                    qase_tree_child,
                    level + 1
                )
                break
        if not found:
            print("  " * level +
                  f"Suite {api_tree_child.path} not found in Qase. Creating..."
                  )
            parent_id = qase_tree.suite.id
            new_suite = create_qase_suite(
                config,
                parent_id,
                api_tree_child.path,
                api_tree_child.description
            )
            new_suite_tree_node = QaseSuiteTreeNode(new_suite)
            print("  " * level + f"Suite {new_suite.title} created in Qase")
            sync_api_tree_with_qase_tree(
                config,
                api_tree_child,
                new_suite_tree_node,
                level + 1
            )


def create_qase_suite(
        config: Config,
        parent_id: int,
        title: str,
        description: str
        ) -> QaseSuite:
    """
    Create a new Qase suite
    """
    url = f"{QASE_BASE_URL}/suite/{config.qase_project_id}"
    response = requests.post(
        url,
        headers={"Token": config.qase_api_token},
        json={
            "title": title,
            "parent_id": parent_id,
            "description": description
        }
    )
    if response.status_code != 200:
        raise QaseSuiteException(
            f"Failed to create suite: {response.status_code} {response.text}"
        )
    data = response.json()
    data_result = data["result"]
    suite_id = int(data_result["id"])
    return QaseSuite(suite_id, title, parent_id, title)

###############################################################################
# MAIN
###############################################################################


def main():
    args = sys.argv[1:]
    config = parse_args(args)
    print(f"Loading API tree from {config.file}...")
    api_tree = load_tree_from_openapi_file(config.file)
    debug_api_tree(api_tree)
    print("Getting all Qase suites...")
    suites = get_all_suites(config)
    debug_qase_suites(suites)
    print("Building Qase suite tree...")
    qase_tree = build_qase_suite_tree(
        config.qase_root_suite_id,
        suites
    )
    debug_qase_suite_tree(qase_tree)
    print("Syncing API tree with Qase tree...")
    sync_api_tree_with_qase_tree(config, api_tree, qase_tree)


if __name__ == "__main__":
    main()
