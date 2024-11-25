import io
from solid.solid_api import SolidAPI
from ..models import Song, User
import json
from ..services.trust_awareness import TrustAwareness

API = SolidAPI()
PLAYLISTS_URL = 'streaming/playlists/'
PLAYLISTS_FILE_NAME = 'list.json'
UPLOAD_URL = 'streaming/uploaded_songs/'
PERSONAL_INFO_URL = 'personal/info.json'

def fetch_name(storage_link):
  response = json.loads(API.get(storage_link+PERSONAL_INFO_URL).text)
  return response['name']

def fetch_playlists(storage_link):
  playlist_list = fetch_playlist(storage_link, storage_link + PLAYLISTS_URL + PLAYLISTS_FILE_NAME) 
  trusted_playlists = TrustAwareness.check_playlists(playlist_list.keys())
  return list(trusted_playlists), (len(playlist_list) > len(trusted_playlists))

def upload(storage_link, uploaded_file, thumbnail, entered_song_name):
  API.create_folder(storage_link+UPLOAD_URL+entered_song_name+'/')
  upload_url = storage_link+UPLOAD_URL+entered_song_name+'/'
  upload_file(thumbnail, upload_url+'thumbnail/')
  song_url = upload_file(uploaded_file, upload_url+'song/')
  is_trustworthy = TrustAwareness.check_uploaded_song(song_url, entered_song_name)
  create_records(storage_link, 
                 entered_song_name,
                 is_trustworthy,
                 upload_file(uploaded_file, upload_url+'song/'),
                 upload_file(thumbnail, upload_url+'thumbnail/'))

def delete_song(song):
  upload_url = song.artist.storage_url+UPLOAD_URL+song.name+'/'
  API.delete(song.link)
  API.delete(song.thumbnail)
  API.delete(upload_url+'thumbnail/')
  API.delete(upload_url+'song/')
  API.delete(upload_url)
  song.delete()

def exists(link):
  return API.item_exists(link)

def upload_file(file, upload_url):
  uploaded_url = upload_url+file.name
  API.put_file(uploaded_url, file, file.content_type)
  return uploaded_url

def add_to_playlist(song, storage_link, playlist_name):
  playlist_url = storage_link+PLAYLISTS_URL+PLAYLISTS_FILE_NAME
  playlist_data = fetch_playlist(storage_link, playlist_url)
  if song.link not in playlist_data.get(playlist_name, []):
    playlist_data.setdefault(playlist_name, []).append(song.link)
  json_data = json.dumps(playlist_data, indent=4)
  f = io.BytesIO(json_data.encode('UTF-8'))
  return API.put_file(playlist_url, f, 'application/json')

def remove_from_playlist(song, storage_link, playlist_name):
  playlist_url = storage_link+PLAYLISTS_URL+PLAYLISTS_FILE_NAME
  playlist_data = fetch_playlist(storage_link, playlist_url)
  playlist_data[playlist_name].remove(song.link)
  json_data = json.dumps(playlist_data, indent=4)
  f = io.BytesIO(json_data.encode('UTF-8'))
  return API.put_file(playlist_url, f, 'application/json')

def fetch_playlist(storage_link, playlist_url):
  if not exists(storage_link+PLAYLISTS_URL):
    API.create_folder(storage_link+PLAYLISTS_URL)
  
  if not exists(playlist_url):
    return {}
  
  resp = API.get(playlist_url)
  return json.loads(resp.text)

def playlist_songs(storage_link, playlist_name):
  playlists = fetch_playlist(storage_link, storage_link+PLAYLISTS_URL+PLAYLISTS_FILE_NAME)
  return playlists[playlist_name]

def create_playlist(storage_link, playlist_name):
  playlist_url = storage_link+PLAYLISTS_URL+PLAYLISTS_FILE_NAME
  playlist_data = fetch_playlist(storage_link, playlist_url)
  playlist_data[playlist_name] = []
  json_data = json.dumps(playlist_data, indent=4)
  f = io.BytesIO(json_data.encode('UTF-8'))
  return API.put_file(playlist_url, f, 'application/json')

def delete_playlist(storage_link, playlist_name):
  playlist_url = storage_link+PLAYLISTS_URL+PLAYLISTS_FILE_NAME
  playlist_data = fetch_playlist(storage_link, playlist_url)
  del playlist_data[playlist_name]
  json_data = json.dumps(playlist_data, indent=4)
  f = io.BytesIO(json_data.encode('UTF-8'))
  return API.put_file(playlist_url, f, 'application/json')

def create_records(storage_link, song_name, is_trustworthy, uploaded_song_url, uploaded_thumbnail_url):
  try:
    user = User.objects.get(storage_url=storage_link)
  except User.DoesNotExist:
    user = User.objects.create(storage_url=storage_link)
  
  Song.objects.create(artist=user, name=song_name, link=uploaded_song_url, thumbnail=uploaded_thumbnail_url, is_trusted=is_trustworthy)

def check_songs(storage_link, current_roster):
  song_folder_data = API.read_folder(storage_link+UPLOAD_URL)
  song_folders = list(map(lambda x: x, song_folder_data.folders))
  current_songs_link = [song.link for song in current_roster]
  for song_folder in song_folders:
    song_data = API.read_folder(song_folder.url+'/song/')
    song_url = song_data.files[0].url
    if not song_url in current_songs_link:
      is_trustworthy = TrustAwareness.check_uploaded_song(song_url, song_folder.name)
      thumnnail_data = API.read_folder(song_folder.url+'/thumbnail/')
      thumbnail_url = thumnnail_data.files[0].url
      create_records(storage_link, song_folder.name, is_trustworthy, song_url, thumbnail_url)