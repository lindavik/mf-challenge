# Millennium Falcon Challenge

The Death Star - the Empire's ultimate weapon - is almost operational and is currently approaching the Endor planet. The
countdown has started.

Han Solo, Chewbacca, Leia and C3PO are currently on Tatooine boarding on the Millennium Falcon. They must reach Endor to
join the Rebel fleet and destroy the Death Star before it annihilates the planet.

The Empire has hired the best bounty hunters in the galaxy to capture the Millennium Falcon and stop it from joining the
rebel fleet...

You can read more about the challenge [here](https://github.com/dataiku/millenium-falcon-challenge).

The solution proposed here uses a Depth First Search based algorithm to calculate the odds of the Millennium Falcon
reaching Endor in time and saving the galaxy.

## Starting The Web App

If you have Docker and docker-compose installed locally, you can follow the steps below.

First build your app images using ```docker-compose build```.

You can start the application using:
```docker-compose up -d```
By default, the frontend should be available on [port 8501](http://localhost:8501/)
and the backend should be available on [port 8000](http://localhost:8000/).

To stop and remove the containers, networks, volumes, and images created by the previous up command run:
```docker-compose down```

### Backend

The backend is created using [FastApi](https://fastapi.tiangolo.com/). To locally run the backend separately (
for `docker-compose` see above), from the project root directory run
`python backend/givemetheodds/main.py`. You can also build a Docker image in the `backend` directory and run it locally.

Without reconfiguring the ports, the app should spin up and be accessible on port 8000: ```localhost:8000```
When running the backend locally, the API docs can be accessed via ```localhost:8000/docs```.

You can add custom startup files by adding them to the `backend/inputs` folder in the project root:

- mission details must be named `millennium-falcon.json`;
- the planet database must be named `universe.db`. A default file for each is already available in the folder.

### Frontend

The frontend is built using [Streamlit](https://streamlit.io/). Dependency management is done
using [Poetry]((https://python-poetry.org/docs/)) which is described in more detail below.

Without reconfiguring the ports, the frontend app should spin up and be accessible on port 8501: ```localhost:8501```

If the file upload button is not responding, please try allowing pop-ups in your browser and once you adjust this
setting, restart the browser and try again.

### CLI App

There is an option to get the predictions using a CLI app. To do this you have to do the following steps:

- check out the project code;
- install Poetry (see above);
- navigate into the `backend` directory and run `poetry install` to install the package and its dependencies.

Once done, from the backend directory you can then run
`give-me-the-odds inputs/millennium-falcon.json inputs/empire.json`
(assuming your input files are in the `inputs` folder). NB! The file location must be relative to the path from which
you are running the command.

To get more information on the CLI app simply use the `--help` flag.

## Setup

### Poetry

This project uses Poetry which is a tool for dependency management and packaging in Python. It allows you to declare the
libraries your project depends on and it will manage (install/update) them for you. You can read more about Poetry, how
to install it and set it up [here](https://python-poetry.org/docs/).

To install dependencies using Poetry, move into the app or frontend directory and run `poetry install`.

### Pre-commit Hooks

This project uses [Pre-Commit](https://pre-commit.com/#intro) for identifying simple issues before submitting to code
reviews.

To use the hooks available:

- you have to [install](https://pre-commit.com/#install) `pre-commit` locally;
- you have to run `pre-commit install` to install pre-commit into your git hooks. Once executed, pre-commit will run on
  every commit.

In this particular case, I have added a pre-commit hook for [shed](https://github.com/Zac-HD/shed) which takes care of
managing unused imports, code formatting etc. You can read more about it [here](https://github.com/Zac-HD/shed).

## If only I had more time...

You can get an insight into the way the work was organized in
this [planning board](https://github.com/lindavik/mf-challenge/projects/1). Things that I would consider doing, if I had
the luxury of more time:

- Spend more time refactoring the code as there are still some bits which I would like to improve for readability,
  particularly in the prediction service;
- Right now the route optimisation to avoid bounty hunters is very simplistic and flawed, if I had more time, I would
  try different more different approaches;
- I would add unit tests for the Frontend and/or end-to-end testing using Cucumber + Selenium + Gherkin for a more
  Behaviour Driven Development (BDD) style;
- Investigate why the Streamlit file uploader button sometimes does not work well on Chrome. At least the drag and drop
  always seems to work.
- I had issues getting Poetry to work with GitHub Actions and at the time it was not a priority. I would either figure
  out how to make Poetry and GitHub Actions work together or find a pre-commit hook that generates the requirements file
  from the Poetry toml file on commit, as the hooks I found were flawed and again this was not a priority.
- Depending on the registry that you deploy your Artifacts to, there are always interesting things to set up like
  continuous deep recursive scanning, signing and verifying the signed Docker images etc.
- I could also add a [docker-slim](https://github.com/docker-slim/docker-slim) step to the CI/CD to minimize the
  image/potential attack surface. Additionally, I could/should update the Docker image to use a leaner base image.

