# AIMealPlannerBE

# 2 ways to run the project
## Using docker
Download docker for your machine: https://docs.docker.com/compose/install/

(Optional but recommend) Install docker and docker compose extension for your IDE

Start app: in terminal run "docker-compose up -d" or "make dev"
Stop app: in terminal run "docker-compose down" or "make dev-down"

Or use the docker compose extension function if you have it

## Run wihout docker
(Caution) You will need to change mongo and elasticsearch value in config/setting.toml to a valid connection

Download python3.8 and create and venv with it
Run "pip install -r requirements.txt"
Run "make start-reload" or "make start"

## Folder structure
app
    database -> code for database connection
    dto -> data transfer object, still contain my previous project code, use for reference
    helpers -> helper function and class
    middlewares -> handle middleware logic like CORS, exception, api limiter
    models -> data model, still contain my previous project code, use for reference
    routers -> Controllers code, still contain my previous project code, use for reference
    services -> Logic class stand between controller and model, still contain my previous project code, use for reference
    settings -> load setting from file
config -> config file

## Swagger
After app run, go to:
localhost:8080/docs for swagger ui
localhost:8080/redoc for redoc

## Secret key
In docer-compose.yml, mealplanner.environment have 2 values. These are not included in the commit
Contact me to get those values
