# Testing on Fast API with a dummy DB
The idea of this project it's to serve as an example in a talk about how to test in Fast API with a Dummy DB.

# Summary
- [Up & Running](#up-and-running)
- [Test commands](#test-commands)
- [Implementation theory](/docs/tests.md)
- [How do I organize the work](#how-do-i-organize-the-work)

## Up and running
Environment variable | Example value          | Required | Default
--- |------------------------|----------| --- 
DATABASE_USER  | "root" | NO       | 
DATABASE_PASSWORD  | ""  | NO       | 
DATABASE_HOST  | "mysql"  | NO       |
DATABASE_PORT  | "3306"  | NO       |
DATABASE_NAME  | "dummy-db"  | NO       |
TEST_DATABASE_HOST  | "mysql-test"  | NO       |
TEST_DATABASE_NAME  | "dummy-db-test"  | NO       |

```bash
$ make build
$ make run
```

## Test commands
```bash
$ make test
$ make debug test_dir={tests/tests_folder/test_file}
```

## Migrations commands
```bash
$ make create-migration desc={description_with_underscore_separation}
$ make apply-migrations
$ make downgrade-migrations identifier={migration_identifier_int}
```

## How do I organize the work
Number | Description 
--- | --- 
[#1](https://github.com/galloramiro/fastapi-testing-with-dummy-db/issues/1) | Create project and environment
[#2](https://github.com/galloramiro/fastapi-testing-with-dummy-db/issues/2) | Configured database
[#3](https://github.com/galloramiro/fastapi-testing-with-dummy-db/issues/3) | Create Session Interface
[#4](https://github.com/galloramiro/fastapi-testing-with-dummy-db/issues/4) | Create Crop Model
[#5](https://github.com/galloramiro/fastapi-testing-with-dummy-db/issues/5) | Create Crop Repository
[#6](https://github.com/galloramiro/fastapi-testing-with-dummy-db/issues/6) | Create Crop Endpoint