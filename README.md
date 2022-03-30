# Millennium Falcon Challenge

The details of this challenge can be found [here](https://github.com/dataiku/millenium-falcon-challenge).

[//]: <> (todo add a more elaborate description) + add how to start everything up, where to put input files, default files used

## Setup

### To start the web app

If you have Docker and docker-compose installed locally, you can start the application using:
```docker-compose up -d```
By default, the frontend should be available on [port 8501](http://localhost:8501/)
and the backend should be available on [port 8000](http://localhost:8000/).

To stop and remove the containers, networks, volumes, and images created by the previous up command run:
```docker-compose down```

### Backend

The backend is created using [FastApi](https://fastapi.tiangolo.com/).
#todo to run the app details
When running the backend locally, the API docs can be accessed via ```localhost:8000/docs```.

#### Poetry

This project uses Poetry which is a tool for dependency management and packaging in Python. 
It allows you to declare the libraries your project depends on and it will manage (install/update) them for you.
You can read more about Poetry, how to install it and set it up [here](https://python-poetry.org/docs/).

To install dependencies using Poetry, move into the app or frontend directory and run `poetry install`.

### Frontend

The frontend is built using [Streamlit](https://streamlit.io/).
Dependency management is done using [Poetry]((https://python-poetry.org/docs/)) which is described in more detail above.
If the file upload button is not responding, please try allowing pop-ups in your browser and once you adjust this 
setting, restart the browser and try again.

### CLI 

There is an option to get the predictions using a CLI app. There are multiple ways to do it.
- If you have checked out the code and installed the dependencies, from the project root you can simply run the command below, 
specifying the file location relative to the directory that you are running the command from:
```python backend/givemetheodds/cli.py ./backend/givemetheodds/default_inputs/millennium-falcon.json ./backend/givemetheodds/default_inputs/empire.json```
- If you have checked out the code and installed poetry, you can run `poetry install` to install the package and its dependencies. 
You can then run the 

To get more information on the CLI app simply use the `--help` flag.

#### Pre-commit

This project uses [Pre-Commit](https://pre-commit.com/#intro) for identifying simple issues before submitting to code reviews.

To use the hooks available:
- you have to [install](https://pre-commit.com/#install) `pre-commit` locally;
- you have to run `pre-commit install` to install pre-commit into your git hooks. Once executed, pre-commit will run on every commit.

## If only I had more time...

You can get an insight into the way the work was organized in this [planning board](https://github.com/lindavik/mf-challenge/projects/1).
Things that I would consider doing, if I had the luxury of more time:
- End-to-end testing using Cucumber + Selenium + Gherkin for a more Behaviour Driven Development (BDD) style
