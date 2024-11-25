def set_user_name(request):
  user_name = ''
  if 'storage_link' in request.session:
    if 'user_name' in request.session:
      user_name = request.session['user_name']
  
  return {'user_name': user_name}
