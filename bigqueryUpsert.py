#!/usr/bin/env python
# coding: utf-8

# In[ ]:


#!/usr/bin/env python
# coding: utf-8

from google.cloud import bigquery
import pandas as pd
key_path = 'fifaonlineabusing-e53258229306.json'
client = bigquery.Client.from_service_account_json(key_path)

def upload(df):
    project_id = 'fifaonlineabusing'
    dataset_id = 'transactionData'
    table_name = 'tempStagingTable'

    table_ref = f'{project_id}.{dataset_id}.{table_name}'
    job_config = bigquery.LoadJobConfig()
    job_config.autodetect = True
    job_config.write_disposition = bigquery.WriteDisposition.WRITE_TRUNCATE
    job = client.load_table_from_dataframe(df, table_ref, job_config=job_config)
    job.result()

    print(f'Data uploaded to {table_ref}')

def merge():
    project_id = 'fifaonlineabusing'
    dataset_id = 'transactionData'
    table_name = 'transactionData'
    query = f"""
    MERGE transactionData AS T
    USING tempStagingTable AS S
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
if __name__ == "__main__":
    main()

