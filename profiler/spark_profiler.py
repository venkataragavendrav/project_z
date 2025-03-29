from pyspark.sql import SparkSession
from pyspark.sql.functions import col, countDistinct, count, when

def spark_session():
    return SparkSession.builder \
        .appName("ProjectZProfiler") \
        .getOrCreate()

def profile_table(table_df):
    profile = []
    total_count = table_df.count()

    for col_name in table_df.columns:
        col_data = table_df.select(col(col_name))
        null_count = col_data.filter(col(col_name).isNull()).count()
        distinct_count = col_data.agg(countDistinct(col(col_name))).collect()[0][0]
        duplicate_count = total_count - distinct_count

        result = {
            "column": col_name,
            "null_percentage": (null_count / total_count) * 100,
            "distinct_count": distinct_count,
            "duplicate_count": duplicate_count,
            "min_value": col_data.agg({col_name: "min"}).collect()[0][0],
            "max_value": col_data.agg({col_name: "max"}).collect()[0][0]
        }
        profile.append(result)
    return profile

if __name__ == "__main__":
    spark = spark_session()
    df = spark.read.format("csv").option("header", "true").load("your_data.csv")
    print(profile_table(df))
