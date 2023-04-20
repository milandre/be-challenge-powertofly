import os
import time

from faker import Faker
from flask_sqlalchemy import SQLAlchemy
from pyspark.sql import SparkSession
from pyspark.sql.types import IntegerType, StringType, StructField, StructType, TimestampType
from sqlalchemy_utils import Timestamp

# Setting database object
db = SQLAlchemy()

# Setting database and spark information
basedir = os.path.abspath(os.path.join(__file__, '../../..'))
database_info = os.getenv('DATABASE_URL').split('@') or 'sqlite:///' + os.path.join(basedir, 'db.sqlite')
jdbc_database_url = f"jdbc:postgresql://{database_info[1] if len(database_info) > 0 else database_info[0]}"
database_user = database_info[0].split("//")[1].split(":")[0] if len(database_info) > 0 else "admin"
database_password = database_info[0].split("//")[1].split(":")[1] if len(database_info) > 0 else "example"
spark_classpath = os.getenv('SPARK_CLASSPATH')


class User(db.Model, Timestamp):
    """User model

    Fields:
        id (int): User model primary key.
        email (str): User email, unique and indexed.
        first_name (str): User first name.
        last_name (str): User last name.
    """

    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(64), unique=True, index=True)
    first_name = db.Column(db.String(64), nullable=False)
    last_name = db.Column(db.String(64), nullable=False)

    def full_name(self):
        return f'{self.first_name} {self.last_name}'

    @staticmethod
    def insert_fake_users_into_db(count: int = 10, max_rows_per_transaction: int = 100000, **kwargs) -> None:
        fake = Faker()
        users_per_partition = max_rows_per_transaction
        num_partitions = count // max_rows_per_transaction

        # Define schema
        schema = StructType(
            [
                StructField("id", IntegerType(), False),
                StructField("email", StringType(), False),
                StructField("first_name", StringType(), False),
                StructField("last_name", StringType(), False),
                StructField("created", TimestampType(), False),
                StructField("updated", TimestampType(), False),
            ]
        )

        # Initialize SparkSession
        spark = (
            SparkSession.builder.appName("Bulk Insert Dummy Users")
            .config("spark.driver.extraClassPath", spark_classpath)
            .config("spark.executor.extraClassPath", spark_classpath)
            .getOrCreate()
        )

        # Create PySpark DataFrame in parallel
        rdd = spark.sparkContext.parallelize(range(num_partitions), num_partitions)
        df = rdd.flatMap(
            lambda x: [
                (
                    id + x * users_per_partition,
                    f"user{id + x*users_per_partition}@{fake.domain_name()}",
                    fake.first_name(),
                    fake.last_name(),
                    fake.date_time(),
                    fake.date_time(),
                )
                for id in range(users_per_partition)
            ]
        ).toDF(schema)

        start_time = time.time()
        df.write.mode("overwrite").jdbc(
            jdbc_database_url,
            "users",
            properties={"user": database_user, "password": database_password, "driver": "org.postgresql.Driver"},
        )

        duration = time.time() - start_time
        print(f"Spark insertions time: {duration:.2f} seconds.")

        # Stop SparkSession
        spark.stop()

    def __repr__(self):
        return '<User \'%s\'>' % self.full_name()
