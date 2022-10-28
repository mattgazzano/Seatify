import sys
sys.path.insert(1, '/home/mattgazzano/github/seatify/')
import config
from minio import Minio
from datetime import date

# Move CSV Files into Minio S3 Bucket
minio = Minio(config.minio_port
            , access_key=config.minio_access_key
            , secret_key=config.minio_secret_key
            , secure=False)

if minio.bucket_exists('seatify'): None
else: minio.make_bucket(bucket_name= 'seatify'
                        , location='us-east-1')

seatify_tables = ['r_dimension_spotify_artists'
                , 'r_fact_spotify_track_relationships'
                , 'r_dimension_spotify_tracks'
                , 'r_dimension_spotify_albums'
                , 'r_fact_spotify_artist_genres'
                , 'r_fact_spotify_album_markets'
                , 'r_dimension_country_codes'
                , 'r_fact_seatgeek_performer_event_relationships'
                , 'r_dimension_seatgeek_performers']

for i in seatify_tables:
    minio.fput_object(bucket_name='seatify'
                    , object_name= f'{date.today()}/{i}.csv'
                    , file_path= f'{config.extract_path+i}.csv')