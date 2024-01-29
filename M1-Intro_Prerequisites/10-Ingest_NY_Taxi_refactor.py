import argparse
import pandas as pd
from sqlalchemy import create_engine
import pyarrow.parquet as pq
from time import time
import os


def ingest_parquet(engine, table: str, data_source: str, batch_size: int = 100000):
    # Define the path to your Parquet file
    parquet_file = data_source

    # Open the Parquet file
    parquet_table = pq.ParquetFile(parquet_file)

    print("Previewing the data schema:")
    df = parquet_table.read().to_pandas()
    print(pd.io.sql.get_schema(df, name=table, con=engine))

    # Truncate table
    df.head(0).to_sql(name=table, con=engine, if_exists="replace", index=False)

    # Iterate over batches and load into PostgreSQL
    print("Start ingesting data...")
    for batch in parquet_table.iter_batches(batch_size=batch_size):
        t_start = time()

        chunk = batch.to_pandas()
        chunk.to_sql(name=table, con=engine, if_exists="append", index=False)

        t_end = time()
        print(f"Loaded {len(chunk)} rows to '{table}' in {t_end - t_start} seconds.")


def ingest_csv(engine, table: str, data_source: str, batch_size: int = 100000):
    print("Previewing the data schema:")
    df_preview = pd.read_csv(data_source, nrows=1000)
    print(pd.io.sql.get_schema(df_preview, name=table, con=engine))

    # Truncate table
    df_preview.head(0).to_sql(name=table, con=engine, if_exists="replace", index=False)

    # Ingest csv by chunks
    print("Start ingesting data...")
    df_iter = pd.read_csv(
        data_source, iterator=True, chunksize=batch_size, low_memory=False
    )

    while True:
        try:
            t_start = time()

            df = next(df_iter)
            df.to_sql(name=table, con=engine, if_exists="append", index=False)

            t_end = time()
            print(f"Loaded {len(df)} rows to '{table}' in {t_end - t_start} seconds.")

        except StopIteration:
            # Exit the loop when no more data is available
            break


def main(params):
    user = params.user
    password = params.password
    host = params.host
    port = params.port
    database = params.database
    table = params.table
    data_source = params.data_source

    # Download file from url
    filename = data_source.split("/")[-1]
    os.system(f"wget {data_source} -O {filename}")

    data_source = f"{filename}"

    # # Setup DB engine
    # pip install sqlalchemy
    # pip install psycopg2

    connection_string = f"postgresql://{user}:{password}@{host}:{port}/{database}"

    engine = create_engine(connection_string)
    engine.connect()

    # If filename is `.parquet` file
    if data_source.endswith(".parquet"):
        ingest_parquet(engine, table, data_source)
    # If filename is `.csv`/ `.csv.gz` file
    elif any(ext in data_source for ext in [".csv", ".csv.gz"]):
        ingest_csv(engine, table, data_source)
    else:
        raise ValueError("File format not supported")

    # Close the engine connection
    engine.dispose()

    print(f"Data ingestion to '{table}' complete!")


if __name__ == "__main__":
    # Handle the command line arguments
    parser = argparse.ArgumentParser(
        description="Ingest the NYC Taxi Data into Postgres"
    )
    parser.add_argument("--user", type=str, help="Postgres user name", required=True)
    parser.add_argument("--password", type=str, help="Postgres password", required=True)
    parser.add_argument("--host", type=str, help="Postgres host", required=True)
    parser.add_argument("--port", type=int, help="Postgres port", required=True)
    parser.add_argument(
        "--database", type=str, help="Postgres database name", required=True
    )
    parser.add_argument("--table", type=str, help="Postgres table name", required=True)
    parser.add_argument(
        "--data_source", type=str, help="NYC Taxi data source", required=True
    )
    args = parser.parse_args()
    main(args)
