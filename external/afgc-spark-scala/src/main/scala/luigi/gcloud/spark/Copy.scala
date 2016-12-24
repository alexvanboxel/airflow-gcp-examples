package luigi.gcloud.spark

import org.apache.spark.{SparkConf, SparkContext}

object Copy {

  def main(args: Array[String]) {
    val sparkConf = new SparkConf().setAppName("DataProcSpark")

    if (args.length != 2) {
      throw new scala.RuntimeException("args.length = " + args.length)
    }

    val in = args(0)
    val out = args(1)

    val sc = new SparkContext(sparkConf)

    val data = sc.textFile(in)
    data.saveAsTextFile(out)

  }
}
