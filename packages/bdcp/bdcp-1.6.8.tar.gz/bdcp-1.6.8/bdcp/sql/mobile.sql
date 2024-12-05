package com.qingjiao.sql

import org.apache.spark.sql.types.{IntegerType, LongType}
import org.apache.spark.sql.{DataFrame, SaveMode, SparkSession}

object MobileAnalysis {
  def main(args: Array[String]): Unit = {
    val spark: SparkSession = new SparkSession.Builder()
      .appName("MobileAnalysis")
      .master("local[*]")
      .config("spark.driver.bindAddress", "127.0.0.1")
      .getOrCreate()

    import spark.implicits._

    val file = "E:\\root\\movie\\mobile.txt"
    val df: DataFrame = spark.read.format("csv")
      .option("header", "true")
      .option("inferSchema", "true")
      .csv(file)
      .toDF("brand", "mobile", "price", "sale", "ratio", "url")
      .withColumn("cost", $"price"*$"sale".cast(LongType))

    df.createOrReplaceTempView("mobiles")
    val result: DataFrame = spark.sql(
      """
        |select brand, sum(cost) as sum_cost, sum(sale) as sum_sale, cast(round(sum(ratio)/count(*)) as int) as avg_ratio
        |from mobiles group by brand
        |""".stripMargin)

    // MR输出格式 --> part-r-00000
    result.coalesce(1).write.mode(SaveMode.Overwrite)
      .format("csv")
      .option("header", "false")
      .option("sep", "\t")
      .save("E:\\workspace\\idea-workspace\\qingjiao_practice\\spark\\src\\main\\resources\\out")
  }
}
