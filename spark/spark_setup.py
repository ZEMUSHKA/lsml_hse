import os
import sys


def setup_pyspark_env(version="2.1.0"):
    if version == "2.1.0":
        os.environ["SPARK_HOME"] = "/usr/hdp/current/spark2.1"
        sys.path.insert(0, os.path.join(os.environ["SPARK_HOME"], 'python'))
        sys.path.insert(0, os.path.join(os.environ["SPARK_HOME"], 'python/lib/py4j-0.10.4-src.zip'))
    elif version == "1.6.2":
        os.environ["SPARK_HOME"] = "/usr/hdp/current/spark-client"
        sys.path.insert(0, os.path.join(os.environ["SPARK_HOME"], 'python'))
        sys.path.insert(0, os.path.join(os.environ["SPARK_HOME"], 'python/lib/py4j-0.9-src.zip'))
    else:
        raise Exception("Version not supported!")
