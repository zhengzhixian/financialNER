# financialNER
CCF竞赛-互联网金融实体识
网址 https://www.datafountain.cn/competitions/361 
初赛 baseline 0.24

#### 该比赛使用了两种方式：
1、[BERT_BILSTM_CRF]：中文预训练Bert模型fine-tuning后生成每个词向量,再过BILSTM_CRF进行实体标注。其中可省略BILSTM直接使用CRF,这是因为BERT编码向量内已经包含了双向信息。
2、[BILSTM_CRF]：gensim版本的word2vec在中文维基语料库的词向量，再经过BILSTM_CRF。

#### 数据生成
``
mu_data.py 生成序列标注

result_processiing 融合BERT_BILSTM 和 BILSTM_CRF 结果
``
#### 模型训练  BERT_BILSTM_CRF

下载BERT预训练模型并解压
```shell
wget https://storage.googleapis.com/bert_models/2018_11_03/chinese_L-12_H-768_A-12.zip 
unzip chinese_L-12_H-768_A-12.zip
```
下载开源包，该包支持命名实体识别的训练。
```shell
pip install bert-base==0.0.7 -i https://pypi.python.org/simple
```
安装完bert-base后，会生成两个基于命名行的工具，其中bert-base-ner-train支持命名实体识别模型的训练，需要指定训练数据的目录，BERT相关参数的目录即可。
执行以下命令即可开始训练
```shell
bert-base-ner-train 
-data_dir data/ 
-output_dir data/finance_output/ 
-init_checkpoint chinese_L-12_H-768_A-12/bert_model.ckpt 
-bert_config_file chinese_L-12_H-768_A-12/bert_config.json 
-vocab_file chinese_L-12_H-768_A-12/vocab.txt 
-device_map 0,1 
-batch_size 32 
-num_train_epochs 20  
-label_list B-ORG,I-ORG,O
```
-device_map 指定GPU训练
-batch_size：批训练的数量
-label_list 实体命名的分类

