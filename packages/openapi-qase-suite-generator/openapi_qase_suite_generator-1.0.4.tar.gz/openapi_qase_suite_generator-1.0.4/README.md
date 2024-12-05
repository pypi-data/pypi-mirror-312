# openapi-qase-suite-generator

This script generates a Qase suite from an OpenAPI spec YAML file.
This is useful for keeping the consistency between the API and the test cases. In my company we use Qase for API testing.
For every Operation (Endpoint + Method) we create a new Qase suite. Every suite contains testcases for the given operation,
whether it is Unit Test or API Test, manual or automated.
Consistency naming for the test cases and the Operations is a good practice for maintenance.

For example, the following OpenAPI spec contains 3 operations:
```
paths:
  /api/v1/users:
    get:
      operationId: ApiV1UsersGet
      description: Get all available users
    post:
      operationId: ApiV1UsersPost
      description: Create a new user
  /api/v1/users/{id}:
    get:
      operationId: ApiV1UsersIdGet
      description: Get a user by ID
```

This script will generate 3 suites:
- Suite: ApiV1UsersGet under directory "api", "v1", "users"
- Suite: ApiV1UsersPost under directory "api", "v1", "users"
- Suite: ApiV1UsersIdGet under directory "api", "v1", "users", "{id}"

The tester can add test cases to the generated suites.
The script will generate a new Qase suite only if it does not exist yet.

Usage:
```
  openapi_qase_suite_generator \
    --api-definition <path-to-openapi-spec> \
    --qase-api-token <qase-api-token> \
    --qase-project-id <qase-project-id> \
    --qase-root-suite-id <qase-root-suite-id>
```
Where:
- <path-to-openapi-spec> is the path to the OpenAPI spec YAML file
- <qase-api-token> is the Qase API token
- <qase-project-id> is the Qase project ID
- <qase-root-suite-id> is the Qase root suite ID
