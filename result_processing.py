import pandas as pd
#Bert ner
bert_ner = pd.read_csv('BERT_BiLSTM_CRF/result.csv')

crf_ner = pd.read_csv('BiLSTM_CRF_NER/Test_result.csv')
crf_ner = crf_ner.drop('Unnamed: 0',1)
crf_ner=crf_ner.rename(columns ={'0':'id','1':'unknownEntities_1'})

result = pd.merge(bert_ner,crf_ner,on ='id')

#常见的实体
regular = ['iPhone']

def tag_clean(Tag):
    TAG =[]
    for tag in Tag.split(';'):
        if tag !='nan':
            tag_1 = tag.replace('\t','').replace('____','').replace('__','').replace('┏_ ━━━━━━━┓','').replace('_┗━━━━━━━━┛','')\
                .replace('"','').replace(',','').replace(' ','').replace('(','').replace(')','').replace('\\','').replace('   ','').replace('    ','')
            if len(tag_1)>1 and ' 'not in tag_1:
                print(tag_1)
                TAG.append(tag_1)
    return TAG


TAG_output =[]
ID =[]
for  i in range(len(result)):

    tag_bert = str(result.loc[i,'unknownEntities'])
    tag_crf = str(result.loc[i,'unknownEntities_1'])
    TAG =[]
    #对Bert结果进行过滤输出
    TAG_bert = tag_clean(tag_bert)
    #对crf结果进行过滤输出
    TAG_crf = tag_clean(tag_crf)
    tag_str = ';'.join(list(set(TAG_bert+TAG_crf))).replace('"','')
    TAG_output.append(tag_str)
    ID.append(result.loc[i,'id'])
df =pd.DataFrame(zip(ID,TAG_output)).rename(columns ={0:'id',1:'unknownEntities'})

df.to_csv('result_all.csv',encoding='utf8',index=None)
df.to_excel('result_all.xlsx',encoding='utf8',index=None)

