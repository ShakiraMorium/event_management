from django.contrib import admin
from django.urls import path, include
from events.views import home_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home_view, name='home'),  # root path shows homepage
    path('events/', include('events.urls')),
]
