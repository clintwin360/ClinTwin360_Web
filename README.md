# ClinTwin360_Web
The Sponsor Web Application for ClinTwin360

To run the application on developer machine, make sure you have `docker` and `docker-compose` installed.

Run the command

``` docker-compose up --build --remove-orphans ```

To run the docker-compose in daemon mode,

``` docker-compose up --build --remove-orphans -d ```

Once the application is running, you can access the application using the url

```http://127.0.0.1:8000/```

To load test data in the application, access the URL from any browser

```http://127.0.0.1:8000/sponsor/loaddata/ ```

Once the above call returns, it creates an admin user with credentials ```username: admin, password:admin``` and test sponsors with credentials,
```username: pitt, password:blackandgold```
```username:amsterdam,password:redlight```
```username:kaiser,password:permanente```
Note: The data is only prepopulate to prevent the repetitive efforts of loading the data. Any data added through forms is also persistent and can be used. 

The docker image runs by mouting the code files on the docker image, any changes made to the source files will be effective immediately.
