package com.qingjiao.core

import com.hankcs.hanlp.HanLP
import com.hankcs.hanlp.seg.common.Term
import org.apache.log4j.{Level, Logger}
import org.apache.spark.rdd.RDD
import org.apache.spark.storage.StorageLevel
import org.apache.spark.{SparkConf, SparkContext}

import java.util
import scala.io.Source

object SearchLogAnalysis {
  def main(args : Array[String]): Unit = {
    Logger.getLogger("org.apache.spark").setLevel(Level.ERROR)
    val conf = new SparkConf()
      .setAppName("SearchLogAnalysis")
      .setMaster("local[*]")
      .set("spark.driver.bindAddress","127.0.0.1")
    val sc = new SparkContext(conf)

    import scala.collection.JavaConverters._
    val file="E:\\root\\retrievelog\\SogouQ.reduced"
    val stopWordsFile="E:\\root\\retrievelog\\scu_stopwords.txt"

    val rdd = sc.textFile(file).filter(line => line!=null && line.trim.split("\\s+").length == 6)
    val stopWords = Source.fromFile(stopWordsFile).getLines().toSet
    val logBeanRDD = rdd.mapPartitions(it => {
      it.map(line => {
        val splits = line.trim.split("\\s+")
        val keyWords = splits(2).replaceAll("[\\[|\\]]","")
        LogBean(splits(0), splits(1), keyWords, splits(3).toInt, splits(4).toInt, splits(5))
      })
    })
    logBeanRDD.persist(StorageLevel.MEMORY_AND_DISK).count()

    // 用户uuid统计
    val uuidResult: RDD[(String, Int)] = logBeanRDD.mapPartitions(it => {
      it.map(bean => {
        (bean.userID, 1)
      })
    }).reduceByKey(_ + _).sortBy(_._2, false)
    uuidResult.coalesce(1).take(10).foreach(println)

    //URL访问量统计
    val urlResult: RDD[(String, Int)] = logBeanRDD.mapPartitions(it => {
      it.filter(bean => bean.clickUrl.substring(0, 3).equals("www"))
      .map(bean => {
        val Urls: Array[String] = bean.clickUrl.split("/")
        (Urls(0), 1)
      })
    }).reduceByKey(_ + _).sortBy(_._2, false)
    urlResult.coalesce(1).take(10).foreach(println)

    // 访问行为统计
    val actionResult: RDD[(Int, Int)] = logBeanRDD.mapPartitions(it => {
      it.map(bean => {
        (bean.clickRank, 1)
      })
    }).reduceByKey(_+_)
      .sortBy(f => f._2, false)
    actionResult.coalesce(1).take(10).foreach(println)

    // 搜索关键词的统计，统计数据集种搜索次数top10的关键词
    val keyWordsResult = logBeanRDD.mapPartitions(it => {
      it.flatMap(bean => {
        val words = HanLP.segment(bean.keyWords)
        words.asScala.filter(item=>{
          !stopWords.contains(item.word)
        })
          .map(item => {(item.word, 1)})
      })
    }).reduceByKey(_ + _)
      .sortBy(_._2, false)
      .coalesce(1)
    keyWordsResult.take(10).foreach(println)

    // 用户搜索点击统计，每个用户搜索的关键词次数Top10
    val userKeyWordsResult = logBeanRDD.mapPartitions(it => {
      it.flatMap(bean => {
        val words: util.List[Term] = HanLP.segment(bean.keyWords)
        words.asScala .filter(item => {
          !stopWords.contains(item.word)
        })
          .map(item => ((bean.userID, item.word), 1))
      })
    }).reduceByKey(_ + _)
      .sortBy(_._2,false)
    userKeyWordsResult.coalesce(1).take(10).foreach(println)

    // 搜索时间段统计，按小时统计用户访问量
    val timeResult = logBeanRDD.mapPartitions(it => {
      it.map(bean => {
        (bean.requestTime.substring(0,2),1)
      })
    }).reduceByKey(_ + _).sortBy(_._2, false)
    timeResult.coalesce(1).foreach(println)

    // resultRank ===clickRank / count(*)
    val bestResult = logBeanRDD.filter(bean => {
      bean.resultRank == bean.clickRank
    })
    val bestRatio = bestResult.count().toFloat / logBeanRDD.count()
    println(f"best ratio:${bestRatio*100}%.2f%%")

    logBeanRDD.unpersist()
    sc.stop()
  }
  // 数据封装样例类，便于后续调用
  case class LogBean(
                      requestTime: String,  // 时间
                      userID: String,     // 用户id
                      keyWords: String, // 关键词
                      resultRank: Int,    // 该URL在返回结果中的排名
                      clickRank: Int,     // 用户点击顺序号
                      clickUrl: String    // url
                    )
}
