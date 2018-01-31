from django.conf.urls import url, include
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic.base import RedirectView

from .views import *

urlpatterns = [
                  url(r'^', include('staff_panel.urls')),
                  url(r'^admin/', admin.site.urls),
                  url(r'^login/', RedirectView.as_view(url='/accounts/login/', permanent=True), name='login'),
                  url(r'^logout/', RedirectView.as_view(url='/accounts/logout/', permanent=True), name='logout'),
              ] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) \
              + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
