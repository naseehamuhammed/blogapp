
from django.shortcuts import render
from django.utils import timezone
from django.db.models import Count, Q
from rest_framework import generics, status
from rest_framework.exceptions import ValidationError as DjangoValidationError
from rest_framework.response import Response
from .models import Blog, Author, Category
from .serializers import BlogCreateSerializer, AuthorCreateSerializer, BlogSerializer, BlogDetailSerializer, AuthorSerializer, CategorySerializer
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404


Author = get_user_model()

class BlogCreateAPIView(generics.CreateAPIView):
    queryset = Blog.objects.all()
    serializer_class = BlogCreateSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
            blog = serializer.save()
 
            if blog.is_published:
                message = "Blog post has been published successfully."
            else:
                message = "Blog post has been saved as a draft."
 
            return Response(
                {"message": message, "blog": serializer.data},
                status=status.HTTP_201_CREATED
            )
        except Exception as e:
            return Response(
                {"message": "An error occurred.", "errors": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

class AuthorCreateAPIView(generics.CreateAPIView):
    queryset = Author.objects.all()
    serializer_class = AuthorCreateSerializer

class CategoryCreateAPIView(generics.CreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

class BlogListAPIView(generics.ListAPIView):
    queryset = Blog.objects.filter(is_published=True)
    serializer_class = BlogSerializer

class BlogDetailAPIView(generics.ListAPIView):
    from rest_framework.generics import RetrieveAPIView
from .models import Blog
from .serializers import BlogSerializer

class BlogDetailAPIView(generics.ListAPIView):
    queryset = Blog.objects.all()
    serializer_class = BlogSerializer  # Specify the serializer class here
 
       
class TopAuthorsAPIView(generics.ListAPIView):
    serializer_class = AuthorSerializer

    def get_queryset(self):
        # Get top 3 authors with the most posts in the last 6 months
        six_months_ago = timezone.now() - timezone.timedelta(days=180)
        return Author.objects.annotate(
            num_posts=Count('blogs', filter=Q(blogs__publish_date__gte=six_months_ago))
        ).order_by('-num_posts')[:3]

class PopularCategoryAPIView(generics.ListAPIView):
    serializer_class = CategorySerializer

    def get_queryset(self):
        six_months_ago = timezone.now() - timezone.timedelta(days=180)
        return (
            Category.objects.annotate(num_blogs=Count('blog'))
            .filter(blog__publish_date__gte=six_months_ago)
            .order_by('-num_blogs')[:1]
        )

class DraftListAPIView(generics.ListAPIView):
    queryset = Blog.objects.filter(is_published=False)  # Filter for drafts
    serializer_class = BlogSerializer  # Use the serializer to format the output
 
    def get(self, request, *args, **kwargs):
        drafts = self.get_queryset()
        serializer = self.get_serializer(drafts, many=True)
        return Response(serializer.data)
