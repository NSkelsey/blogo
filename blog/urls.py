from django.conf.urls import patterns, include, url
from blog import views as bviews

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', bviews.home,),
    url(r'create$', bviews.create_user),
    url(r'login$', bviews.login),
    url(r'^secret/home$', bviews.logged_in),
    url(r'logout$', bviews.logout),
    url(r'^submit_post$', bviews.post_sub),
    url(r'^posts/(?P<id_num>\d+)$', bviews.show_post),
    url(r'^posts/(?P<id_num>\d+)/edit$', bviews.edit_post),
    url(r'^posts/(?P<id_num>\d+)/delete$', bviews.delete_post),
    url(r'^user/(?P<name>\S+)$', bviews.user_page),
    url(r'^users$', bviews.users),
    url(r'^freespeech$', bviews.freedom),
)
