from django.urls import reverse
from django.shortcuts import render
from django.shortcuts import redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from .models import Song, User
from .forms import StorageForm, SongUploadForm, PlaylistForm
from .services import solid_client
from .services.trust_awareness import TrustAwareness
from .serializers.song_serializer import SongSerializer
from streaming.decorators.custom_login_required import custom_login_required
from django.contrib import messages

def storage(request):
  if request.method == 'POST':
    storage_form = StorageForm(request.POST)
    if storage_form.is_valid():
      storage_link = storage_form.cleaned_data['link']
      if TrustAwareness.valid_storage(storage_link):
        if solid_client.exists(storage_link):
          request.session['storage_link'] = storage_link
        if solid_client.exists(storage_link+'personal/info.json'):
          request.session['user_name'] = solid_client.fetch_name(storage_link)
      else:
        messages.error(request, 'This does not seems to be a trusted storage space.', extra_tags='alert-danger')
        return render(request, 'storage.html', { 'form': storage_form})
    try:
      user = User.objects.get(storage_url=storage_link)
      solid_client.check_songs(request.session['storage_link'], user.song_set.all())
    except User.DoesNotExist:
      user = None  
    return redirect('/my_songs/')
  else:
    return render(request, 'storage.html', { 'form': StorageForm()})

def logout(request):
  if 'storage_link' in request.session:
    if 'storage_link' in request.session:
      del request.session['storage_link']
    if 'user_name' in request.session:
      del request.session['user_name']

  return redirect('/index/')

def index(request):
  songs = Song.objects.filter(is_trusted=True)
  filtered_elements = [song for song in songs if solid_client.exists(song.link)]
  serializer = SongSerializer(filtered_elements, many=True)
  return render(request, 'index.html', {'songs': serializer.data})

@csrf_exempt  
def songs_list(request):
  songs = Song.objects.filter(is_trusted=True)
  filtered_elements = [song for song in songs if solid_client.exists(song.link)]
  serializer = SongSerializer(filtered_elements, many=True)
  return JsonResponse(serializer.data, safe=False)

@custom_login_required
def playlists(request):
  storage_link = request.session['storage_link']
  trusted_playlists, some_missed_information = solid_client.fetch_playlists(storage_link)
  if(some_missed_information):
    messages.error(request, "There was some untrusted information which has been omitted from list", extra_tags='alert-danger')
  return render(request, 'playlists.html', {'list_of_playlists': trusted_playlists})

@custom_login_required
def playlist_songs(request, playlist_name):
  storage_link = request.session['storage_link']
  filtered_elements = Song.objects.filter(link__in=solid_client.playlist_songs(storage_link, playlist_name))
  serializer = SongSerializer(filtered_elements, many=True)
  songs = Song.objects.filter(is_trusted=True)
  filtered_songs = [song for song in songs if solid_client.exists(song.link)]
  library_songs_serializer = SongSerializer(filtered_songs, many=True)
  return render(request, 'edit_playlist.html', {'playlist_name': playlist_name, 'playlist_songs': serializer.data, 'songs': library_songs_serializer.data})

@custom_login_required
def create_playlist(request):
  if request.method == 'POST':
    form = PlaylistForm(request.POST)
    if form.is_valid():
      playlist_name = form.cleaned_data['name']
      solid_client.create_playlist(request.session['storage_link'], playlist_name)
      destination_url = reverse('playlist_songs', kwargs={'playlist_name': playlist_name})
      return redirect(destination_url)

    return render(request, 'create_playlist.html', {'form': form})
  else:
    return render(request, 'create_playlist.html', { 'form': PlaylistForm()})
    
@custom_login_required
def delete_playlist(request, playlist_name):
  storage_link = request.session['storage_link']
  solid_client.delete_playlist(storage_link, playlist_name)
  return redirect('/playlists/')

@custom_login_required
def song(request, song_id):
  song = Song.objects.get(id=song_id)
  if not song.is_trusted:
    messages.error(request, "This song seems to have some untrustworthy information and will not be included in the library", extra_tags='alert-danger')
  return render(request, 'song.html', {'song': song, 'artist': song.artist, 'artist_name':  request.session['user_name']})

@custom_login_required
def upload_song(request):
  if request.method == 'POST':
    form = SongUploadForm(request.POST, request.FILES)
    if form.is_valid():
      storage_link = request.session['storage_link']
      solid_client.upload(storage_link, form.cleaned_data['song_file'], form.cleaned_data['thumbnail'], form.cleaned_data['name'])
      return redirect('/my_songs/')
    else:
      return render(request, 'upload_song.html', { 'form': form})
  else:
    return render(request, 'upload_song.html', { 'form': SongUploadForm()})

@csrf_exempt
@custom_login_required
def delete_song(request, song_id):
  if request.method == 'DELETE':
    song = Song.objects.get(id=song_id)
    storage_link = request.session['storage_link']
    if song.artist.storage_url == storage_link:
      solid_client.delete_song(song)
      return JsonResponse({'message': 'Success!'})
    else:
      msg = "You don't have the permission to delete this song"
      return JsonResponse(msg, status=500)
  else:
    msg = "Request does not have the correct type."
    return JsonResponse(msg, status=500)

@custom_login_required
def add_to_playlist(request, song_id, playlist_name):
  song = Song.objects.get(id=song_id)
  solid_client.add_to_playlist(song, request.session['storage_link'], playlist_name)
  return redirect(request.META.get('HTTP_REFERER', '/'))

@custom_login_required
def remove_from_playlist(request, song_id, playlist_name):
  song = Song.objects.get(id=song_id)
  solid_client.remove_from_playlist(song, request.session['storage_link'], playlist_name)
  return redirect(request.META.get('HTTP_REFERER', '/'))

@custom_login_required
def my_songs(request):
  user = User.objects.get(storage_url=request.session['storage_link'])
  songs = user.song_set.all()
  filtered_elements = [song for song in songs if solid_client.exists(song.link)]
  serializer = SongSerializer(filtered_elements, many=True)
  return render(request, 'my_songs.html', {'songs': serializer.data})
