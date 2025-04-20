import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from pyspark.sql import SparkSession
from pyspark.sql.functions import col, countDistinct, count
from pyspark.sql.types import NumericType

from dotenv import load_dotenv

import psycopg2
import uuid

from backend.service.profile_service import insert_into_data_profile
from backend.service.schema_service import insert_schema_snapshot
from backend.service.alert_service import insert_alert, send_slack_alert
from backend.config import DB_CONFIG
from schema_checker import *

def spark_session():
    jar_path = os.path.abspath("lib/postgresql-42.7.5.jar")
    return SparkSession.builder \
        .appName("ProjectZProfiler") \
        .config("spark.jars", jar_path) \
        .getOrCreate()

def profile_table(table_df):
    total_count = table_df.count()
    profile = []

    for field in table_df.schema.fields:
        col_name = field.name
        col_type = field.dataType

        col_data = table_df.select(col(col_name))
        null_count = col_data.filter(col(col_name).isNull()).count()
        distinct_count = col_data.agg(countDistinct(col(col_name))).collect()[0][0]
        duplicate_count = total_count - distinct_count

        min_value = None
        max_value = None

        if isinstance(col_type, NumericType):
            min_value = col_data.agg({col_name: "min"}).collect()[0][0]
            max_value = col_data.agg({col_name: "max"}).collect()[0][0]

        result = {
            "column_name": col_name,
            "null_percentage": round((null_count / total_count) * 100, 2),
            "distinct_count": distinct_count,
            "duplicate_count": duplicate_count,
            "min_value": min_value,
            "max_value": max_value,
            "data_type": str(col_type)
        }
        profile.append(result)

    return profile


def read_postgres_table(spark, table_name):
    jdbc_url = f"jdbc:postgresql://{DB_CONFIG['POSTGRES_HOST']}:{DB_CONFIG['POSTGRES_PORT']}/{DB_CONFIG['POSTGRES_DB']}"

    if not all([DB_CONFIG['POSTGRES_USER'], DB_CONFIG['POSTGRES_PASSWORD'], jdbc_url, table_name]):
        raise ValueError("Missing DB credentials or table name")

    df = spark.read \
        .format("jdbc") \
        .option("url", jdbc_url) \
        .option("dbtable", table_name) \
        .option("user", DB_CONFIG['POSTGRES_USER']) \
        .option("password", DB_CONFIG['POSTGRES_PASSWORD']) \
        .option("driver", "org.postgresql.Driver") \
        .load()
    return df


if __name__ == "__main__":
    spark = spark_session()

    #--- CASE 1: Profile CSV file ---
    # df = spark.read.format("csv").option("header", "true").load("your_data.csv")
    # datasource = "csv"
    # table_name = "your_data.csv"

    # --- CASE 2: Profile PostgreSQL Table ---
    db_host = os.getenv("DB_HOST")
    db_port = os.getenv("DB_PORT")
    db_name = os.getenv("DB_NAME")
    user = os.getenv("DB_USER")
    password = os.getenv("DB_PASSWORD")
    table_name = os.getenv("TARGET_TABLE")

    jdbc_url = f"jdbc:postgresql://{db_host}:{db_port}/{db_name}"

    df = read_postgres_table(spark,table_name)
    datasource = "postgresql"

    run_id = str(uuid.uuid4())

    profiles = profile_table(df)

    insert_into_data_profile(profiles, run_id, datasource, table_name)

    current_schema = get_schema_snapshot(df)
    previous_schema = fetch_latest_schema_snapshot(datasource, table_name)

    drift_info = detect_schema_drift(current_schema, previous_schema or {})

    change_detected = any(drift_info.values())

    insert_schema_snapshot(current_schema, datasource, table_name, change_detected)

    insert_alert(
        alert_type="schema_change",
        description="Detected schema drift in 'customers' table: ['email' column type changed]",
        severity="warning",
        run_id=run_id
    )

    slack_webhook_url = "https://hooks.slack.com/services/your/webhook/url"

    send_slack_alert(
        message="⚠️ Schema drift detected in `customers` table. Check the dashboard or logs for details.",
        webhook_url=slack_webhook_url
    )
