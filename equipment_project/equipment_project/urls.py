from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('admin/', admin.site.urls),
    # path('api/', include('api.urls')),
    path('auth/', include('users.urls')),
    path('auth/', include('django.contrib.auth.urls')),
    path('', include('web.urls')),
]

handler404 = 'core.views.page_not_found'
handler500 = 'core.views.server_errror'
handler403 = 'core.views.csrf_failure'
