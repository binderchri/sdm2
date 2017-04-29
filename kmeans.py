# Parts of this code are taken from:
# https://spark.apache.org/docs/2.1.0/mllib-clustering.html#k-means

from pyspark import SparkContext, SparkConf
from pyspark.mllib.clustering import KMeans, KMeansModel
from numpy import array
from math import sqrt
from time import time

conf = SparkConf()
sc = SparkContext()

# path to data file
file = "/home/binderchri/kddcup1999/kddcup.data.cleaned"

# path to file to write statistics into
outputfilepath = "/home/binderchri/kddcup1999/out.txt"


data = sc.textFile(file)
parsedData = data.map(lambda line: array([float(x) for x in line.split(',')]))

ks = [1,2,3,4,5,8,13,20,50] # for k estimation (elbow method)
# ks = [1,3,5,10,50] # for performance measurement (comment-in)

for k in ks:
    startTime = time()

    epsilon = 1e-6

    clusters = KMeans.train(parsedData,
                            k=k,
                            epsilon=epsilon,
                            maxIterations=1000,
                            seed=99
                           )

    elapsed = time() - startTime # seconds

    # Evaluate clustering by computing Within Set Sum of Squared Errors
    def error(point):
        center = clusters.centers[clusters.predict(point)]
        return sqrt(sum([x**2 for x in (point - center)]))

    WSSSE = 0
    # for performance measurement comment-out error estimation (very time consuming step)
    WSSSE = parsedData.map(lambda point: error(point)).reduce(lambda x, y: x + y)

    output = "k={}, error={}, duration={} seconds, epsilon={}".format(k, WSSSE, elapsed, epsilon)

    with open(outputfilepath, "a") as f:
        print(output, file=f)

sc.stop()
