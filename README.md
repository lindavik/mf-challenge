# Millennium Falcon Challenge

## Problem description
The Death Star - the Empire's ultimate weapon - is almost operational and is currently approaching the Endor planet. The countdown has started.

Han Solo, Chewbacca, Leia and C3PO are currently on Tatooine boarding on the Millennium Falcon. They must reach Endor to join the Rebel fleet and destroy the Death Star before it annihilates the planet.

The Empire has hired the best bounty hunters in the galaxy to capture the Millennium Falcon and stop it from joining the rebel fleet...

This project provides with a solution to calculate the odds of the Millennium Falcon reaching Endor in time and saving the galaxy.

You can read more about the challenge [here](https://github.com/dataiku/millenium-falcon-challenge).

## Solution outline

The solution algorithm works as follows:
- Based on the provided input files, Dijkstra's algorithm is used to find the shortest path in a weighted graph.
Here we regard the planets as nodes and the distances as the weights;
- Once we have determined the shortest path between the starting node, i.e. the departure planet, and the end node, i.e.
the destination planet, we assume that this is the best path (even though a longer path with fewer bounty hunters might 
actually be better from a probability perspective in reality);
- If the shortest path (adjusted for fuelling needs) exceeds the time limit, i.e. countdown, the probability of success becomes zero;
- If the shortest path is within the provided time limit, we continue to calculate the probability of success based on
the intercepted information on bounty hunter presence.

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

There is an option to get the predictions using a CLI app.
To do this you have to do the following steps:
- check out the project code;
- install Poetry (see above);
- navigate into the `backend` directory and run `poetry install` to install the package and its dependencies.

Once done, from the project root directory you can then run
`give-me-the-odds inputs/millennium-falcon.json inputs/empire.json`
  (assuming your input files are in the `inputs` folder).
NB! The file location must be relative to the path from which you are running the command.

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
