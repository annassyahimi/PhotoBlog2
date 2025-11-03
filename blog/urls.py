from django.urls import path, include
from . import views
from rest_framework import routers
from .views import UploadView, PhotoListView


router = routers.DefaultRouter()
router.register('Post', views.blogImage)

urlpatterns=[
    path('',views.post_list,name='post_list'),
    path('post/<int:pk>/', views.post_detail, name='post_detail'),
    path('post/new/', views.post_new, name='post_new'),
    path('post/<int:pk>/edit/', views.post_edit, name='post_edit'),
    path('js_test/', views.js_test, name='js_test'),
    path('upload/', views.UploadView.as_view(), name='upload'),
    path('upload/', UploadView.as_view(), name='upload'),
    path('photos/', PhotoListView.as_view(), name='photos'),

]