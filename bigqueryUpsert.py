#!/usr/bin/env python
# coding: utf-8

# In[ ]:


#!/usr/bin/env python
# coding: utf-8

from google.cloud import bigquery
import pandas as pd
key_path = 'practice-388013-9fab12440f02.json'
client = bigquery.Client.from_service_account_json(key_path)
project_id = 'opgg-data-analytics'
dataset_id = 'tft'

def upload(df):
    table_name = 'tempStagingTable'
    table_ref = f'{project_id}.{dataset_id}.{table_name}'
    job_config = bigquery.LoadJobConfig()
    job_config.autodetect = True
    job_config.write_disposition = bigquery.WriteDisposition.WRITE_TRUNCATE
    job = client.load_table_from_dataframe(df, table_ref, job_config=job_config)
    job.result()

    print(f'Data uploaded to {table_ref}')

def merge():
    table_name = 'transactionData'
    query = f"""
    MERGE {project_id}.{dataset_id}.transactionData AS T
    USING {project_id}.{dataset_id}.tempStagingTable AS S
    ON T.saleSn = S.saleSn
    WHEN MATCHED THEN
        UPDATE SET 
        T.accessId = S.accessId,
        T.tradeDate = S.tradeDate,
        T.saleSn = S.saleSn,
        T.spid = S.spid,
        T.grade = S.grade,
        T.value = S.value,
        T.type = S.type
    WHEN NOT MATCHED THEN
        INSERT (saleSn, accessId, tradeDate, spid, grade, value, type)
        VALUES (S.saleSn, S.accessId, S.tradeDate, S.spid, S.grade, S.value, S.type)
"""
    client = bigquery.Client.from_service_account_json(key_path)
    job = client.query(query)
    job.result()
if __name__ == "__main__":
    main()

