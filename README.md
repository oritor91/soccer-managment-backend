# Soccer Management Backend

## Description

Creates a backend server using Python's FastAPI package to perform all backend operation
needed by the front side


## Taskfile usage

There are some common tasks that be managed via Taskfile.yml.
In order to do so, please first create a virtual env running 

`pip install go-task-bin`

See all available tasks

- `task --list-all`

Create virtual env

- `task create-venv`


Run development server locally

- `task run`

This will run the backend server on your localhost at
http://127.0.0.1:8000/docs
