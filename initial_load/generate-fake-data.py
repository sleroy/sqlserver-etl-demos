import sys
from awsglue.transforms import *
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from awsglue.job import Job
from pyspark.sql.types import StructType, StructField, BooleanType, BinaryType, IntegerType, StringType


sc = SparkContext.getOrCreate()
glueContext = GlueContext(sc)
spark = glueContext.spark_session
job = Job(glueContext)
import logging
logger = logging.getLogger(__name__)
logger.info("Schema creation")

#Defining the schema of the dataframe.
schema = StructType([
    StructField("CustSurr", BinaryType(), False),
    StructField("IpId", StringType(), False),
    StructField("CustIntId", StringType(), False),
    StructField("LoadStatusId", IntegerType(), False),
    StructField("CustSurrInt", IntegerType(), False),
    StructField("IsAnonymized", BooleanType(), False),    
])



from faker import Faker
from faker.providers import internet
from pyspark.sql import Row
import os
import struct
fake = Faker()
fake.add_provider(internet)

max_rows = 47000000
number_occ = 1000000


    # 47000000
logger.info("Creation of the fake data %d occurences", number_occ)
vals = []
for i in range(0, number_occ):
     # Generate a random byte sequence
    byte_sequence = os.urandom(16)

    # Convert the byte sequence to a format suitable for PySpark
    byte_sequence_hex = byte_sequence.hex()
    byte_sequence_struct = struct.pack('16s', byte_sequence)
    ar = (byte_sequence_struct, fake.ipv4_private(), fake.md5(), fake.pyint(), fake.pyint(),  fake.pybool() )
    vals.append(ar) 
logger.info("Data generated")


print("Begin")

maxTrials=round(max_rows/ number_occ) + 1
for trial in range(0, maxTrials):

    logger.info("Sending thefake data %d/%d", trial, maxTrials)
    logger.info("Data Creation of the dataframe")

    fake_table = spark.createDataFrame(vals, schema)

    logger.info("Creation of the dynamic frame")
    df = fake_table.toDF('CustSurr', 'IpId', 'CustIntId', 'LoadStatusId', 'CustSurrInt', 'IsAnonymized')

    logger.info("Data generated")
    from awsglue.dynamicframe import DynamicFrame
    dynamic_frame_write = DynamicFrame.fromDF(fake_table, glueContext, "dynamic_frame_write")
    #logger.info("Write in S3")
    #glueContext.write_dynamic_frame.from_options(
    #    frame = df    
    #    connection_type = "s3",
    #    format="parquet",
    #    connection_options = {
    #        "useGlueParquetWriter": True,
    #        "path": "s3://ml-bucket-131313/danske/parquet"
    #    }
    #)
    logger.info("Write in SQL Server")
    # Script generated for node Microsoft SQL Server        
    glueContext.write_dynamic_frame.from_jdbc_conf(dynamic_frame_write, "sqljdbc", connection_options={"dbtable": "large_table", "database": "wine"})
    logger.info("Write finished")

job.commit()