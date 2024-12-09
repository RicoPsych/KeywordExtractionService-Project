# Intelligent Text Processing Service - Project Template

## Project Setup

1. **Install Python 3.12**
    * Download and install Python 3.12 from the official
      website: [Python 3.12 Download](https://www.python.org/downloads/).
      Make sure that Python is added to your system's `PATH` during installation, so that the Python command can be used
      from the terminal or command prompt.

2. **Install `pip`**
    * `pip` is the package manager for Python. It allows you to install, update, and manage third-party Python packages.
    * If you're using Python 3.12, `pip` should already be included. Verify the installation by running:
      ```bash
      pip --version
      ```
    * If `pip` is not installed or needs to be updated, follow the official installation
      guide: [pip Installation Guide](https://pip.pypa.io/en/stable/installation/).

3. **Set up a Virtual Environment (`venv`)**
    * A virtual environment (`venv`) isolates the dependencies of your project, ensuring that packages installed for
      this project don’t interfere with other projects or the global Python installation.
    * To create a virtual environment in your project directory, run the following command:
      ```bash
      python -m venv .venv
      ```
    * This creates a `.venv` directory that contains a separate Python interpreter and its own package directories.
    * You need to **activate the virtual environment** every time you work on the project:
        * On **Linux/macOS**, use:
          ```bash
          source .venv/bin/activate
          ```
        * On **Windows**, use:
          ```powershell
          .venv\Scripts\Activate.ps1
          ```
    * Once activated, your terminal should show a prefix like `(.venv)`, indicating that you are inside the virtual
      environment.

4. **Install Project Dependencies**
    * After activating the virtual environment, you need to install the dependencies required for the project. These
      dependencies are listed in the `requirements.txt` file.
    * Run the following command to install them:
      ```bash
      # remember to activate venv first!
      pip install -r requirements-dev.txt
      ```
    * This ensures that all necessary libraries are installed in your virtual environment and are isolated from the
      system-wide Python installation.

5. Build and test the project
    * install Docker from the official website (https://www.docker.com/get-started/)
    * run `build.sh` (Linux) or `build.ps1` (Windows) to build the project
    * start the Docker Container by running:
      ```bash
      docker run --rm -p 8080:8080 renameme:latest
      ```
    * visit http://localhost:8080/docs You should see the Swagger UI and be able to send a request to the service REST
      API

6. Rename all places and variables that use to service name:
    * `src/renameme_service` directory
    * Docker Image name in `build.ps1` and `build.sh`
    * project name and known-first-party in `pyproject.toml`

7. (Optional) Run the project from PyCharm
    * In the top menu select `Run` > `Edit configurations` > `Add new configuration` (+ symbol) > find and
      chose `FastApi`
    * In the configuration window set the `Application file` to full path to `src\main.py`
    * Then you can start the project from PyCharm

## Project configuration

The project uses `pyproject.toml` file for storing the project configuration. The `pyproject.toml` file provides a clean
and standardized way to manage dependencies, configure tools like linters (e.g., Ruff), and streamline the setup for
build and packaging tasks.

### Ruff - linter and code formatter

Ruff is a tool that checks your Python code for errors, formatting issues, and potential bugs. This process is called
linting. By ensuring that your code follows best practices, Ruff helps improve code quality and consistency across the
project.

The Ruff configuration is stored in `pyproject.toml` in `[tool.ruff]` tables

To check your code for any issues, run:

```bash
ruff check src
```

Ruff can also automatically fix some of these problems (such as formatting). To apply fixes, run:

```bash
ruff check src --fix
```

Ruff is also executed during in the `build.sh` and `build.ps1`

### Dependency management

The project uses `pip-tools` (https://github.com/jazzband/pip-tools) to manage both production and development
dependencies effectively.
`pip-tools` is a set of tools that helps you manage Python dependencies by resolving and locking down specific versions,
ensuring consistency across environments. It automatically resolves and pins all transitive dependencies, preventing
conflicts and avoiding "dependency hell."

Important files:

* `requirements.in` - lists production dependencies
* `requirements-dev.in` includes development dependencies and references `requirements.in` to keep dev environments
  aligned with production
* `requirements.txt` and `requirements-dev.txt` - list all dependencies, including all transitive dependencies with all
  pinned versions, ensuring that the exact same dependencies are installed across different environments **YOU MUST NOT
  MODIFY THEM MANUALLY**

If you want to add new library to your project, you must add them to either `requirements.in` (if the library is
required to deploy the service) or to `requirements-dev.in` (if the library is required only during development). Then
run following command to  generate `requirements.txt` and `requirements-dev.txt`:

```bash
pip-compile requirements.in
pip-compile requirements-dev.in
```
This will resolve and pin all dependencies, generating `requirements.txt` and `requirements-dev.txt` files

To install dependencies on your computer run:

```bash
# remember to activate venv first!
pip install -r requirements-dev.txt
```

## Project structure

│ .dockerignore - Specifies files and directories to ignore when building the Docker image.  
│ .gitignore - Lists files and directories that should be ignored by Git version control.  
│ build.ps1 - PowerShell script for building the project  
│ build.sh - Bash script for building the project  
│ Dockerfile  
│ pyproject.toml - Defines project metadata, configuration for tools (such as Ruff), etc   
│ readme.md  
│ requirements-dev.in - Lists the development dependencies (including production ones via -r requirements.in).   
│ requirements-dev.txt - The compiled and pinned versions of all development dependencies.  
│ requirements.in - Lists the main dependencies required for the project in production.  
│ requirements.txt - The compiled and pinned versions of all production dependencies.  
└───src - Contains the source code for the service  

## FastAPI

This project uses **FastAPI** as the web framework for building the REST API. FastAPI is designed to simplify the
development of APIs while ensuring high performance. Key features relevant to this project include:

* a straightforward way to define API endpoints for handling HTTP methods (e.g., GET, POST, PUT, DELETE)
* Swagger Documentation: FastAPI automatically generates an interactive API documentation interface using Swagger UI
* Request Validation: FastAPI validates incoming data based on Python type hints

The project will use `APIRouter` to organize and structure the API into multiple, smaller modules.
Each router can handle a specific set of routes (e.g., user-related or product-related endpoints) and is registered with
the main FastAPI application.
For more details check:

* `main.py`
* `routers/example.py`

Learn more: https://fastapi.tiangolo.com/tutorial/
