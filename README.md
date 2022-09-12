# Testing on Fast API with a dummy DB
The idea of this project it's to serve as an example in a talk about how to test in Fast API with a Dummy DB.

# Summary
- [Set up the environment](#set-up-the-environment)
- [Test commands](#test-commands)
- [Implementation theory](/docs/implementation_theory.md)
- [How do I organize the work](#how-do-i-organize-the-work)

## Set up the environment
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
In order allow the reproducibility in any environment and testing with an exact replica of the DB that we are going to use on production we combine three key things:
- 1 `Dockerfile`
- 2 different `docker-compose.yaml`
- 1 `Makefile`

The `Dockerfile` is the one that contains the main environment, holds the Python version, installs Poetry and the dependencies, and finally copy all the files that we need in order to make the project works.
The `docker-compose.yaml` has the maps the volumes, declare som environment variables and create the database that we are going to use locally.
The `docker-compose-test.yaml` create a new database located on a different port, with a different host, user, and db name that allow us to avoid problems on the jenkins run and on the local test runs. This is the setup that we are going to use fo run all the tests.
Finally, the `Makefile` allow us to avoid run complex and endless commands to use this setup.

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