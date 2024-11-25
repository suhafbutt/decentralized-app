
class TrustAwareness:
  def valid_storage(storage_link):
    if storage_link == 'https://getbootstrap.com/':
      return False
    
    return True

  def check_uploaded_song(uploaded_file_url, entered_song_name):
    return entered_song_name!='houdini'

  def check_playlists(playlists):
    return list(filter(lambda playlist_name: playlist_name != 'fav_songs', playlists))
  