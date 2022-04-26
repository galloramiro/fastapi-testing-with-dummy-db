# Testing on Fast API with a dummy DB
The idea of this project it's to serve as an example in a talk about how to test in Fast API with a Dummy DB.

# Summary
- [Up & Running](#up-and-running)
- [Implementation theory](/docs/tests.md)
- [How do I organize the work](#how-do-i-organize-the-work)

## Up and running
Environment variable | Example value          | Required | Default
--- |------------------------| --- | --- 
DATABASE_URL  | "sqlite:///./local.db" | YES | 
TESTING_DATABASE_URL  | "sqlite:///./test.db"  | YES | 
```bash
$ pipenv install --dev
$ pipenv shell
$ uvicorn src.main:app --reload
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