package com.luojiahan.mobile;

import com.luojiahan.utils.MyPropertiesUtil;
import org.apache.hadoop.conf.Configuration;
import org.apache.hadoop.fs.FileSystem;
import org.apache.hadoop.fs.Path;
import org.apache.hadoop.io.LongWritable;
import org.apache.hadoop.io.Text;
import org.apache.hadoop.mapreduce.Job;
import org.apache.hadoop.mapreduce.Mapper;
import org.apache.hadoop.mapreduce.Reducer;
import org.apache.hadoop.mapreduce.lib.input.FileInputFormat;
import org.apache.hadoop.mapreduce.lib.output.FileOutputFormat;
import org.apache.hadoop.util.GenericOptionsParser;

import java.io.IOException;
import java.util.Properties;

public class BrandAnalysis {
	/**
	 * 用户自定义Mapper继承自Mapper，重写map方法实现对应的逻辑
	 * 按行读取文件中的内容，将品牌作为key，一行内容作为value
	 * 用户自定义Reducer类继承自Reducer，重写reduce方法实现对key相同的数据进行聚合的处理
	 */
	public static class MyMapper extends Mapper<LongWritable, Text, Text, Text> {
		// 初始化key
		Text k=new Text();

		@Override
		public void map(LongWritable key, Text value, Mapper<LongWritable, Text, Text, Text>.Context context) throws IOException, InterruptedException {
			// 跳过第一行数据
			if (key.get()==0) {
				return;
			}

			// 读取一行数据:品牌,手机名称,价格,销量,好评率,购买链接
			String[] contents = value.toString().split(",");

			// 将品牌作为key，一行数据作为value
			k.set(contents[0]);

			// 通过上下文对象将数据写出
			context.write(k, value);
		}
	}
	public static class MyReducer extends Reducer<Text, Text, Text, Text> {
		// 初始化value
		Text v = new Text();

		@Override
		public void reduce(Text key, Iterable<Text> values, Reducer<Text, Text, Text, Text>.Context context) throws IOException, InterruptedException {
			// 对key相同的数据聚合处理，values中每个元素：品牌0,手机名称1,价格2,销量3,好评率4,购买链接5

			/**
			 * 手机总销售量；（同一品牌手机价格*销量）
			 * 总销售额；（同一品牌手机总销售额）
			 * 平均好评率。（同一品牌手机平均好评率=同一品牌手机总好评率/同一品牌手机总数，结果取整数）
			 */

			// 手机总销售量
			double sumSale=0.0;
			// 手机总销售额
			int sales=0;
			// 总好评率
			double sumPositive=0.0;

			for (Text value : values) {
				String[] contents = value.toString().split(",");
				sumSale += Double.parseDouble(contents[2]) * Double.parseDouble(contents[3]);

				sales+=Integer.parseInt(contents[3]);

				sumPositive+=Double.parseDouble(contents[4]);

			}

			// 平均好评率
			double avgPositive = sumPositive * 100 / sales;
			String avgPositiveRate = String.format("%.0f", avgPositive);
			String result=sales+"\t"+(long) sumSale+"\t"+avgPositiveRate+"\t"+sumPositive;
			v.set(result);
			context.write(key,v);
		}
	}
	public static void main(String[] args) throws IOException, InterruptedException, ClassNotFoundException {
		long startTime = System.currentTimeMillis();
		// 创建Configuration对象
		Configuration conf = new Configuration();

		// 对应于HDFS中文件所在的位置路径
		Properties prop = MyPropertiesUtil.load("config.properties");
		String hdfs = prop.getProperty("fs.defaultFS");

		// 设置客户端访问datanode使用hostname来进行访问
		conf.set("dfs.client.use.datanode.hostname", "true");
		conf.set("fs.defaultFS", hdfs);
		// Hadoop3 No FileSystem for scheme "hdfs"
		conf.set("fs.hdfs.impl", "org.apache.hadoop.hdfs.DistributedFileSystem");
		conf.set("fs.file.impl", "org.apache.hadoop.fs.LocalFileSystem");
		System.setProperty("HADOOP_USER_NAME", "root");

		// 获取文件对象
		FileSystem fs = FileSystem.get(conf);

		// 创建Job对象
		Job job = Job.getInstance(conf);

		// 设置jar路径
		job.setJarByClass(BrandAnalysis.class);

		// 设置mapper和reducer类
		job.setMapperClass(MyMapper.class);
		job.setReducerClass(MyReducer.class);

		// 设置map输出的kv数据类型
		job.setMapOutputKeyClass(Text.class);
		job.setMapOutputValueClass(Text.class);

		// 设置最终输出的kv的数据类型
		job.setOutputKeyClass(Text.class);
		job.setOutputValueClass(Text.class);

		// 方法一：自定义输入路径
		String[] otherArgs = new GenericOptionsParser(conf, args).getRemainingArgs();
		if (otherArgs.length != 0) {
			// 方法一：自定义输入路径
			for (int i = 0; i < otherArgs.length - 1; ++i) {
				FileInputFormat.addInputPath(job, new Path(otherArgs[i]));
			}
			if (fs.exists(new Path(otherArgs[otherArgs.length - 1]))) {
				// 存在，删除
				fs.delete(new Path(otherArgs[otherArgs.length - 1]), true);
			}
			FileOutputFormat.setOutputPath(job,
					new Path(otherArgs[otherArgs.length - 1]));
		} else {
			// 方法二：输入和输出目录
			String input_path = hdfs + "/mobile.txt";
			String output_path = hdfs + "/mobile/";
			Path input = new Path(input_path);
			Path output = new Path(output_path);

			// 判读输出目录是否存在
			if (fs.exists(output)) {
				// 存在，删除
				fs.delete(output,true);
			}

			// 设置输入和输出目录
			FileInputFormat.setInputPaths(job, input);
			FileOutputFormat.setOutputPath(job, output);
		}

		long endTime = System.currentTimeMillis();
		long executionTime = endTime - startTime;
		//System.out.println("用时: " + executionTime / 1000  + "s");
		System.out.println("mkdir /root/data/mobile");
		System.out.println("hdfs dfs -get /mobile/part-r-00000 /root/data/mobile");

		// 提交job
		System.exit(job.waitForCompletion(true)?0:-1);
	}
}