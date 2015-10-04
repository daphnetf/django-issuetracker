from django.conf.urls import url
from issuetracker import views

urlpatterns = [
    url(r'^$', views.HomeView.as_view(), name='home'),
    url(r'^issues/(?P<pk>[0-9]+)/$', views.IssueView.as_view(), name='issue'),
    url(r'^issues/$', views.IssueListView.as_view(), name='issues'),
    url(r'^tags/$', views.TagListView.as_view(), name='tags'),
]
