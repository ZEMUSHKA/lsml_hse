import pyspark


def get_spark_conf(parallelism, addPythonMemoryOverhead, nodesAlive,
                   executorsPerNode, memoryPerExecutor, additionalConf):
    executorInstances = nodesAlive * executorsPerNode - 1  # One for Application Master
    executorMemoryOverheadMb = 1024
    pythonMemoryOverheadMb = 0
    if addPythonMemoryOverhead:
        # python eats the same amount, add to overhead!
        pythonMemoryOverheadMb = int((memoryPerExecutor - executorMemoryOverheadMb) * 0.5)
    executorMemoryMb = memoryPerExecutor - executorMemoryOverheadMb - pythonMemoryOverheadMb
    conf = (
        pyspark.SparkConf()
        .set("spark.executor.memory", "{0}m".format(executorMemoryMb))
        .set("spark.driver.memory", "{0}m".format(executorMemoryMb))
        .set("spark.yarn.executor.memoryOverhead", executorMemoryOverheadMb + pythonMemoryOverheadMb)
        .set("spark.yarn.driver.memoryOverhead", executorMemoryOverheadMb + pythonMemoryOverheadMb)
        .set("spark.python.worker.memory", "{0}m".format(int(pythonMemoryOverheadMb * 0.6)))
        .set("spark.executor.instances", executorInstances)
        .set("spark.default.parallelism", parallelism)
    )
    for k, v in additionalConf.iteritems():
        conf = conf.set(k, v)
    return conf


def get_spark_context(master="yarn-client", appName="Jupyter Notebook",
                      parallelism=300, addPythonMemoryOverhead=True, nodesAlive=3,
                      executorsPerNode=4, memoryPerExecutor=6144, additionalConf={}):
    sc = pyspark.SparkContext(
        master=master,
        appName=appName,
        conf=get_spark_conf(parallelism, addPythonMemoryOverhead, nodesAlive,
                            executorsPerNode, memoryPerExecutor, additionalConf)
    )
    print "Ambari - http://10.0.1.21:8080"
    print "All Applications - http://10.0.1.23:8088/cluster"
    return sc
