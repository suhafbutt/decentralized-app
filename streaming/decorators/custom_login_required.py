from functools import wraps
from django.http import HttpResponseForbidden
from django.shortcuts import redirect
from django.contrib import messages

def custom_login_required(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
      if 'storage_link' in request.session:
        return view_func(request, *args, **kwargs)
      else:
        messages.error(request, 'You need to provide the storage location', extra_tags='alert-danger')
        return redirect('/storage/')
    return wrapper
