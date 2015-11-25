from django.conf.urls import url
from issuetracker import views

urlpatterns = [
    url(r'^$', views.HomeView.as_view(), name='home'),
    url(r'^issues/(?P<ipk>[0-9]+)/(?P<pk>[0-9]+)/$', views.IssueActionUpdateView.as_view(), name='issueaction_update'),
    url(r'^issues/(?P<pk>[0-9]+)/update/$', views.IssueUpdateView.as_view(), name='issue_update'),
    url(r'^issues/(?P<pk>[0-9]+)/meta/$', views.IssueMetaUpdateView.as_view(), name='issue_update_meta'),
    url(r'^issues/(?P<pk>[0-9]+)/$', views.IssueDetailView.as_view(), name='issue'),
    url(r'^issues/new/$', views.IssueCreateView.as_view(), name='new_issue'),
    url(r'^issues/$', views.IssueListView.as_view(), name='issues'),
    url(r'^tags/(?P<pk>[0-9]+)/$', views.TagDetailView.as_view(), name='tag'),
    url(r'^tags/new/$', views.TagCreateView.as_view(), name='new_tag'),
    url(r'^tags/$', views.TagListView.as_view(), name='tags'),
    url(r'^search/(?P<needle>.*)/$', views.SearchResultView.as_view(), name='search_result'),
    url(r'^search/$', views.SearchView.as_view(), name='search'),
]
