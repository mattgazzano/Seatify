import sys
sys.path.insert(1, '/home/mattgazzano/github/seatify/')
import boto3
import pandas as pd
import config
import psycopg2
import psycopg2.extras
from datetime import date


minio_s3 = boto3.client('s3',
                  endpoint_url=config.minio_endpoint_url,
                  aws_access_key_id=config.minio_access_key,
                  aws_secret_access_key=config.minio_secret_key,
                  region_name='us-east-1'
)

postgres_connection = psycopg2.connect(
    host='localhost'
    , port='5432'
    , database='seatify'
    , user=config.postgres_username
    , password=config.postgres_password
)

#Extract .csv files from the MinIO S3 bucket
processing_date = date.today()

seatify_tables = ['r_fact_seatgeek_performer_event_relationships'
                , 'r_dimension_seatgeek_performers'
                , 'r_dimension_spotify_artists'
                , 'r_fact_spotify_track_relationships'
                , 'r_dimension_spotify_tracks'
                , 'r_dimension_spotify_albums'
                , 'r_fact_spotify_artist_genres'
                , 'r_fact_spotify_album_markets'
                , 'r_dimension_country_codes']
  

for i in seatify_tables:
    print('Starting:',i)
    response = minio_s3.get_object(Bucket='seatify'
                                  , Key=f'{processing_date}/{i}.csv')
    status = response.get('ResponseMetadata', {}).get('HTTPStatusCode')

    if status == 200:
        s3_df = pd.read_csv(response.get('Body'))
    else:
        print(f'Unsuccessful S3 get_object response. Status - {status}')

    #Add to postgres
    postgres_cursor = postgres_connection.cursor()

    #Drop if it exists
    drop_if_exists = f'DROP TABLE IF EXISTS {i};'
    postgres_cursor.execute(drop_if_exists)

    #Create table if it doesnt already exist
    create_table = open(f'{config.postgres_create_insert_path}CREATE TABLE {i}.sql','r').read()
    postgres_cursor.execute(create_table)

    #Insert data into table
    insert_query = open(f'{config.postgres_create_insert_path}INSERT INTO {i}.sql','r').read()

    #execute the insert statement on multiple records
    postgres_cursor.executemany(insert_query, s3_df.values)

    postgres_connection.commit()
    print('Finished:',i)

postgres_connection.close()