# Dependency Management with UV

### 1.Installation

```bash
curl -LsSf https://astral.sh/uv | sh
uv --version
```

### 2. Creating new project

To create an empty folder and initialize a project: 
```bash
uv init my-app # Creates the folder my-app and initialize a project
```

To initialize a project under the current folder:
```bash
uv init
```

### 3. Adding dependencies to project

```bash
uv add fastapi uvicorn black
```
This will add the dependencies to the virtual environment of the project.

### 4. Running commands / scripts

To run a python source file:

```bash 
uv run main.py
```

To run a command (for exampo):

```bash
uv run black main.py # format main.py with black
```

### 5. Working with FastAPI 

Write a simple FastAPI server:

```python 
# main.py 
from fastapi import FastAPI 

app = FastAPI()

app.get("/")
async def root():
    return {"Message":"Hello World from FastAPI!"}

```

Running it with uvicorn:

```bash
uv run uvicorn main:app --reload
```
