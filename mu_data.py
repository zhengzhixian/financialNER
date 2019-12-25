import pandas as pd
from multiprocessing import Pool

def train_data_process(text, labels, i):
    print('开始：', i)
    text = str(text)
    new_dataframe = pd.DataFrame(columns=('text', 'label'))
    label_list = str(labels).split(';')
    data_hang_iter = iter(range(len(str(text))))
    i = 0
    for t in data_hang_iter:
        # 匹配多个label
        for label in label_list:
            label_len = len(label)
            if text[t:label_len+t] == label:
                new_dataframe.loc[i] = [text[t], 'B-ORG']
                i = i+1
                for num in range(label_len-1):
                    next(data_hang_iter)
                    new_dataframe.loc[i] = [text[t+num+1], 'I-ORG']
                    i = i+1
                break
            elif label == label_list[-1]:
                new_dataframe.loc[i] = [text[t], 'O']
                i = i+1
    new_dataframe.loc[i] = [None, None]
    print('结束：', i)
    return new_dataframe

if __name__ == '__main__':
    train_data = pd.read_csv('data/Train_Data.csv', index_col=None)
    tmp_dataframe = []
    pool = Pool()
    new_dataframe = pd.DataFrame(columns=('text', 'label'))
    for i in range(0, len(train_data)):
        text = train_data.iloc[i]['text']
        label = train_data.iloc[i]['unknownEntities']
        print('i:', i)
        tmp_dataframe.append(pool.apply_async(
            train_data_process, args=(text, label, i)))
    pool.close()
    pool.join()
    for j in tmp_dataframe:
        new_dataframe = pd.concat(
            [new_dataframe, j.get()], axis=0, ignore_index=True)
        print(new_dataframe)
    new_dataframe.to_csv('data/mu_train.csv', index=None)