from django.contrib import admin
from django.urls import path
from django.http import HttpResponse
from .api import api

# halaman root biar nggak 404
def home(request):
    return HttpResponse("API is running 🚀")

urlpatterns = [
    path('', home),              # http://127.0.0.1:8000/
    path('admin/', admin.site.urls),
    path('api/', api.urls),      # http://127.0.0.1:8000/api/docs
]