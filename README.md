# Lane Detection

## Introduction
Lane Detection is a Python application developed as part of a fourth-year project for the AI course at the University of East Sarajevo - School of Electrical Engineering.

## Features
- Real-time lane detection from a video source.
- Region of interest (ROI) masking for better lane detection.
- Average slope intercept calculation for lane lines.
- Display of detected lanes on the original video frame.
- User-friendly GUI for selecting and displaying videos.

## Installation
To run the LaneDetection project you can run the command: `docker-compose up` 

## Makefile commands
1. `make install` - installs a project with dependecies
2. `make install-test` - installs dev version with dependecies to validation and test
3. `make run-test`- Runs all tests from `tests`
4. `make validate` - Runs `mypy`, `flake8`, `isort` and `safety` checks
5. `make coverage` - Generates coverage HTML report
6. `make run-test-full` - Runs tests + validations
7. `make run-docker-validate` - Runs validation and tests inside the docker container

## Authors

- Vesna Bjeloglav (https://github.com/vbjeloglav)
- Stefan Jokic (https://github.com/stefanjokic99)
- Radmilo Borovina (https://github.com/rborovina)

## License

This application under MIT license.

## Contact

For any additional information or questions, you can contact the authors.
