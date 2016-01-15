from django.conf.urls import url
from issuetracker import views

urlpatterns = [
    url(r'^$', views.ProjectDetailView.as_view(), name='project'),
    url(r'^issues/(?P<issue>[0-9]+)/(?P<pk>[0-9]+)/$', views.IssueCommentUpdateView.as_view(), name='issuecomment_update'),
    url(r'^issues/(?P<pk>[0-9]+)/close/$', views.IssueCloseView.as_view(), name='issue_close'),
    url(r'^issues/(?P<pk>[0-9]+)/open/$', views.IssueOpenView.as_view(), name='issue_open'),
    url(r'^issues/(?P<pk>[0-9]+)/update/$', views.IssueUpdateView.as_view(), name='issue_update'),
    url(r'^issues/(?P<pk>[0-9]+)/meta/$', views.IssueMetaUpdateView.as_view(), name='issue_update_meta'),
    url(r'^issues/(?P<pk>[0-9]+)/$', views.IssueDetailView.as_view(), name='issue'),
    url(r'^issues/new/$', views.IssueCreateView.as_view(), name='new_issue'),
    url(r'^issues/$', views.IssueListView.as_view(), name='issues'),
    url(r'^tags/(?P<pk>[0-9]+)/update/$', views.TagUpdateView.as_view(), name='tag_update'),
    url(r'^tags/(?P<pk>[0-9]+)/$', views.TagDetailView.as_view(), name='tag'),
    url(r'^tags/new/$', views.TagCreateView.as_view(), name='new_tag'),
    url(r'^tags/$', views.TagListView.as_view(), name='tags'),
    url(r'^search/(?P<needle>.*)/$', views.SearchResultView.as_view(), name='search_result'),
    url(r'^search/$', views.SearchView.as_view(), name='search'),
]
