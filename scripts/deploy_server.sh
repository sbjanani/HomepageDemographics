#!/bin/sh

cd Homepage-Demographics

hdfs dfs -mkdir -p oozie/workflow/homepage-demographics/python/
hdfs dfs -mkdir -p oozie/workflow/homepage-demographics/scripts/


hdfs dfs -put -f oozie/workflow/coordinator.xml oozie/workflow/homepage-demographics/
hdfs dfs -put -f oozie/workflow/workflow.xml oozie/workflow/homepage-demographics/
hdfs dfs -put -f python oozie/workflow/homepage-demographics/
