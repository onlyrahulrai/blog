from django.urls import path

from . import views

urlpatterns = [
    path('', views.home, name="home"),
    path('post/new/', views.postCreate, name="post-create"),
    path('post/<str:pk>/', views.postDetail, name="post-detail"),
    path('post/<str:pk>/update/', views.postUpdate.as_view(), name="post-update"),
    path('post/<str:pk>/delete/', views.postDelete.as_view(), name="post-delete"),
    path('users/<str:name>/', views.postUser, name="post-user"),
    path('category/<str:name>/', views.postCategory, name="post-category"),
    path('search/', views.postSearch, name="search"),

    path('post/<str:pk>/comment', views.comment, name="comment"),
]
