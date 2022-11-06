import sys
sys.path.insert(1, '/home/mattgazzano/github/seatify/')
import seatify_secrets
import gspread
from gspread_dataframe import set_with_dataframe
import pandas as pd
import os

#Instantiate connections
## Google Sheets
gcloud_service_account = gspread.service_account()

## Postgres
postgres_connection = seatify_secrets.postgres_connection_sqa
dbt_models_path = os.listdir('/home/mattgazzano/github/seatify/transform/seatify/models')
dbt_models = ','.join(["'" + x.replace('.sql','')+ "'" for x in dbt_models_path if '.sql' in x])
tables = pd.read_sql(f"select table_name from information_schema.tables where table_name in ({dbt_models}) and table_name != 'dim_album_markets'",postgres_connection)['table_name'].values.tolist()

for i in tables:
    print('start:',i)
    worksheet = gcloud_service_account.open_by_key(seatify_secrets.seatify_dashboard_postgres_tables).worksheet(i)
    worksheet.clear()
    postgres_table = pd.read_sql(f'select * from {i}',postgres_connection)
    set_with_dataframe(worksheet=worksheet, dataframe=postgres_table, include_index=False,include_column_header=True)
    print('end:',i)
