import pyspark


def get_spark_conf(CORES_PER_EXECUTOR=1, NODES_ALIVE=3):
    # optimal EXECUTOR_CORES is factor of 4, spark.executor.instances is ignored if > 1
    EXECUTOR_INSTANCES = int(NODES_ALIVE * 4 / CORES_PER_EXECUTOR) - 1  # One for Application Master
    EXECUTOR_MEMORY_MB = 6144 * CORES_PER_EXECUTOR - max(384, int(6144 * CORES_PER_EXECUTOR * 0.10) + 1)
    SPARK_PARALLELISM = EXECUTOR_INSTANCES * CORES_PER_EXECUTOR
    if SPARK_PARALLELISM < 100:
        SPARK_PARALLELISM = 100
    conf = pyspark.SparkConf() \
        .set("spark.executor.cores", CORES_PER_EXECUTOR) \
        .set("spark.executor.memory", "{0}m".format(EXECUTOR_MEMORY_MB)) \
        .set("spark.executor.instances", EXECUTOR_INSTANCES) \
        .set("spark.default.parallelism", SPARK_PARALLELISM)
    return conf


def get_spark_context(master="yarn-client", appName="Jupyter Notebook", CORES_PER_EXECUTOR=1, NODES_ALIVE=3):
    sc = pyspark.SparkContext(
        master=master,
        appName=appName,
        conf=get_spark_conf(CORES_PER_EXECUTOR, NODES_ALIVE)
    )
    print "Ambari - http://10.0.1.21:8080"
    print "All Applications - http://10.0.1.23:8088/cluster"
    return sc
