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
    WHERE tradeDate > '2023-05-01'
    AND tradeDate < '2023-05-20'
"""

query_job = client.query(query)
results = query_job.result()
df = results.to_dataframe()


# In[2]:


player = pd.DataFrame(fifaMetaData.spid)
season = pd.DataFrame(fifaMetaData.seasonId)


# In[3]:


df['seasonId'] = df.spid.apply(lambda x : int(str(x)[:3]))
temp_df = pd.merge(df, player, left_on = 'spid', right_on = 'id')
merge_df = pd.merge(temp_df, season, on = 'seasonId')
overBilion = merge_df[merge_df['value']>1000000000]#십 억 이상
overBilion.loc[overBilion['type'] == 'sell', 'sellMoney'] = overBilion.loc[overBilion['type'] == 'sell', 'value'].copy()
overBilion.loc[overBilion['type'] == 'buy', 'buyMoney'] = overBilion.loc[overBilion['type'] == 'buy', 'value'].copy()
overBilion.loc[:,'datetime'] = pd.to_datetime(overBilion['tradeDate'])


# In[4]:


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


# In[5]:


X_test = group_overBilion[['className','name','grade','datetime','buyCount','sellCount','transactionCount','benefit']].reset_index(drop = True)


# In[6]:


import joblib
clf = joblib.load('random_forest_model.joblib')
y_pred = clf.predict(X_test.drop(columns = ['className','name']))


# In[7]:


X_test['predict'] = y_pred


# In[49]:


X_test[X_test['predict']==1].sort_values(by = 'benefit', ascending = False).to_csv('testDoubtData.csv', encoding = 'utf-8-sig')

