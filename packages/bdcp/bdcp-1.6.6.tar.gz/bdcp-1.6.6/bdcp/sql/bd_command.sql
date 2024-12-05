/*
 Navicat MySQL Data Transfer

 Source Server         : hadoop111
 Source Server Type    : MySQL
 Source Server Version : 50744 (5.7.44)
 Source Host           : 124.70.110.14:3306
 Source Schema         : hongya

 Target Server Type    : MySQL
 Target Server Version : 50744 (5.7.44)
 File Encoding         : 65001

 Date: 22/11/2024 23:17:30
*/

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for bd_command
-- ----------------------------
DROP TABLE IF EXISTS `bd_command`;
CREATE TABLE `bd_command`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `type` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '命令类型',
  `title` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '命令描述',
  `command` text CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL COMMENT '命令示例',
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 57 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of bd_command
-- ----------------------------
INSERT INTO `bd_command` VALUES (1, '文本分类', '读取文件，将第一列设置为索引', 'df = pd.read_csv(\'text2cls.csv\', index_col=0)');
INSERT INTO `bd_command` VALUES (2, 'pandas', '检查缺失值', 'df.isnull().sum()');
INSERT INTO `bd_command` VALUES (3, 'pandas', '检查重复值', 'df.duplicated().sum()');
INSERT INTO `bd_command` VALUES (4, 'pandas', '查看各类别的数量', 'df[\'label\'].value_counts()');
INSERT INTO `bd_command` VALUES (5, 'jieba', 'jieba分词器进行精确模式分词 ', 'word_list = jieba.cut(sentence)');
INSERT INTO `bd_command` VALUES (6, 'sklearn', '分割数据集', 'train_test_split(df[\'cut_text\'], df[\'label\'], test_size=0.3, random_state=42)');
INSERT INTO `bd_command` VALUES (7, 'pandas', '独热编码', 'y_train = pd.get_dummies(y_train).values');
INSERT INTO `bd_command` VALUES (8, '文本分类', '训练文本', 'tokenizer.fit_on_texts(x_train)');
INSERT INTO `bd_command` VALUES (9, '文本分类', '文本转为序列', 'train_seq = tokenizer.texts_to_sequences(x_train)');
INSERT INTO `bd_command` VALUES (10, '文本分类', '截断补齐', 'train_padding = pad_sequences(train_seq, padding=\'post\', maxlen=50) # 序列长度设置为50');
INSERT INTO `bd_command` VALUES (11, 'keras', '搭建神经网络LSTM层', 'model.add(LSTM(64, return_sequences=True)) # LSTM层');
INSERT INTO `bd_command` VALUES (12, 'keras', '1维卷积', 'model.add(Convolution1D(32, 5, padding=\'same\', strides=1, activation=\'relu\')) # 1维卷积，进行补0操作，激活函数设置为relu');
INSERT INTO `bd_command` VALUES (13, 'keras', '1维最大池化', 'model.add(MaxPool1D(pool_size=3)) # 1维最大池化');
INSERT INTO `bd_command` VALUES (14, 'keras', '平铺层', 'model.add(Flatten()) # 平铺层');
INSERT INTO `bd_command` VALUES (15, 'keras', '全连接层', 'model.add(Dense(64, activation=\'relu\')) # 全连接层，激活函数设置为relu');
INSERT INTO `bd_command` VALUES (16, 'keras', '丢弃神经元', 'model.add(Dropout(0.3)) # 丢弃30%神经元');
INSERT INTO `bd_command` VALUES (17, 'keras', '神经网络2分类设置', 'model.add(Dense(2, activation=\'softmax\')) # 2分类，激活函数设置为softmax');
INSERT INTO `bd_command` VALUES (18, 'keras', '损失函数使用多分类交叉熵compile', 'model.compile(optimizer=adam_v2.Adam(1e-5), # # 优化器为Adam，学习率设置为1e-5\r\n              loss=\'categorical_crossentropy\',  # 损失函数使用多分类交叉熵\r\n              metrics=[\"accuracy\"] # 用准确率做评估\r\n             )');
INSERT INTO `bd_command` VALUES (19, 'keras', 'EarlyStopping三个参数', 'earlyStop = EarlyStopping(monitor=\'val_accuracy\', # 检测指标为val_accuracy\r\n                          min_delta=0.01, # 最小提升度0.01 \r\n                          patience=10, # 训练轮次10次\r\n                          mode=\'max\', # 被检测数据停止上升\r\n                          verbose=1, # 精确模式\r\n                         )');
INSERT INTO `bd_command` VALUES (20, 'keras', '训练模型', 'history = model.fit(train_padding, #训练集\r\n                    y_train, #标签\r\n                    epochs=100 , #训练轮数\r\n                    batch_size=16, #每次训练抽取样本数\r\n                    callbacks = [earlyStop], # 设置提前停止\r\n                    validation_data=(test_padding,y_test), # 测试集\r\n                    shuffle=True,\r\n                   )');
INSERT INTO `bd_command` VALUES (21, 'keras', '训练集准确率', 'acc = history.history[\'accuracy\']');
INSERT INTO `bd_command` VALUES (22, 'keras', '测试集准确率', 'val_acc = history.history[\'val_accuracy\']');
INSERT INTO `bd_command` VALUES (23, 'keras', '训练集损失', 'loss = history.history[\'loss\']');
INSERT INTO `bd_command` VALUES (24, 'keras', '测试集损失', 'val_loss = history.history[\'val_loss\'] # 测试集损失');
INSERT INTO `bd_command` VALUES (25, 'plot', '多子图', 'fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 5)) # 多子图');
INSERT INTO `bd_command` VALUES (26, 'keras', '测试集评估', 'model.evaluate(test_padding,y_test) # 对测试集评估');
INSERT INTO `bd_command` VALUES (27, 'keras', '预测测试集标签', 'predict = model.predict(test_padding) # 预测测试集标签');
INSERT INTO `bd_command` VALUES (28, 'pandas', '按行求最大值所在行索引', 'predict = predict.argmax(axis=1) # 按行求最大值所在行索引（索引恰好是类别）');
INSERT INTO `bd_command` VALUES (29, 'sklearn', '混淆矩阵', 'confmat= confusion_matrix(y_true=y_true,y_pred=predict) #输出混淆矩阵');
INSERT INTO `bd_command` VALUES (30, 'sns', '绘制热度图', 'sns.heatmap(confmat,annot=True) #绘制热度图');
INSERT INTO `bd_command` VALUES (32, 'pandas', '删除列', 'data = data.drop([\'Time\', \'Amount\'], axis=1)');
INSERT INTO `bd_command` VALUES (33, 'sklearn', '词频矩阵 ', '#将文本中的词语转换为词频矩阵  \r\nvectorizer = CountVectorizer()\r\n\r\n#计算个词语出现的次数  \r\nX = vectorizer.fit_transform(corpus)\r\n\r\n#获取词袋中所有文本关键词  \r\nword = vectorizer.get_feature_names() ');
INSERT INTO `bd_command` VALUES (34, 'pandas', '删除缺失值', 'data = data.dropna() #删除缺失值');
INSERT INTO `bd_command` VALUES (35, '文本分类', '逐行提取停用词', 'stopwords = [line.strip() for line in open(filepath,\'r\',  encoding=\'utf-8\').readlines()]  #逐行提取停用词');
INSERT INTO `bd_command` VALUES (36, '文本分类', '获取单词排名', 'word_index = tokenizer.word_index #将单词（字符串）映射为它们的排名或者索引');
INSERT INTO `bd_command` VALUES (37, 'keras', 'embedding层', 'model.add(Embedding(input_dim=max_words, output_dim=embedding_dim)) #embedding层，设置输入输出维度');
INSERT INTO `bd_command` VALUES (38, 'keras', 'LSTM层', 'model.add(LSTM(100, dropout=0.3, recurrent_dropout=0.3, return_sequences=True)) #LSTM层，丢弃30%。若后面还需要接LSTM层，则return_sequences=True');
INSERT INTO `bd_command` VALUES (39, 'keras', '神经网络多分类', 'model.add(Dense(9, activation=\'softmax\'))');
INSERT INTO `bd_command` VALUES (40, 'keras', '配置模型compile', 'model.compile(loss=\'categorical_crossentropy\', #损失函数\r\n              optimizer=\'RMSProp\', #优化器\r\n              metrics=[\'accuracy\'] #评估指标\r\n             ) ');
INSERT INTO `bd_command` VALUES (41, 'keras', '训练模型', 'history = model.fit(X_train, #训练集\r\n                    Y_train, #标签\r\n                    epochs=100 , #训练轮数\r\n                    batch_size=400, #每次训练抽取样本数\r\n#                    callbacks = [monitor],\r\n                    validation_split=0.2, #验证集比例\r\n                    #validation_data=(X_test,Y_test) #验证集\r\n                   )');
INSERT INTO `bd_command` VALUES (42, 'keras', '保存模型  ', 'model.save(\'model_LSTM.h5\')  #  生成模型文件 \'my_model.h5\'  ');
INSERT INTO `bd_command` VALUES (43, 'keras', '加载模型', 'model2 = load_model(\'model_LSTM.h5\') #加载储存的模型');
INSERT INTO `bd_command` VALUES (44, 'keras', '验证集标签预测', 'y_pred = model2.predict(X_test) #对验证集进行预测，预测结果为概率\r\ny_pred = y_pred.argmax(axis = 1) #每行最大值的索引，即概率最大的索引也是标签');
INSERT INTO `bd_command` VALUES (45, 'torch', '数据加载器', 'train_loader = DataLoader(train_dataset, batch_size=200, shuffle=True)');
INSERT INTO `bd_command` VALUES (46, 'torch', '梯度清零', 'optimizer.zero_grad() # 梯度清零');
INSERT INTO `bd_command` VALUES (47, 'torch', '定义优化器', 'optimizer = torch.optim.Adam(model.parameters(), lr=0.01)');
INSERT INTO `bd_command` VALUES (48, 'torch', '定义损失函数', 'criterion = nn.CrossEntropyLoss()');
INSERT INTO `bd_command` VALUES (49, 'torch', '计算损失', 'loss = criterion(outputs, labels) # 计算损失');
INSERT INTO `bd_command` VALUES (50, 'torch', 'loss.backward', 'loss.backward() # 自动计算损失函数对于模型参数的梯度');
INSERT INTO `bd_command` VALUES (51, 'torch', ' 更新模型的参数', 'optimizer.step() # 更新模型的参数');
INSERT INTO `bd_command` VALUES (52, 'ResNet50', '移除最后一层', 'model.add(tf.keras.applications.ResNet50(include_top = False, # 网络结构的最后一层,resnet50有1000类,移除最后一层\r\n                                        input_shape=(224,224,3), # 设置输入图像大小\r\n                                        pooling = \'avg\', # resnet50模型倒数第二层的输出是三维矩阵-卷积层的输出,做pooling或展平\r\n                                        weights = \'imagenet\'),# 参数有两种imagenet和None,None为从头开始训练,imagenet为从网络下载已训练好的模型开始训练\r\n                                         )');
INSERT INTO `bd_command` VALUES (53, 'ResNet50', '设置合适激活函数进行5分类', 'model.add(tf.keras.layers.Dense(5, activation = \'softmax\')) # 设置合适激活函数进行5分类');
INSERT INTO `bd_command` VALUES (54, 'ResNet50', '增加一个维度', 'img_array = tf.expand_dims(images[i], 0) # 对于单张图片，要符合训练集训练时的格式，即增加一个维度');
INSERT INTO `bd_command` VALUES (55, 'ResNet50', '增加一个维度', 'x = np.expand_dims(x, axis=0) # 对于单张图片，要符合训练集训练时的格式，即增加一个维度');
INSERT INTO `bd_command` VALUES (56, 'ResNet50', '图片转化为数组', 'x = image.img_to_array(img) # 图片转化为数组');

SET FOREIGN_KEY_CHECKS = 1;
