#!/usr/bin/env python
# coding: utf-8

# In[1]:


import fifaMetaData
from google.cloud import bigquery
import pandas as pd
import shap
key_path = 'practice-388013-9fab12440f02.json'
client = bigquery.Client.from_service_account_json(key_path)
project_id = 'opgg-data-analytics'
dataset_id = 'tft'
table_name = 'transactionData'
query = f"""
    SELECT DISTINCT *
    FROM `{project_id}.{dataset_id}.{table_name}`
    WHERE tradeDate < '2023-05-01'
"""

query_job = client.query(query)
results = query_job.result()
df = results.to_dataframe()


# In[11]:


player = pd.DataFrame(fifaMetaData.spid)
season = pd.DataFrame(fifaMetaData.seasonId)


# In[12]:


df['seasonId'] = df.spid.apply(lambda x : int(str(x)[:3]))
temp_df = pd.merge(df, player, left_on = 'spid', right_on = 'id')
merge_df = pd.merge(temp_df, season, on = 'seasonId')
overBilion = merge_df[merge_df['value']>1000000000]#십 억 이상
overBilion.loc[overBilion['type'] == 'sell', 'sellMoney'] = overBilion.loc[overBilion['type'] == 'sell', 'value'].copy()
overBilion.loc[overBilion['type'] == 'buy', 'buyMoney'] = overBilion.loc[overBilion['type'] == 'buy', 'value'].copy()
overBilion.loc[:,'datetime'] = pd.to_datetime(overBilion['tradeDate'])


# In[13]:


group_overBilion = overBilion.groupby(['accessId','name','seasonId','className','id','spid'], as_index = False).agg({
    'datetime' : lambda x : (x.max() - x.min()).total_seconds(),
    'sellMoney' : ['sum','count'],
    'buyMoney' : ['sum','count'],
    'spid' : 'count',
    'id' : 'first',
    'grade' : ['max','std']
})
group_overBilion.columns = ['accessId','name','seasonId','className','datetime','sellSum','sellCount','buySum','buyCount','transactionCount','id','grade','gradeStd']

group_overBilion = group_overBilion[group_overBilion['gradeStd'].notnull()]
group_overBilion = group_overBilion[group_overBilion['gradeStd'] == 0]
group_overBilion = group_overBilion[~group_overBilion['seasonId'].isin([280,283,284,511])]#신규 시즌인 HG, RTN, 라이브 퍼포먼스 대상인 22UCL, 22PL 시즌 제외
group_overBilion['benefit'] = group_overBilion['sellSum'] - group_overBilion['buySum']


# In[14]:


doubt = group_overBilion[(group_overBilion['benefit'] >= 10000000000) & 
                         (group_overBilion['buyCount'] > 3) &
                         (group_overBilion['grade'] > 5)].sort_values(by = 'datetime')[['className','name','grade','datetime','buyCount','sellCount','transactionCount','benefit']]
doubt['label'] = 1


# In[15]:


import random
#doubt data augmentation
doubt_augmentation = doubt
for i in range(1,1000):
    temp_doubt = pd.DataFrame()
    temp_doubt[['className','name','grade']]  = doubt[['className','name','grade']] 
    temp_doubt['datetime'] = doubt['datetime'].apply(lambda x : x + random.randrange(0,10000))
    transacation_random = random.randrange(1,10)
    temp_doubt['buyCount'] = doubt['buyCount'].apply(lambda x: x + transacation_random)
    temp_doubt['sellCount'] = doubt['sellCount'].apply(lambda x : x + transacation_random)
    temp_doubt['transactionCount'] = temp_doubt['buyCount'] + temp_doubt['sellCount']
    temp_doubt['benefit'] = doubt['benefit'].apply(lambda x : x + random.randrange(-1000000000, 1000000000))
    temp_doubt['label'] = doubt['label']
    doubt_augmentation = pd.concat([doubt_augmentation, temp_doubt])


# In[16]:


merge_data = pd.merge(doubt_augmentation, group_overBilion, on = ['className','name','grade','datetime','buyCount','sellCount','transactionCount','benefit'], how = 'outer')
merge_data = merge_data[['name','className','grade','datetime','buyCount','sellCount','transactionCount','benefit','label']]
merge_data = merge_data.fillna(0)


# In[17]:


train_data = pd.concat([temp_doubt, merge_data]).reset_index(drop = True)


# In[18]:


shuffle_data = train_data.sample(frac = 1, random_state = 42)
new_train_data = shuffle_data.drop(columns = ['className','name'])


# In[19]:


from sklearn.ensemble import RandomForestClassifier
import matplotlib.pyplot as plt
from sklearn import tree

train_len = int(len(new_train_data)*0.7)
clf = RandomForestClassifier()
X_train = new_train_data[:train_len].drop(columns='label')
y_train = new_train_data[:train_len]['label']
clf.fit(X_train, y_train)

fig, ax = plt.subplots(figsize=(12, 12))
estimator = clf.estimators_[0]
tree.plot_tree(estimator, ax=ax, class_names=['0', '1'], feature_names=X_train.columns)
plt.show()


# In[20]:


import joblib
joblib.dump(clf, 'random_forest_model.joblib')

