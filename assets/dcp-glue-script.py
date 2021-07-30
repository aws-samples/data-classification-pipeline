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
## @type: DataSource
## @args: [database = "dcp", table_name = "dcp_glue_landing_us_east_1_ACCOUNT_ID", transformation_ctx = "datasource0"]
## @return: datasource0
## @inputs: []
datasource0 = glueContext.create_dynamic_frame.from_catalog(database = "dcp", table_name = "dcp_glue_landing_us_east_1_ACCOUNT_ID", transformation_ctx = "datasource0")
## @type: ApplyMapping
## @args: [mapping = [("version", "string", "version", "string"), ("id", "string", "id", "string"), ("detail-type", "string", "detail-type", "string"), ("source", "string", "source", "string"), ("account", "string", "account", "string"), ("time", "string", "time", "string"), ("region", "string", "region", "string"), ("resources", "array", "resources", "array"), ("detail", "struct", "detail", "struct"), ("partition_0", "string", "partition_0", "string"), ("partition_1", "string", "partition_1", "string"), ("partition_2", "string", "partition_2", "string"), ("partition_3", "string", "partition_3", "string")], transformation_ctx = "applymapping1"]
## @return: applymapping1
## @inputs: [frame = datasource0]
applymapping1 = ApplyMapping.apply(frame = datasource0, mappings = [("version", "string", "version", "string"), ("id", "string", "id", "string"), ("detail-type", "string", "detail-type", "string"), ("source", "string", "source", "string"), ("account", "string", "account", "string"), ("time", "string", "time", "string"), ("region", "string", "region", "string"), ("resources", "array", "resources", "array"), ("detail", "struct", "detail", "struct"), ("partition_0", "string", "partition_0", "string"), ("partition_1", "string", "partition_1", "string"), ("partition_2", "string", "partition_2", "string"), ("partition_3", "string", "partition_3", "string")], transformation_ctx = "applymapping1")
## @type: DataSink
## @args: [connection_type = "s3", connection_options = {"path": "s3://GLUE_CURATED_BUCKET"}, format = "parquet", transformation_ctx = "datasink2"]
## @return: datasink2
## @inputs: [frame = applymapping1]
datasink2 = glueContext.write_dynamic_frame.from_options(frame = applymapping1, connection_type = "s3", connection_options = {"path": "s3://GLUE_CURATED_BUCKET"}, format = "parquet", transformation_ctx = "datasink2")
job.commit()