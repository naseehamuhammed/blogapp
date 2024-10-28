from django.urls import path
from .views import BlogListAPIView, BlogDetailAPIView, TopAuthorsAPIView, PopularCategoryAPIView, BlogCreateAPIView, AuthorCreateAPIView, CategoryCreateAPIView,DraftListAPIView

urlpatterns = [
    path('api/blogs/', BlogListAPIView.as_view(), name='blog-list'),
    path('api/top-authors/', TopAuthorsAPIView.as_view(), name='top-authors'),
    path('api/popular-category/', PopularCategoryAPIView.as_view(), name='popular-category'),
    path('api/blogs/create/', BlogCreateAPIView.as_view(), name='blog-create'),
    path('api/blogs/createauthor/', AuthorCreateAPIView.as_view(), name='author-create'),
    path('api/blogs/createcategory/', CategoryCreateAPIView.as_view(), name='category-create'),
    path('api/drafts/', DraftListAPIView.as_view(), name='draft-list'),
    path('api/blog-details/', BlogDetailAPIView.as_view(), name='blog-details'),
]