# LegacyOCaml-Update-2025
Epitech Project which consists in modernizing a OCaml app


# You can find our documents to this link

https://www.notion.so/AWKWARD-LEGACY-26b5abaf37a48050a429ef73b7526a2f?source=copy_link


# ⚙️ Project Automation — Makefile

To simplify testing, building, and running the project, we implemented a **Makefile-based automation system**.  
It ensures **reproducibility**, **ease of use**, and adherence to **DevOps best practices**.

---

## 🧩 Main Commands

| Command | Description |
|----------|--------------|
| `make` / `make all` | Runs the full workflow: executes requirements, audit, conventions, unit tests, then builds and launches the Docker containers if tests pass. |
| `make dependencies` | Executes pip install on file requirements.txt. Stops immediately if any module fails. |
| `make test` | Executes all unit tests using **pytest** with verbose output. Stops immediately if any test fails. |
| `make build` | Builds and runs all containers defined in `docker-compose.yml` in **interactive mode** (logs appear directly in the terminal). |
| `make audit` | Executes an audit using pip-audit to detect any vulnerabilitie in requirements.txt.Stops immediately if any audit founds.
| `make conventions` | Executes conventions pycodestyle(PEP8).Stops immediately if any conventions error found.
| `make clean` | Stops containers and removes Python cache folders (`__pycache__`, `.pytest_cache`, `.coverage`, etc.). |
| `make fclean` | Performs a full cleanup: same as `clean` + removes all Docker images labeled for the project. |
| `make re` | Equivalent to `make fclean all` — performs a complete rebuild and relaunch. |
| `make admin` | Launches the **Admin interface**: `python -m geneweb.gwsetup`. Accepts additional runtime arguments via `ARGS`. |
| `make user` | Launches the **User interface**: `python -m geneweb.gwd`. Accepts additional runtime arguments via `ARGS`. |
| `make stop` | Stops all active containers. |

---

## 🧠 Passing Arguments to Python Commands

The `admin` and `user` targets accept **custom runtime arguments** through the `ARGS` variable.  

Example usage:

```bash
make user ARGS="--port 8081 --debug"
make admin ARGS="--config config/dev.yaml"
```

## dependencies

Executes pip install on file requirements.txt

```bash
make requirements
```
*   Prints an error message if dependencies fail.
    
*   Prints a success message if all dependencies pass.


## test

Runs all unit tests using pytest.

```bash
make test
```

*   Prints an error message if tests fail.
    
*   Prints a success message if all tests pass.
    

### build

Builds and launches Docker containers using Docker Compose.

```bash
make build
```

*   Typically run after tests succeed.
    
*   Displays messages before and after building containers.
    

### audit

Executes an audit using pip-audit to detect any vulnerabilitie in requirements.txt.

```bash
make audit
```

*   Prints an error message if audit fail.
    
*   Prints a success message if audit pass.


### conventions

Executes conventions pycodestyle(PEP8)

```bash
make conventions
```

*   Prints an error message if pycodestyle fail.
    
*   Prints a success message if pycodestyle pass.


### clean

Cleans Docker containers and Python cache files.

```bash
make clean
```

*   Stops Docker containers.
    
*   Deletes Python cache directories: \_\_pycache\_\_, .python\_cache, .pytest\_cache, .coverage.
    
*   Deletes .pyc files.
    

## fclean

Performs a full cleanup: containers, caches, and Docker images.

```bash
make fclean
```

*   Runs clean.
    
*   Removes Docker images labeled with geneweb.
    

## re

Performs a complete rebuild: fclean followed by all.

```bash
make re
```

## admin

Launches the Admin interface manually.

```bash
make admin ARGS="..."
```

*   ARGS can include optional arguments for the admin interface.
    

## user

Launches the User interface (non-admin).

```bash
make user ARGS="..."
```

*   ARGS can include optional arguments for the user interface.
    

## logs

Displays Docker container logs.

```bash
make logs
```

## stop

Stops all project containers.

```bash
make stop
```