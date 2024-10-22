# Vehicle Allocation

## How to run this APP Locally

### `.env` file is already provided, no need to create any

## `Windows`:

1) Keep the Docker Desktop running

2) ### `docker-compose up --build` run it on vs code or other IDE terminal

3) ### Go to `http://localhost:8000/docs` to test the api

## `Linux`:

1) ### `sudo docker-compose up --build` run it on vs code or other IDE terminal

2) ### Go to `http://localhost:8000/docs` to test the api


## `Optional`:

#### You may create a `venv` (virtual environment) and install the package from requirements.txt file
#### Doing so will remove the red mark or import error from text editor of any IDE.

### To Do so: 

1) #### `python -m venv venv`
2) #### `venv\Scripts\activate`
2) #### `pip install -r requirements.txt`


## `Deploy` and `Maintain`:

### `Deploy`:

1) #### I could deploy the project on aws ec2 instance or lambda.
2) #### Suppose for EC2 I will first create an instance
3) #### That instance could be on amazon linux AMI or an Ubuntu Server
4) #### as per my region intance type would be t3.micro
5) #### creating a new key pair and allow http and https with ssh
6) #### After inctance gets created we would open a terminal and connect via ssh (If using wsl, pem should be on wsl directory)
7) #### Then, Install Docker and docker compose 
8) #### Now, we can upload our code to ec2 instance using `scp` or using `git` clone.
9) #### docker-compose up --build
10) #### It will make the fastapi accessible publicly. Example: `http://ec2-public-ip:8000`


### `Maintain`

1) #### I could implement CI/CD pipeline, so that It gets instantly deployed after a change in a certain branch.

2) #### If I work with a team, then we can connect Slack Bot with our git repository. In this way, if anyone pushes any code, or merges any branch we will be notified.

3) #### We got configure Snyk with out repository. So, that any vulnerabilities or old packages can get detected automatically, also we could configure it to automate pull request with updated package versions.

4) #### Task for the project could be assigned to team and maintain via ClickUp or Jira Board.