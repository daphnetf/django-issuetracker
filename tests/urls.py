from django.conf.urls import patterns, include, url


urlpatterns = patterns(
    '',
    url('^markdown/', include( 'django_markdown.urls')),
)
