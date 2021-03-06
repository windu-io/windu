"""windu URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import include, url
from django.contrib import admin
from django.contrib import auth

from oauth2_provider.views import base

urlpatterns = [
    url(r'^api/', include('chat.urls')),
    url(r'^admin/', admin.site.urls),
#    url(r'^o/', include('oauth2_provider.urls', namespace='oauth2_provider')),
    url(r'^accounts/login/$', auth.views.login, {'template_name': 'admin/login.html'}),
    url(r'^accounts/logout/$', auth.views.logout, {'template_name': 'admin/logout.html'}),
    url(r'^o/token/$', base.TokenView.as_view(), name="token"),
    url(r'^o/revoke-token/$', base.RevokeTokenView.as_view(), name="revoke-token")

]
