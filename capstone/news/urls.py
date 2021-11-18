from django.urls import path

from . import views
# API Routes

app_name = 'news'
urlpatterns = [
    path("<int:page>", views.PostList.as_view(), name="index"),
    path("blogs/<int:page>", views.BlogList.as_view(), name="blogs"),
    #path('posts/<int:category_id>/<int:page>', views.PostsCategory.as_view(), name='posts_category-list'),
    path('blog/detail/<int:pk>/', views.BlogDetail.as_view(), name='blog-detail'),
    path('blog/add/',views.BlogCreate.as_view(), name='blog-add'),
    path('blog/update/<int:pk>/', views.BlogUpdate.as_view(), name='blog-update'),
    path('blog/delete/<int:pk>/', views.BlogDelete.as_view(), name='blog-delete'),

    path("posts/<int:page>", views.PostList.as_view(), name="posts"),
    path('posts/<int:category_id>/<int:page>', views.PostCategory_View.as_view(), name='posts_category-list'),
    path('post/detail/<int:pk>/', views.PostDetail.as_view(), name='post-detail'),
    path('post/add/',views.PostCreate.as_view(), name='post-add'),
    path('post/update/<int:pk>/', views.PostUpdate.as_view(), name='post-update'),
    path('post/delete/<int:pk>/', views.PostDelete.as_view(), name='post-delete'),

]