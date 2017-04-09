import pyspark


def get_spark_conf(parallelism, addPythonMemoryOverhead, nodesAlive,
                   executorsPerNode, memoryPerExecutor):
    executorInstances = nodesAlive * executorsPerNode - 1  # One for Application Master
    executorMemoryOverheadMb = max(384, int(memoryPerExecutor * 0.10) + 1)  # default Spark behavior
    if addPythonMemoryOverhead:
        # python eats the same amount, add to overhead!
        executorMemoryOverheadMb = int(memoryPerExecutor * 0.5)
    executorMemoryMb = memoryPerExecutor - executorMemoryOverheadMb
    conf = (
        pyspark.SparkConf()
        .set("spark.executor.memory", "{0}m".format(executorMemoryMb))
        .set("spark.driver.memory", "{0}m".format(executorMemoryMb))
        .set("spark.yarn.executor.memoryOverhead", executorMemoryOverheadMb)
        .set("spark.yarn.driver.memoryOverhead", executorMemoryOverheadMb)
        .set("spark.python.worker.memory", executorMemoryOverheadMb * 0.8)  # 10 % of memory is for other stuff
        .set("spark.executor.instances", executorInstances)
        .set("spark.default.parallelism", parallelism)
    )
    return conf


def get_spark_context(master="yarn-client", appName="Jupyter Notebook",
                      parallelism=300, addPythonMemoryOverhead=True, nodesAlive=3,
                      executorsPerNode=4, memoryPerExecutor=6144):
    sc = pyspark.SparkContext(
        master=master,
        appName=appName,
        conf=get_spark_conf(parallelism, addPythonMemoryOverhead, nodesAlive, executorsPerNode, memoryPerExecutor)
    )
    print "Ambari - http://10.0.1.21:8080"
    print "All Applications - http://10.0.1.23:8088/cluster"
    return sc
