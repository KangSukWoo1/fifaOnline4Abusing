#!/usr/bin/env python
# coding: utf-8

from google.cloud import bigquery
import pandas as pd

def upload(df):
    key_path = 'fifaonlineabusing-e53258229306.json'
    client = bigquery.Client.from_service_account_json(key_path)
    project_id = 'fifaonlineabusing'
    dataset_id = 'transactionData'
    table_name = 'transactionData'

    table_ref = f'{project_id}.{dataset_id}.{table_name}'
    job_config = bigquery.LoadJobConfig()
    job_config.autodetect = True
    job_config.write_disposition = bigquery.WriteDisposition.WRITE_TRUNCATE
    job = client.load_table_from_dataframe(df, table_ref, job_config=job_config)
    job.result()

    print(f'Data uploaded to {table_ref}')

if __name__ == "__main__":
    main()