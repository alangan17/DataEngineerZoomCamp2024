FROM python:3.9.1

RUN apt-get install wget
RUN pip install pandas sqlalchemy psycopg2 pyarrow

WORKDIR /app
COPY "10-Ingest_NY_Taxi_refactor.py" "10-Ingest_NY_Taxi_refactor.py"

ENTRYPOINT ["python", "10-Ingest_NY_Taxi_refactor.py"]