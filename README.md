# Millennium Falcon Challenge

The details of this challenge can be found [here](https://github.com/dataiku/millenium-falcon-challenge).

[//]: <> (todo add a more elaborate description) + add how to start everything up, where to put input files, default files used

## Setup

### To start

```docker-compose up -d```

### Backend

The backend is created using [FastApi](https://fastapi.tiangolo.com/).
#todo to run the app details
When running the backend locally, the API docs can be accessed via ```localhost:8000/docs```.

#### Poetry

This project uses Poetry which is a tool for dependency management and packaging in Python. 
It allows you to declare the libraries your project depends on and it will manage (install/update) them for you.
You can read more about Poetry, how to install it and set it up [here](https://python-poetry.org/docs/).

To install dependencies using Poetry, move into the `app` directory (backend component) and run `poetry install`.


### Frontend

The frontend is built using [Streamlit](https://streamlit.io/).
Dependency management is done using [Poetry]((https://python-poetry.org/docs/)) which is described in more detail above.
If the file upload button is not responding, please try allowing pop-ups in your browser and once you adjust this 
setting, restart the browser and try again.

#### Pre-commit

This project uses [Pre-Commit](https://pre-commit.com/#intro) for identifying simple issues before submitting to code reviews.

To use the hooks available:
- you have to [install](https://pre-commit.com/#install) `pre-commit` locally;
- you have to run `pre-commit install` to install pre-commit into your git hooks. Once executed, pre-commit will run on every commit.

## If only I had more time...

You can get an insight into the way the work was organized in this [planning board](https://github.com/lindavik/mf-challenge/projects/1).
Things that I would consider doing, if I had the luxury of more time:
- End-to-end testing using Cucumber + Selenium + Gherkin for a more Behaviour Driven Development (BDD) style
- 