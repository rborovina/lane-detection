# Lane-Detection

## Makefile commands
1. `make install` - installs a project with dependecies
2. `make install-test` - installs dev version with dependecies to validation and test
3. `make run-test`- Runs all tests from `tests`
4. `make validate` - Runs `mypy`, `flake8`, `isort` and `safety` checks
5. `make coverage` - Generates coverage HTML report
6. `make run-test-full` - Runs tests + validations
7. `make run-docker-validate` - Runs validation and tests inside the docker container
