## Module 1 Homework

## Docker & SQL

In this homework we'll prepare the environment 
and practice with Docker and SQL


## Question 1. Knowing docker tags

Run the command to get information on Docker 

```docker --help```

Now run the command to get help on the "docker build" command:

```docker build --help```

Do the same for "docker run".

Which tag has the following text? - *Automatically remove the container when it exits* 

- `--delete`
- `--rc`
- `--rmc`
- <span style="color:green">--rm</span>


## Question 2. Understanding docker first run 

Run docker with the python:3.9 image in an interactive mode and the entrypoint of bash.

dockerfile
```dockerfile
FROM python:3.9
ENTRYPOINT ["bash"]
```

bash
```bash
docker build -t homework_Q2:latest .
docker run --rm -it  homework_Q2:latest
```

Now check the python modules that are installed ( use ```pip list``` ). 

What is version of the package *wheel* ?

- <span style="color:green">0.42.0</span>
- 1.0.0
- 23.0.1
- 58.1.0


# Prepare Postgres

Run Postgres and load data as shown in the videos
We'll use the green taxi trips from September 2019:

```wget https://github.com/DataTalksClub/nyc-tlc-data/releases/download/green/green_tripdata_2019-09.csv.gz```

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
      --data_source "https://d37ci6vzurychx.cloudfront.net/trip-data/green_tripdata_2019-09.parquet"
```

You will also need the dataset with zones:

```wget https://s3.amazonaws.com/nyc-tlc/misc/taxi+_zone_lookup.csv```

```bash
docker run -it \
    --network=dataengineerzoomcamp2024_pg-network \
    taxi_ingest:v001 \
      --user "root" \
      --password "root" \
      --host "pg-database" \
      --port 5432 \
      --database "ny_taxi" \
      --table "taxi_zone_lookup" \
      --data_source "https://s3.amazonaws.com/nyc-tlc/misc/taxi+_zone_lookup.csv"
```

Download this data and put it into Postgres (with jupyter notebooks or with a pipeline)


## Question 3. Count records 

How many taxi trips were totally made on September 18th 2019?

Tip: started and finished on 2019-09-18. 

Remember that `lpep_pickup_datetime` and `lpep_dropoff_datetime` columns are in the format timestamp (date and hour+min+sec) and not in date.

```sql
select count(*)
FROM public.green_taxi_data
WHERE 1=1
AND date(lpep_pickup_datetime ) = '2019-09-18'
;
```

- 15767
- <span style="color:green">15612</span>
- 15859
- 89009

## Question 4. Largest trip for each day

Which was the pick up day with the largest trip distance
Use the pick up time for your calculations.

```sql
select 
    date(lpep_pickup_datetime) as pickup_date,
    sum(trip_distance)
FROM public.green_taxi_data
group by date(lpep_pickup_datetime)
order by sum(trip_distance) desc
;
```

- 2019-09-18
- 2019-09-16
- <span style="color:green">2019-09-26</span>
- 2019-09-21


## Question 5. Three biggest pick up Boroughs

Consider lpep_pickup_datetime in '2019-09-18' and ignoring Borough has Unknown

Which were the 3 pick up Boroughs that had a sum of total_amount superior to 50000?
 
```sql
SELECT B."Borough", sum(A.total_amount)
FROM public.green_taxi_data A
LEFT JOIN public.taxi_zone_lookup B ON 1=1
	AND A."PULocationID" = B."LocationID"
WHERE 1=1
	AND date(lpep_pickup_datetime) = '2019-09-18'
	AND B."Borough" <> 'Unknown'
GROUP BY B."Borough"
HAVING sum(A.total_amount) > 50000
ORDER BY sum(A.total_amount) DESC
```

- <span style="color:green">"Brooklyn" "Manhattan" "Queens"</span>
- "Bronx" "Brooklyn" "Manhattan"
- "Bronx" "Manhattan" "Queens" 
- "Brooklyn" "Queens" "Staten Island"


## Question 6. Largest tip

For the passengers picked up in September 2019 in the zone name Astoria which was the drop off zone that had the largest tip?
We want the name of the zone, not the id.

Note: it's not a typo, it's `tip` , not `trip`

```sql
SELECT
	C."Zone" as DO_Zone,
	MAX(A.tip_amount)
FROM public.green_taxi_data A
LEFT JOIN public.taxi_zone_lookup B ON 1=1
	AND A."PULocationID" = B."LocationID"
LEFT JOIN public.taxi_zone_lookup C ON 1=1
	AND A."DOLocationID" = C."LocationID"
WHERE 1=1
	AND B."Zone" = 'Astoria'
GROUP BY
	C."Zone"
ORDER BY MAX(A.tip_amount) DESC
```

- Central Park
- Jamaica
- <span style="color:green">JFK Airport</span>
- Long Island City/Queens Plaza



## Terraform

In this section homework we'll prepare the environment by creating resources in GCP with Terraform.

In your VM on GCP/Laptop/GitHub Codespace install Terraform. 
Copy the files from the course repo
[here](https://github.com/DataTalksClub/data-engineering-zoomcamp/tree/main/01-docker-terraform/1_terraform_gcp/terraform) to your VM/Laptop/GitHub Codespace.

Modify the files as necessary to create a GCP Bucket and Big Query Dataset.


## Question 7. Creating Resources

After updating the main.tf and variable.tf files run:

```
terraform apply
```

Paste the output of this command into the homework submission form.
```
google_bigquery_dataset.demo-dataset: Creating...
google_storage_bucket.demo-bucket: Creating...
google_bigquery_dataset.demo-dataset: Creation complete after 1s [id=projects/dez2024/datasets/demo_dataset]
google_storage_bucket.demo-bucket: Creation complete after 2s [id=dez2024-demo-bucket]
```

## Submitting the solutions

* Form for submitting: https://courses.datatalks.club/de-zoomcamp-2024/homework/hw01
* You can submit your homework multiple times. In this case, only the last submission will be used. 

Deadline: 29 January, 23:00 CET
