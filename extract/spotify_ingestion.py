# Import required packages
import sys
sys.path.insert(1, '/home/mattgazzano/github/seatify/')
import seatify_secrets
import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime, timedelta
import base64
import itertools
import gspread

gcloud_service_account = gspread.service_account()

# Spotify API Authentication
client_id = seatify_secrets.seatify_client_id
client_secret = seatify_secrets.seatify_client_secret
client_creds = f'{client_id}:{client_secret}'
client_creds_b64 = base64.b64encode(client_creds.encode())

## Create a class to streamline authentication and calling specific objects
class SpotifyAPI(object):
    access_token = None
    access_token_expires = datetime.now()
    access_token_did_expire = True
    client_id = None
    client_secret = None
    token_url = seatify_secrets.spotify_token_url

    def __init__(self,client_id,client_secret,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.client_id = client_id
        self.client_secret=client_secret

    def _get_client_credentials(self):
        """
        Returns a base64 encoded string
        """
        client_id = self.client_id
        client_secret = self.client_secret
        if client_secret == None or client_id == None:
            raise Exception('You must set client_id and client_secret')
        
        client_creds = f'{client_id}:{client_secret}'
        client_creds_b64 = base64.b64encode(client_creds.encode())
        return client_creds_b64.decode()

    def _get_token_headers(self):
        return {
            'Authorization': f'Basic {client_creds_b64.decode()}'
            , 'Content-Type': 'application/x-www-form-urlencoded'
        }
    
    def _get_token_data(self):
        return  {
            'grant_type': 'client_credentials'
        }

    def _perform_auth(self):
        token_url = self.token_url
        token_data = self._get_token_data()
        token_headers = self._get_token_headers()

        r = requests.post(token_url
                , data = token_data
                , headers = token_headers)

        if r.status_code not in range(200,299):
            raise Exception('Could not authenticate client')
            return False
        data = r.json()
        now = datetime.now()
        access_token = data['access_token']
        expires_in = data['expires_in'] # seconds
        expires = now + timedelta(seconds=expires_in)
        self.access_token = access_token
        self.access_token_expires = expires
        self.access_token_did_expire = expires < now
        did_expire = expires < now
        return True

    def _get_access_token(self):
        token = self.access_token
        expires = self.access_token_expires
        now = datetime.now()
        if expires < now:
            self._perform_auth()
            return self._get_access_token()
        elif token == None:
            self._perform_auth()
            return self._get_access_token()
        return token

    def _get_resource_header(self):
        access_token = self._get_access_token()
        headers = {
            'Authorization' : f'Bearer {access_token}'
        }
        return headers

    def _get_resource(self,lookup_id,resource_type='albums',version='v1'):
        endpoint = f'https://api.spotify.com/{version}/{resource_type}/{lookup_id}'
        headers = self._get_resource_header()
        r = requests.get(endpoint,headers=headers)
        if r.status_code not in range(200,299):
            return r.status_code
        return r.json()

    #Callable functions
    def get_artist(self,_id):
        return self._get_resource(_id, resource_type='artists')
    
    def get_artists_50(self,_ids):
        return self._get_resource(f'?ids={_ids}', resource_type='artists')
    
    def get_artist_top_tracks(self,_id,market='US'):
        return self._get_resource(f'{_id}/top-tracks?market={market}', resource_type='artists')

    def get_track(self,_id):
        return self._get_resource(_id, resource_type='tracks')
    
    def get_tracks_50(self,_ids):
        return self._get_resource(f'?ids={_ids}', resource_type='tracks')

    def get_album(self,_id):
       return self._get_resource(_id, resource_type='albums')

    def get_albums_20(self,_ids):
        return self._get_resource(f'?ids={_ids}', resource_type='albums')

    def get_playlist(self,_id):
        return self._get_resource(_id, resource_type='playlists')

    def get_playlist_items(self,_id):
        return self._get_resource(f'{_id}/tracks', resource_type='playlists')    

# Compile a list of Popular Playlists via Webscraping and a Google Sheets doc
def webscrape_playlists():
    print('Start: Webscraping playlists')
    url_html = requests.get(seatify_secrets.playlist_website).text
    soup = BeautifulSoup(url_html,features='html.parser')
    h3 = soup.findAll('h3')
    web_scraped_playlist_ids = []
    for result in h3:
        links = result.parent.parent.find_all('a', href=True)
        for link in links:
            if link.get('href').startswith('https://open.spotify.com/playlist'):
                web_scraped_playlist_ids.append(link.get('href')[34:56])
        break
    
    #Google Sheets file
    spotify_playlists_sheet = gcloud_service_account.open_by_key(seatify_secrets.playlists_google_sheet_key).worksheet('playlist_ids')
    google_sheets_playlist_ids = pd.json_normalize(spotify_playlists_sheet.get_all_records())['playlist_id'].values.tolist()

    playlists = web_scraped_playlist_ids + google_sheets_playlist_ids
    print('End: Webscraping playlists')
    return playlists

# Extract Artist ID and Track IDs from Playlists
def extract_from_playlists(spotify,playlists):
    print('Start: Extract from Playlists')
    r_dimension_spotify_artists = pd.DataFrame()
    track_ids = []
    loop_instance = 1
    for playlist_id in playlists:
        playlist = spotify.get_playlist(playlist_id)
        playlist_items = playlist['tracks']['items']
        try: r_dimension_spotify_artists = pd.concat([r_dimension_spotify_artists,pd.DataFrame(pd.json_normalize(playlist_items, record_path=['track','artists']))],axis=0) 
        except: pass
        try: track_ids.append(pd.json_normalize(spotify.get_playlist_items(playlist_id)['items'])['track.id'].values.tolist())
        except: pass
        print(playlist_id,'-',loop_instance,'of',len(playlists),'(',round((loop_instance / len(playlists)) * 100),'%)')
        loop_instance = loop_instance + 1
    ## Dedeup the dataframe. By Nature we will see the same artist multiple times if a user added multiple songs by the same artist
    r_dimension_spotify_artists = r_dimension_spotify_artists.drop_duplicates()
    print('End: Extract from Playlists')
    artist_ids = r_dimension_spotify_artists.id.values.tolist()
    track_ids = list(itertools.chain.from_iterable(track_ids))
    return artist_ids, track_ids

# divide a list into comma separated string segments of n. This is the API limit per call (Either 20 or 50 per the documentation)
def divide_chunks(list, n):   
    list = [x for x in list if str(x) != 'nan' and x != None]
    for i in range(0, len(list), n):
        yield ','.join(list[i:i + n])

# Iterate over the list of Artist IDs found in playlists and extract the full object from the API
def r_dimension_spotify_artists(spotify,artist_ids_50):
    print('Start: dim_artists')
    artists_obj = []
    loop_instance = 1
    r_dimension_spotify_artists = pd.DataFrame()
    for i in artist_ids_50:
        artists_obj = spotify.get_artists_50(i)
        try: r_dimension_spotify_artists = pd.concat([r_dimension_spotify_artists,pd.DataFrame(pd.json_normalize(artists_obj['artists'],sep='_'))],axis=0)
        except: pass
        #Show Progress
        print(i)
        print(loop_instance,'of',len(artist_ids_50),'(',round((loop_instance / len(artist_ids_50)) * 100),'%)')
        loop_instance = loop_instance + 1

    r_fact_spotify_artist_genres = r_dimension_spotify_artists[['id','genres']].explode('genres')

    ## Clean dataframe & Change the Index
    r_dimension_spotify_artists = r_dimension_spotify_artists.drop(['genres'],axis=1)
    r_dimension_spotify_artists.set_index('id', inplace=True)

    #Clean Artist Genres & Drop Nulls
    r_fact_spotify_artist_genres.set_index('id', inplace=True)
    r_fact_spotify_artist_genres.dropna(axis=0, how='any', inplace=True)
    ## Output to a CSV
    r_dimension_spotify_artists.to_csv(seatify_secrets.extract_path+'r_dimension_spotify_artists.csv')
    r_fact_spotify_artist_genres.to_csv(seatify_secrets.extract_path+'r_fact_spotify_artist_genres.csv')
    print('End: dim_artists')

# r_fact_TRACK_RELATIONSHIPS - Track Relationships - each song can have more than one artist & album
def get_tracks(spotify,ids):
    return pd.json_normalize(spotify.get_tracks_50(ids)['tracks']
                                , record_path= ['artists']
                                , meta = ['name'
                                        , 'id'
                                        , 'disc_number'
                                        , 'duration_ms'
                                        , 'explicit'
                                        , 'href'
                                        , 'is_local'
                                        , 'is_playable'
                                        , 'popularity'
                                        , 'preview_url'
                                        , 'track_number'
                                        , ['album','id']]
                                , errors='ignore'
                                , meta_prefix = 'track_'
                                , sep = '_'
                                )

def r_fact_spotify_track_relationships(spotify,track_ids):
    print('Start: r_fact_track_relationships')
    loop_instance = 1
    for i in track_ids:
        if loop_instance == 1:
            r_fact_spotify_track_relationships = get_tracks(spotify,i)
        else:
            r_fact_spotify_track_relationships = pd.concat([r_fact_spotify_track_relationships,get_tracks(spotify,i)])
        #Show Progress
        print(loop_instance,'of',len(track_ids),'(',round((loop_instance / len(track_ids)) * 100),'%)')
        loop_instance = loop_instance + 1

    # Drop Duplicates
    r_fact_spotify_track_relationships = r_fact_spotify_track_relationships.drop_duplicates()
    # Change the Index
    r_fact_spotify_track_relationships.set_index('id', inplace=True)
    # Output to a CSV
    r_fact_spotify_track_relationships.to_csv(seatify_secrets.extract_path+'r_fact_spotify_track_relationships.csv')
    print('End: r_fact_track_relationships')
    return r_fact_spotify_track_relationships

# DIM_TRACKS - Unique Tracks
def r_dimension_spotify_tracks(spotify,r_fact_spotify_track_relationships):
    print('Start: dim_tracks')
    r_dimension_spotify_tracks = r_fact_spotify_track_relationships[['track_id'
                                                                ,'track_name'
                                                                ,'track_disc_number'
                                                                ,'track_duration_ms'
                                                                ,'track_explicit'
                                                                ,'track_href'
                                                                ,'track_is_local'
                                                                ,'track_is_playable'
                                                                ,'track_popularity'
                                                                ,'track_preview_url'
                                                                ,'track_track_number'
                                                                ,'track_album_id']]
    ## Set index
    r_dimension_spotify_tracks = r_dimension_spotify_tracks.reset_index(drop=True)
    r_dimension_spotify_tracks.set_index('track_id', inplace=True)
    ## Remove duplicates
    r_dimension_spotify_tracks = r_dimension_spotify_tracks.drop_duplicates()
    ## Output to a CSV
    r_dimension_spotify_tracks.to_csv(seatify_secrets.extract_path+'r_dimension_spotify_tracks.csv')
    print('End: dim_tracks')

# DIM_ALBUMS & r_fact_ALBUM_MARKETS
def albums_and_markets(spotify,r_fact_spotify_track_relationships):
    print('Start: dim_albums')
    albums_obj = []
    album_markets_obj = []
    album_ids = [*set(r_fact_spotify_track_relationships.track_album_id.values.tolist())]

    # Divide these ids into lists of 20 comma separated strings. 20 is the greatest that the API can handle
    album_ids_20 = list(divide_chunks(album_ids, 20))

    loop_instance = 1
    df_dim_albums = pd.DataFrame()
    df_r_fact_album_markets = pd.DataFrame()
    for i in album_ids_20:
        albums_obj = spotify.get_albums_20(i)
        try: df_dim_albums = pd.concat([df_dim_albums,pd.DataFrame(pd.json_normalize(albums_obj['albums'],sep='_'))],axis=0)
        except: pass
        try: df_r_fact_album_markets = pd.concat([df_r_fact_album_markets,pd.DataFrame(pd.json_normalize(albums_obj['albums'] ,record_path='available_markets',meta ='id',sep='_'))],axis=0)
        except: pass
        #Show Progress
        print(loop_instance,'of',len(album_ids_20),'(',round((loop_instance / len(album_ids_20)) * 100),'%)')
        loop_instance = loop_instance + 1

    # Change the Index
    df_dim_albums.set_index('id', inplace=True)
    df_r_fact_album_markets.set_index('id', inplace=True)

    # Rename the 0 column to alpa_2_code
    df_r_fact_album_markets.rename(columns={0:'alpha_2_code'}, inplace=True)

    # Output to a CSV
    df_dim_albums.to_csv(seatify_secrets.extract_path+'r_dimension_spotify_albums.csv')
    df_r_fact_album_markets.to_csv(seatify_secrets.extract_path+'r_fact_spotify_album_markets.csv')
    print('End: dim_albums')

# DIM_COUNTRY_CODES
def r_dimension_country_codes():
    print('Start: dim_country_codes')
    df_dim_country_codes = pd.read_html(seatify_secrets.github_country_codes)[0][['Country'
                                                                        ,'Alpha-2 code'
                                                                        ,'Alpha-3 code'
                                                                        ,'Numeric code'
                                                                        ,'Latitude (average)'
                                                                        ,'Longitude (average)']]
    df_dim_country_codes.rename(columns={'Country':'country'
                                        ,'Alpha-2 code': 'alpha_2_code'
                                        ,'Alpha-3 code': 'alpha_3_code'
                                        ,'Numeric code': 'numeric_code'
                                        ,'Latitude (average)': 'latitude'
                                        ,'Longitude (average)': 'longitude'
                                        }
                                , inplace=True)

    spotify_playlists_sheet = gcloud_service_account.open_by_key(secrets.countries_sheet_key).worksheet('countries')
    wiki_country_list = pd.json_normalize(spotify_playlists_sheet.get_all_records())

    df_dim_country_codes = df_dim_country_codes.merge(wiki_country_list
                                                    , how='left'
                                                    , left_on= 'country'
                                                    , right_on= 'country')

    df_dim_country_codes.set_index('country', inplace=True)

    df_dim_country_codes.to_csv(seatify_secrets.extract_path+'r_dimension_country_codes.csv')
    print('End: dim_country_codes')


def main():
    spotify = SpotifyAPI(client_id, client_secret)
    print('Authorization Result:',spotify._perform_auth())
    print('Access Token:',spotify.access_token)
    print('End: Spotify API Authentication')
    playlist_ids = webscrape_playlists()
    artist_ids, track_ids = extract_from_playlists(spotify,playlist_ids)
    # artist_ids_cleaned = [x for x in artist_ids if str(x) != 'nan' and x != None]
    artist_ids_50 = list(divide_chunks(artist_ids, 44))
    r_dimension_spotify_artists(spotify,artist_ids_50)
    # track_ids_cleaned = [x for x in track_ids if str(x) != 'nan' and x != None]
    track_ids_50 = list(divide_chunks(track_ids, 44))
    df_r_fact_track = r_fact_spotify_track_relationships(spotify,track_ids_50)
    r_dimension_spotify_tracks(spotify,df_r_fact_track)
    albums_and_markets(spotify,df_r_fact_track)
    r_dimension_country_codes()

if __name__ == '__main__':
    main()
else: pass