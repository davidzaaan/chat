from django.contrib import admin
from django.urls import path, include
# production
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('users.urls')),
    path('chat/', include('chat.urls')),
]

# for production purposes...
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)