import pandas as pd
import requests
import json
from requests.adapters import HTTPAdapter
import re
import warnings
import gspread
import sys
sys.path.insert(1, '/home/mattgazzano/github/seatify/')
import config
warnings.filterwarnings("ignore")
pd.set_option('display.max_columns', None)

seatgeek_client_id = config.seatgeek_client_id
seatgeek_client_secret = config.seatgeek_client_secret

class seatgeek_api(object):

    def __init__(self,client_id,client_secret,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.client_id = client_id
        self.client_secret=client_secret
        self.base_endpoint =  'https://api.seatgeek.com/2/'
        self.record_types = ['performers', 'events', 'venues']

    def _record_type_validation(self,record_type):
        if record_type not in self.record_types:
            raise ValueError('Invalid record type of "{0}". Expected one of: {1}'.format(record_type,self.record_types))

    def get_record_by_bulk_id(self,record_type,id,lookup_record_type=''):
        self._record_type_validation(record_type)
        return f'{self.base_endpoint}{record_type}?{lookup_record_type}id={id}&client_id={self.client_id}&client_secret={self.client_secret}'

seatgeek = seatgeek_api(seatgeek_client_id, seatgeek_client_secret)

DEFAULT_TIMEOUT = 5 # seconds

class TimeoutHTTPAdapter(HTTPAdapter):
    def __init__(self, *args, **kwargs):
        self.timeout = DEFAULT_TIMEOUT
        if "timeout" in kwargs:
            self.timeout = kwargs["timeout"]
            del kwargs["timeout"]
        super().__init__(*args, **kwargs)

    def send(self, request, **kwargs):
        timeout = kwargs.get("timeout")
        if timeout is None:
            kwargs["timeout"] = self.timeout
        return super().send(request, **kwargs)

http = requests.Session()
adapter = TimeoutHTTPAdapter(timeout=5)
http.mount("https://", adapter)


# Get the Performer IDs from the ones recorded on the Google Sheet
def performer_json_normalize(performer_json):
    try: return pd.json_normalize(json.loads(http.get(performer_json).text)
                        , record_path=['performers','links']
                        , meta =[['performers','type']
                            , ['performers','name']
                            , ['performers','image']
                            , ['performers','id']
                            , ['performers','divisions']
                            , ['performers','has_upcoming_events']
                            , ['performers','primary']
                            , ['performers','image_attribution']
                            , ['performers','url']
                            , ['performers','score']
                            , ['performers','slug']
                            , ['performers','home_venue_id']
                            , ['performers','short_name']
                            , ['performers','num_upcoming_events']
                            , ['performers','colors']
                            , ['performers','image_license']
                            , ['performers','popularity']
                            , ['performers','location']
                            , ['performers','image_rights_message']
                            , ['performers','images.huge']
                            , ['performers','stats.event_count']]
                        , meta_prefix='seatgeek_'
                        , errors= 'ignore'
                        , sep='_'
                        )
    except: pass

gcloud_service_account = gspread.service_account()
spotify_playlists_sheet = gcloud_service_account.open_by_key(config.seatgeek_artist_ids_sheet_key).worksheet('performers')
gs_seatgeek_performers = pd.json_normalize(spotify_playlists_sheet.get_all_records())['seatgeek_performer_id'].values.tolist()


def divide_chunks(list,delimiter,n):   
    list = [str(x) for x in list if str(x) != 'nan' and x != None]
    for i in range(0, len(list), n):
        yield f'{delimiter}'.join(list[i:i + n])

def get_bulk_performers_by_id(seatgeek,performer_ids_bulk):
    r_dimension_seatgeek_performers = pd.DataFrame()
    loop_instance = 1
    for performers in performer_ids_bulk:
        http = requests.Session()
        adapter = TimeoutHTTPAdapter(timeout=5)
        http.mount("https://", adapter)
        r_dimension_seatgeek_performers = pd.concat([r_dimension_seatgeek_performers, performer_json_normalize(seatgeek_api.get_record_by_bulk_id(seatgeek,'performers',performers))])
        #Show Progress
        print('Completed: ',loop_instance,'of',len(performer_ids_bulk),'(',round((loop_instance / len(performer_ids_bulk)) * 100),'%)')
        loop_instance = loop_instance + 1

    r_dimension_seatgeek_performers.set_index('seatgeek_performers_id', inplace=True)
    r_dimension_seatgeek_performers.rename(columns={'id':'spotify_artist_id'
                                            ,'url': 'spotify_artists_url'}
                                        , inplace=True)
    r_dimension_seatgeek_performers.to_csv(config.extract_path+'r_dimension_seatgeek_performers.csv')
    return r_dimension_seatgeek_performers

def event_json_normalize(event_json):
    try: return pd.json_normalize(json.loads(http.get(event_json).text)
                , record_path= ['events','performers']
                                , meta =[['events','type']
                                        , ['events','id']
                                        , ['events','datetime_utc']
                                        , ['events','datetime_tbd']
                                        , ['events','is_open']
                                        , ['events','datetime_local']
                                        , ['events','time_tbd']
                                        , ['events','short_title']
                                        , ['events','visible_until_utc']
                                        , ['events','score']
                                        , ['events','announce_date']
                                        , ['events','created_at']
                                        , ['events','date_tbd']
                                        , ['events','title']
                                        , ['events','popularity']
                                        , ['events','description']
                                        , ['events','status']
                                        , ['events','event_promotion']
                                        , ['events','conditional']
                                        , ['events','enddatetime_utc']
                                        , ['events','venue.state']
                                        , ['events','venue.name_v2']
                                        , ['events','venue.postal_code']
                                        , ['events','venue.name']
                                        , ['events','venue.links']
                                        , ['events','venue.timezone']
                                        , ['events','venue.url']
                                        , ['events','venue.score']
                                        , ['events','venue.location.lat']
                                        , ['events','venue.location.long']
                                        , ['events','venue.address']
                                        , ['events','venue.country']
                                        , ['events','venue.has_upcoming_events']
                                        , ['events','venue.num_upcoming_events']
                                        , ['events','venue.city']
                                        , ['events','venue.slug']
                                        , ['events','venue.extended_address']
                                        , ['events','venue.id']
                                        , ['events','venue.popularity']
                                        , ['events','venue.access_method.method']
                                        , ['events','venue.access_method.created_at']
                                        , ['events','venue.access_method.employee_only']
                                        , ['events','venue.metro_code']
                                        , ['events','venue.capacity']
                                        , ['events','venue.display_location']
                                        , ['events','stats.listing_count']
                                        , ['events','stats.average_price']
                                        , ['events','stats.lowest_price_good_deals']
                                        , ['events','stats.highest_price']
                                        , ['events','stats.visible_listing_count']
                                        , ['events','stats.dq_bucket_counts']
                                        , ['events','stats.median_price']
                                        , ['events','stats.lowest_sg_base_price']
                                        , ['events','stats.lowest_sg_base_price_good_deals']
                                        , ['events','access_method.method']
                                        , ['events','access_method.created_at']
                                        , ['events','access_method.employee_only']
                                        , ['events','venue.access_method']
                                        ]
                                , meta_prefix='events_'
                                , errors= 'ignore'
                                , sep='_'
                                )
    except: pass

def get_bulk_events_by_performer_id(seatgeek,performer_ids_bulk):
    r_fact_seatgeek_performer_event_relationships = pd.DataFrame()
    loop_instance = 1
    for performers in performer_ids_bulk:
        http = requests.Session()
        adapter = TimeoutHTTPAdapter(timeout=5)
        http.mount("https://", adapter)
        r_fact_seatgeek_performer_event_relationships = pd.concat([r_fact_seatgeek_performer_event_relationships, event_json_normalize(seatgeek.get_record_by_bulk_id('events',performers,'performers.'))])
        #Show Progress
        print('Completed: ',loop_instance,'of',len(performer_ids_bulk),'(',round((loop_instance / len(performer_ids_bulk)) * 100),'%)')
        loop_instance = loop_instance + 1

    r_fact_seatgeek_performer_event_relationships.set_index('events_events_id', inplace=True)
    r_fact_seatgeek_performer_event_relationships.drop(['taxonomies','genres'],axis=1,inplace=True)
    r_fact_seatgeek_performer_event_relationships.drop_duplicates(inplace=True)
    r_fact_seatgeek_performer_event_relationships.to_csv(config.extract_path+'r_fact_seatgeek_performer_event_relationships.csv')
    return r_fact_seatgeek_performer_event_relationships

if __name__ == '__main__':
    print('Start: r_dimension_seatgeek_performers')
    performer_ids_bulk = list(divide_chunks(gs_seatgeek_performers,'&id=',50))
    r_dimension_seatgeek_performers = get_bulk_performers_by_id(seatgeek,performer_ids_bulk)
    print('Start: r_fact_performer_seatgeek_relationships')
    performer_ids_bulk_events = list(divide_chunks(gs_seatgeek_performers,',',50))
    get_bulk_events_by_performer_id(seatgeek,performer_ids_bulk_events)