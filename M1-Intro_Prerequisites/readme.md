Ref:
[Module 1 Introduction & Prerequisites](https://dezoomcamp.streamlit.app/Module%201%20Introduction%20&%20Prerequisites)

This is the note taking from the course video (DEZ 1.4.2: Using Github Codespaces for the Course (by Luis Oliveira))

# Outcome of this Module


# Why should we care about Docker?
1. Reproducibility (handling 'it works on my machine' issues)
2. Local experiments (e.g. Integration tests using multiple versions of Python, Postgres DBs)
3. Integration Tests (e.g. CI/CD pipelines)
4. Running pipelines on different cloud providers (e.g. AWS, Azure, GCP)
5. Serverless
6. Spark

# Benefit of this setup
1. Just need followings installed in your local machine:
   1. VS Code
2. No need to install anything else

# Setup GitHub Codespaces, Terraform, Jupyter notebooks and Postgres + pgAdmin Containers
Ref: https://www.youtube.com/watch?v=XOSUt8Ih3zA&list=PL3MmuxUbc_hKihpnNQ9qtTmWYy26bPrSb&index=3

## Create a GitHub Codespace from a repo
1. Create a new repo in GitHub
2. Create a new Codespace from the repo
3. Connect to the Codespace from Desktop VS Code
![Alt text](<Assets/connect_vscode_codespace.png>)

## Install Terraform
1. Copy the following commands from [here](https://developer.hashicorp.com/terraform/install?product_intent=terraform#Linux)
2. Paste the commands in the terminal of your Codespace and run them.

## Install Jupyter notebooks
1. Copy the following commands:
```bash
pip install jupyter
```

2. Start Jupyter notebook
```bash
jupyter notebook
```

3. Copy the URL from Terminal and open the notebook in the browser
4. Press `ctrl + c` to stop the notebook server

## Docker: Setup postgres DB
1. Create network
``` bash
docker network create pg-network
```

2. Create volume
``` bash
docker network create pg-network
```

3. Postgres Databse - Pull image and run the container
``` bash
docker run -it \
-e POSTGRES_USER="root" \
-e POSTGRES_PASSWORD="root" \
-e POSTGRES_DB="ny_taxi" \
-v dtc_postgres_volume_local:/var/lib/postgresql/data \
-p 5432:5432 \
--network=pg-network \
--name pg-database \
postgres:13
```

4. pgAdmin - Pull image and run the container
``` bash
docker run -it \
-e PGADMIN_DEFAULT_EMAIL="admin@admin.com" \
-e PGADMIN_DEFAULT_PASSWORD="root" \
-p 8080:80 \
--network=pg-network \
--name pgadmin \
  dpage/pgadmin4
```
![Alt text](<Assets/pg_8080.png>)

5. Create a new server
![Alt text](<Assets/pg_create_new_server1.png>)
![Alt text](<Assets/pg_create_new_server2.png>)
![Alt text](<Assets/pg_create_new_server3.png>)

6. Press `ctrl + c` in the terminal to stop the container(s)