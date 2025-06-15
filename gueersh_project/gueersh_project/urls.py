from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.shortcuts import redirect

admin.site.site_url = '/'

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('base.urls')),
    
    path('summernote/', include('django_summernote.urls')),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


def redirect_home(request):
    return redirect('/')

#URLs do Django Allauth:
urlpatterns += [
    #Bloqueio manual de URLs do Django Allauth:
    path('accounts/reauthenticate/', redirect_home),
    path('accounts/email/', redirect_home),
    path('accounts/password/change/', redirect_home),
    path('accounts/password/set/', redirect_home),
    path('accounts/signup/closed/', redirect_home),
    path('accounts/request-login-code/', redirect_home),
    path('accounts/confirm-login-code/', redirect_home),
    path('accounts/signup/by-passkey/', redirect_home),
    path('accounts/confirm-password-reset-code/', redirect_home),
    path('accounts/phone/change/', redirect_home),
    path('accounts/confirm-phone-verification-code/', redirect_home),
    
    path('accounts/', include('allauth.urls')),
]