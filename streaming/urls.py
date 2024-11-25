from django.urls import path
from . import views

urlpatterns = [
  path('storage/', views.storage),
  path('index/', views.index),
  path('songs_list/', views.songs_list),
  path('playlists/', views.playlists),
  path('song/upload/', views.upload_song),
  path('logout/', views.logout),
  path('my_songs/', views.my_songs),
  path('song/<str:song_id>/', views.song, name='user_song'),
  path('songs/<int:song_id>/delete/', views.delete_song, name='delete_song'),
  path('playlists/<str:playlist_name>/edit/', views.playlist_songs, name='playlist_songs'),
  path('playlists/create/', views.create_playlist, name='create_playlist'),
  path('playlists/<str:playlist_name>/delete/', views.delete_playlist, name='delete_playlist'),
  path('song/<int:song_id>/add_to_playlist/<str:playlist_name>', views.add_to_playlist, name='add_to_playlist'),
  path('song/<int:song_id>/remove_from_playlist/<str:playlist_name>', views.remove_from_playlist, name='remove_from_playlist'),
]