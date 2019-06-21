import datetime
import pyspark.sql.functions as f
from pyspark.sql import SparkSession


def date_to_str(dateval):
    return '-'.join([str(dateval.year), str(f'{dateval.month:02d}'), str(f'{dateval.day:02d}')])


# spark session
spark = SparkSession.builder.appName("HomePageDemographics").config("hive.exec.dynamic.partition.mode",
                                                                     "nonstrict").getOrCreate()


# date manipulation
current_date = datetime.datetime.now()
current_date_str = date_to_str(current_date)
timestamp = current_date.strftime("%Y%m%d%H%M%S")


##########################################################################################################
###################################### Number of Applies #################################################
##########################################################################################################


# get the respective dataframes
jobdid_carotene_df = spark.table('knowledgediscovery.jobcarotenev3')\
    .select(['jobdid', 'carotenetitleid']).where('sequence = 1')
jobdid_location_df = spark.table('sitedata.hhjob')\
    .select(['did', 'cityname', 'statename', 'countryname']).where("countryname = 'US' AND status = 0")\
    .withColumnRenamed('did', 'jobdid')
applies_df = spark.table('jobappl.jobapplication').join(jobdid_location_df, 'jobdid')


applies_count_df = applies_df.groupby('jobdid').count()


# join delta to get caroteneid and location
applies_carotene_location_df = applies_count_df.join(jobdid_carotene_df, 'jobdid')\
    .join(jobdid_location_df, 'jobdid')\
    .groupby('carotenetitleid', 'cityname', 'statename')\
    .agg(f.avg('count').alias('avg_carotene_location'))

applies_count_df\
    .join(jobdid_location_df, 'jobdid')\
    .join(jobdid_carotene_df, 'jobdid')\
    .join(applies_carotene_location_df, ['carotenetitleid', 'cityname','statename'])\
    .withColumn("score", (f.col('count') - f.col('avg_carotene_location'))/f.col('avg_carotene_location'))\
    .select(['jobdid', 'score'])\
    .withColumn("rundate", f.lit(current_date_str))\
    .createOrReplaceTempView("temp_job_score_df")

insert_sql_carotene_location = "INSERT OVERWRITE TABLE dataservices.homepage_demographics_job_score " \
                               "PARTITION(rundate) " \
                               "SELECT * FROM temp_job_score_df"
spark.sql(insert_sql_carotene_location)


