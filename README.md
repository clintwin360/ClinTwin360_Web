# ClinTwin360_Web
The Sponsor Web Application for ClinTwin360

To run the application on developer machine, make sure you have `docker` and `docker-compose` installed.

Run the command

``` docker-compose up --build --remove-orphans ```

To run the docker-compose in daemon mode,

``` docker-compose up --build --remove-orphans -d ```

Once the application is running, you can access the application using the url

```http://127.0.0.1/api```

The docker image runs by mouting the code files on the docker image, any changes made to the source files will be effective immediately.
