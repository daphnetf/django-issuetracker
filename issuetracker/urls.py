from django.conf.urls import url
from issuetracker import views

urlpatterns = [
    url(r'^$', views.HomeView.as_view(), name='home'),
    url(r'^issues/$', views.IssueListView.as_view(), name='issues'),
    url(r'^tags/$', views.TagListView.as_view(), name='tags'),
]
