Ref:
[Module 1 Introduction & Prerequisites](https://dezoomcamp.streamlit.app/Module%201%20Introduction%20&%20Prerequisites)

This is the note taking from the course videos

# 0. Outcome of this Module
## Data Architecture
![Alt text](<assets/Week1_Data_Architecture.jpg>)

## Why should we care about Docker?
1. Reproducibility (handling 'it works on my machine' issues)
2. Local experiments (e.g. Integration tests using multiple versions of Python, Postgres DBs)
3. Integration Tests (e.g. CI/CD pipelines)
4. Running pipelines on different cloud providers (e.g. AWS, Azure, GCP)
5. Serverless
6. Spark

## Benefit of this setup
1. Just need followings installed in your local machine:
   1. VS Code
2. No need to install anything else

# 1. Setup Development Environment
Ref: https://www.youtube.com/watch?v=XOSUt8Ih3zA&list=PL3MmuxUbc_hKihpnNQ9qtTmWYy26bPrSb&index=3

## Create a GitHub Codespace from a repo
1. Create a new repo in GitHub
2. Create a new Codespace from the repo [Codespaces Free Tier](https://docs.github.com/en/billing/managing-billing-for-github-codespaces/about-billing-for-github-codespaces)
3. Connect to the Codespace from Desktop VS Code
![Alt text](<assets/connect_vscode_codespace.png>)

## Setup postgres DB and pgAdmin
1. Postgres Databse - Pull image and run the container (docker compose service = postgres)

2. pgAdmin - Pull image and run the container (docker compose service = pgadmin)
![Alt text](<assets/pg_8080.png>)

3. Create a new server

Note: In the field `Host name/ address`, type the name in `network` of the docker-compose.yml file

![Alt text](<assets/pg_create_new_server1.png>)
![Alt text](<assets/pg_create_new_server2.png>)
![Alt text](<assets/pg_create_new_server3.png>)

4. Press `ctrl + c` in the terminal to stop the container(s)

# 2. Ingesting NY Taxi Data to Postgres DB using Jupyter Notebook
1. Copy the following commands:
```bash
pip install jupyter
```

2. Start Jupyter notebook
```bash
jupyter notebook
```

3. Copy the URL from Terminal and open the notebook in the browser
4. Write the code in the [notebook](10-Ingest_NY_Taxi.ipynb)
5. (Optional) execute the cells in notebook
6. Press `ctrl + c` to stop the notebook server

# 3. Putting the ingestion script into Docker
1. Convert Jupyter notebook to .py file
```bash
jupyter nbconvert --to=script 10-Ingest_NY_Taxi.ipynb
```
2. Tidy up the .py file by removing the unwanted lines
3. Add `argparse` to the .py file
4. Refactor the hard-coded values to variables (see [10-Ingest_NY_Taxi_refactor.py](10-Ingest_NY_Taxi_refactor.py))
5. (Optional) Test the refactored script 
   (Expected results: a table called `green_taxi_data` with 672105 rows)
```pgAdmin
DROP TABLE public.yellow_taxi_data
```

```bash
cd M1-Intro_Prerequisites
python '10-Ingest_NY_Taxi_refactor.py' \
    --user=root \
    --password=root \
    --host=localhost \
    --port=5432 \
    --database=ny_taxi \
    --table=green_taxi_data \
    --data_source=https://d37ci6vzurychx.cloudfront.net/trip-data/green_tripdata_2019-01.parquet
```
1. Create a Dockerfile, which contains all the required packages and py script (see [Dockerfile](Dockerfile))
2. Build the image
```bash
docker build -t taxi_ingest:v001 .
```
3. Test the container
```bash
docker run -it \
    --network=m1-intro_prerequisites_pg-network \
    taxi_ingest:v001 \
      --user "root" \
      --password "root" \
      --host "pg-database" \
      --port 5432 \
      --database "ny_taxi" \
      --table "green_taxi_data" \
      --data_source "https://d37ci6vzurychx.cloudfront.net/trip-data/green_tripdata_2019-01.parquet"
```

# 4. Terraform & Google Cloud Platform (GCP)
## Why Terraform?
1. Simplicity in keeping track of infrastructure
2. Easier collaboration (e.g. git)
3. Reproducibility (e.g. Ensure Dev, Test, Prod are the same)
4. Ensure resources are removed when not needed (avoiding unnecessary costs in the cloud)

## What Terraform is not for?
1. Does not manage/ update code on infrastructure
2. Does not give you the ability to change immutable resources
3. Not used to manage resources not defined in your terraform files

## What is Terraform?
1. Infrastructure as Code (IaC) - Create resources with code files

## Key Terraform Commands
1. `init` - Get me the providers I need
2. `plan` - What ami I about to do? Preview the resources to be created
3. `apply` - Do it! Create the resources
4. `destroy` - Destroy the resources

## GCP
### Create a Project
### Create a Service Account
1. Go to Project Dashboard
2. Click `IAM & Admin` -> `Service Accounts`
3. Click `Create Service Account` (For automation usage)
4. Service account details -> Name: `terraform-runner`
5. Grant this service account access to project:
   1. Cloud Storage -> `Storage Admin` (Use `Creator` in the real world)
   2. BigQuery -> `BigQuery Admin` (Use `Creator` in the real world)
   3. Compute Engine -> `Compute Admin` (Use `Creator` in the real world)
6. In case you to change the existing service account, click on `IAM`, choose the service account and click `Edit`, add or change the role(s)

### Get the Service Account key
1. Go to Project Dashboard
2. Click `IAM & Admin` -> `Service Accounts`
3. Click on the service account you want to use
4. Click `Manage Keys` -> `Add Key` -> `Create new key` -> `JSON` -> `Create`
5. Carefully save the JSON file in a safe place, never commit it to git!

### Install Terraform
1. Copy the following commands from [here](https://developer.hashicorp.com/terraform/install?product_intent=terraform#Linux)
2. Paste the commands in the terminal of your Codespace and run them.
```bash
wget -O- https://apt.releases.hashicorp.com/gpg | sudo gpg --dearmor -o /usr/share/keyrings/hashicorp-archive-keyring.gpg
echo "deb [signed-by=/usr/share/keyrings/hashicorp-archive-keyring.gpg] https://apt.releases.hashicorp.com $(lsb_release -cs) main" | sudo tee /etc/apt/sources.list.d/hashicorp.list
sudo apt update && sudo apt install terraform
```

### Prepare the Terraform file
1. See [`main.tf`](main.tf)
2. Test with `terraform init`

### Create & Destroy a Storage Bucket in GCP
1. Google search for `gcp terraform storage bucket`
2. Copy the example
3. Paste it in the `main.tf` file
4. Review with `terraform plan`
![Alt text](<assets/tf_plan1.png>)
5. Build the resources with `terraform apply` -> Type `yes`
![Alt text](<assets/tf_apply1.png>)
6. Note there is a file called `terraform.tfstate` created in the local machine 
7. Destroy the resources with `terraform destroy` -> Type `yes`
![Alt text](<assets/tf_destroy1.png>)

### Create & Destroy a BigQuery Dataset in GCP
1.