package com.qingjiao.sql

import org.apache.spark.sql.expressions.Window
import org.apache.spark.sql.functions._
import org.apache.spark.sql.{DataFrame, Dataset, Row, SaveMode, SparkSession}

object MovieAnalysis {
  private def saveDF(df: DataFrame, table: String): Unit = {
    val dbParams = Map(
      "url" -> "jdbc:mysql://localhost:3306/movie?characterEncoding=utf-8&&useSSL=false&&allowPublicKeyRetrieval=true",
      //"driver" -> "com.mysql.cj.jdbc.Driver",
      "driver" -> "com.mysql.jdbc.Driver",
      "user" -> "root",
      "password" -> "199037wW",
      "dbtable" -> table
    )
    df.write.format("jdbc")
      .options(dbParams)
      .mode(SaveMode.Append)
      .save()
    println("save df to table!")
  }
  def main(args: Array[String]): Unit = {
    val spark: SparkSession = SparkSession.builder()
      .appName("MovieAnalysis")
      .master("local[*]")
      .config("spark.driver.bindAddress", "127.0.0.1")
      .getOrCreate()

    import spark.implicits._

    val file="E:\\root\\movie\\movie_dataset.csv"
    val df: DataFrame = spark.read.option("header", "true")
      .csv(file).toDF("IMDb", "movieName", "actor", "score", "level", "grossed", "releaseTime")
    //df.show(5)

    df.createOrReplaceTempView("movie")

    // 不同等级(范围)电影的数量
    val levelCountDSL: Dataset[Row] = df.groupBy("level").count().orderBy($"count".desc)
    val levelCountSQL: DataFrame = spark.sql(
      """
        |select level, count(*) as movie_count from movie
        |group by level order by movie_count desc
        |""".stripMargin
    )
    //levelCountDSL.show()
    //levelCountSQL.show()

    // 不同评分(范围)电影的数量
    //df.printSchema()
    val scoreCountDSL: Dataset[Row] = df.withColumn("scoreRange", concat_ws("-", floor($"score"), ceil($"score")))
      .groupBy("scoreRange")
      .count().orderBy($"scoreRange".desc)
    val scoreCountSQL: DataFrame = spark.sql(
      """
        |select concat_ws('-', floor(score), ceil(score)) as score_range, count(*) as movie_count
        |from movie group by concat_ws('-', floor(score), ceil(score))
        |order by score_range
        |""".stripMargin
    )
    //scoreCountDSL.show()
    //scoreCountSQL.show()

    // 按照上映年统计总票房和上映的电影数量
    val grossedDSL: Dataset[Row] = df.withColumn("releaseYear", substring($"releaseTime", 0, 4))
      .groupBy("releaseYear")
      .agg(
        count("releaseYear") as "movieCount",
        sum("grossed") as "sumGrossed"
      ).orderBy("releaseYear")
    val grossedSQL: DataFrame = spark.sql(
      """
        |select substring(releaseTime, 0, 4) as release_year, count(*) as movie_count, sum(grossed) as sum_grossed
        |from movie group by substring(releaseTime, 0, 4) order by release_year
        |""".stripMargin
    )
    //grossedDSL.show()
    //grossedSQL.show()

    // 统计每年上映的总票房Top3的电影
    val grossedRankDSL: Dataset[Row] = df.withColumn("releaseYear", substring($"releaseTime", 0, 4))
      .withColumn("grossedRank", rank().over(Window.partitionBy("releaseYear").orderBy($"grossed".desc)))
      .filter($"grossedRank" <= 3)
    val grossedRankSQL: DataFrame = spark.sql(
      """
        |select * from
        |(select *, substring(releaseTime,0,4) as release_year, rank() over(partition by substring(releaseTime,0,4) order by grossed desc) as grossed_rank
        |from movie) as tmp
        |where grossed_rank<=3
        |""".stripMargin
    )
    //grossedRankDSL.show()
    //grossedRankSQL.show()

    saveDF(levelCountSQL, "level_count")
    saveDF(scoreCountSQL, "score_count")
    saveDF(grossedSQL, "grossed")
    saveDF(grossedRankSQL, "grossed_rank")
    spark.stop()
  }

}
