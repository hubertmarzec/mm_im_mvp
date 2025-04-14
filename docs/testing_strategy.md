# Chapter 1: Testing Levels

| **Level**         | **Purpose**                                                                                                                                                                              | **Scope**                                                                                                                                                                                                                    | **Tools**                                                                                                                |
|-------------------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|--------------------------------------------------------------------------------------------------------------------------|
| **Unit Tests**    | Validate the functionality of individual units of code in isolation (e.g., single functions, classes).                                                                                  | - Pure business logic (e.g., calculations, data transformations)  <br/>- Helper/utility functions  <br/>- Pydantic model validation                                                                                          | - [pytest](https://docs.pytest.org/en/stable/) for test discovery and execution  <br/>- Mocking ([unittest.mock](https://docs.python.org/3/library/unittest.mock.html), [pytest-mock](https://pypi.org/project/pytest-mock/))  |
| **Functional Tests** | Test application features from the user perspective, ensuring each feature works correctly (often via HTTP endpoints), typically with external dependencies mocked or stubbed.         | - Black-box testing of key features  <br/>- Validating endpoints with external calls mocked  <br/>- Checking user stories (e.g., “Create a new user and retrieve their data”)                                               | - [fastapi.testclient](https://fastapi.tiangolo.com/advanced/testing/) to send requests to your FastAPI app  <br/>- Mocking/stubbing external calls                                            |
| **Integration Tests** | Confirm that different parts of the system (database, external services, internal modules) work together seamlessly.                                                                 | - Database queries and ORM usage (e.g., SQLAlchemy)  <br/>- Real or containerized external services  <br/>- Authentication/authorization flows with real or mock external identity providers                                  | - [fastapi.testclient](https://fastapi.tiangolo.com/advanced/testing/) for HTTP testing  <br/>- Docker/Testcontainers to spin up ephemeral DB or external services                              |
| **End-to-End Tests**  | Validate the entire application flow in a production-like environment (e.g., real DB, real external services), covering full user journeys.                                           | - Comprehensive user journeys (e.g., user registration → login → perform actions)  <br/>- Performance, load, or concurrency testing if required                                                                             | - [pytest](https://docs.pytest.org/) or external tools (e.g., [Postman/Newman](https://learning.postman.com/docs/running-collections/using-newman-cli/), [Locust](https://locust.io/))  <br/>- Staging/pre-production environment |

---

# Chapter 2: Test Organization

**Folder Structure**:

```plaintext
.
├── app
│   ├── main.py
│   ├── routers
│   ├── models
│   └── ...
└── tests
    ├── unit
    │   └── ...
    ├── functional
    │   └── ....
    ├── integration
    │   └── ...
    └── e2e
        └── ...
```

## 2.1 Naming Conventions
- Each test file starts with test_ (e.g., test_module_a.py).
- Use pytest-describe (pytest plugin) for pytest that allows tests to be written in arbitrary nested describe-blocks, similar to RSpec (Ruby) and Jasmine (JavaScript).
- Name test methods that describe, in a human-readable form, and follow the “test as documentation” approach, e.g. will_return_error_with_missing_request_id.

## 2.2 Use of conftest.py
- Define fixtures (e.g., FastAPI TestClient, database session, mock dependencies) that can be shared across multiple tests.
- Place conftest.py in the tests/ directory (or in a specific test subfolder) to scope the fixtures accordingly.