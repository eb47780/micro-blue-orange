# Docker

- Setting up the developer jobs app on your local machine is quick and easy with the aid of Docker and Docker Compose.
- Docker provides a common virtual environment.
- Please note that these scripts are intended to be executed from this app's root directory.
- These scripts allow you to bypass the need to keep typing "docker-compose run rails-app".

----

# Getting Started (Contributors)

- Open terminal with a shell.
- Clone the repository.

```
git clone https://github.com/endritber/micro-blue-orange.git
```

- Download the Docker images.
- Build the Docker containers.
- Log the screen output from the steps above.

```
docker/build
```

- Run the server with required Docker containers.

```
docker/server
```

- View backend service in the browser at `http://localhost:8000/admin`.
- You will then get the trace of the containers in the terminal. You can stop the containers using Ctrl-C in the terminal.
- Or you can use `docker/kill`.

# Docker Connect to database

- To connect to database user docker command.

```
docker exec -it micro-blue-orange-database psql -U admin -W database
```

# Docker Script Summary

* docker/build: This script builds the Docker containers specified for this app, and logs the screen output for these operations.  After you use "git clone" to download this repository, run the docker/build script to start the setup process.
* docker/server: Use this script to run this app in the Rails server.  This script executes the "docker-compose up" command and logs the results.  If all goes well, you will be able to view this service on your local browser at http://localhost:8000/.
* docker/test: Use this script to run the entire test suite. TODO: ` Not Available `
* docker/run: Use this script to run commands within the Docker container.  If you want shell access, enter "docker/run bash".  To execute "ls -l" within the Docker container, enter "docker/run ls -l".
* docker/kill: This script destroys all Docker containers but leaves the Docker images alone.