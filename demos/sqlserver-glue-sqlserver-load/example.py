import sys
from awsglue.transforms import *
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from awsglue.job import Job

## @params: [JOB_NAME]
args = getResolvedOptions(sys.argv, ['JOB_NAME'])

sc = SparkContext()
glueContext = GlueContext(sc)
spark = glueContext.spark_session
job = Job(glueContext)
job.init(args['JOB_NAME'], args)

## Read Data from a RDS DB using JDBC driver
connection_options = {
    "useConnectionProperties": "true",
    "dbtable": "new_table",
    "connectionName": "source-sqlserver",
}
source_df = glueContext.create_dynamic_frame.from_options(
    connection_type = "sqlserver",
    connection_options = connection_options
)

source_df.printSchema()
print("Count: ", source_df.count())
df = source_df.toDF()
df.show()
# Script generated for node Microsoft SQL Server
glueContext.write_dynamic_frame.from_jdbc_conf(source_df, 
 catalog_connection = "target-rds-sqlserver",
connection_options={"dbtable": "replicated", "database": "example"})

job.commit()
