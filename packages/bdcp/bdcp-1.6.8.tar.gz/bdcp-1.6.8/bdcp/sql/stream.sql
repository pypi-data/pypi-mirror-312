package com.qingjiao.streaming

import org.apache.log4j.{Level, Logger}
import org.apache.spark.sql.{SaveMode, SparkSession}
import org.apache.spark.sql.functions.get_json_object
import org.apache.spark.sql.streaming.{OutputMode, Trigger}

object AdsAnalysisDF {
  def main(args: Array[String]): Unit = {
    Logger.getLogger("org.apache").setLevel(Level.ERROR)
    val spark = SparkSession.builder()
      .appName("AdsAnalysisDF")
      .master("local[*]")
      .config("spark.driver.bindAddress", "127.0.0.1")
      .getOrCreate()

    import spark.implicits._

    val kafkaDF = spark.readStream
      .format("kafka")
      .option("kafka.bootstrap.servers", "bigdata:9092")
      .option("subscribe", "ads")
      .load()

    val areaCityCount = kafkaDF.selectExpr("CAST(value AS STRING)").as[String]
      .select(
        get_json_object($"value", "$.area").as("area"),
        get_json_object($"value", "$.city").as("city")
      ).groupBy($"area", $"city").count()

    val dbParams = Map(
      "url" -> "jdbc:mysql://bigdata:3306/ads?useSSL=false&&allowPublicKeyRetrieval=true&&characterEncoding=utf-8",
      "driver" -> "com.mysql.jdbc.Driver",
      "user" -> "root",
      "password" -> "123456",
      "dbtable" -> "area_city"
    )
    areaCityCount.writeStream
      .outputMode(OutputMode.Update())
      .foreachBatch((df, batchId) => {
        if (!df.isEmpty){
          df.coalesce(1)
            .write
            .mode(SaveMode.Overwrite)
            .format("jdbc")
            .options(dbParams)
            .save()
        }
      }).start().awaitTermination()

//    areaCityCount.writeStream
//      .format("console")
//      .outputMode(OutputMode.Update())
//      .option("truncate", false)
//      .start()
//      .awaitTermination()

  }

}
