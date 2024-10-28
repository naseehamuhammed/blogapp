from rest_framework import serializers
from .models import Blog, Author, Category

class BlogCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Blog
        fields = ['title', 'content', 'author', 'category', 'is_published']


class AuthorCreateSerializer(serializers.ModelSerializer):
    num_blogs = serializers.IntegerField(read_only=True)

    class Meta:
        model = Author  # Use your custom Author model
        fields = ['username', 'password', 'email', 'bio', 'contact_info', 'num_blogs']

    def get_num_blogs(self, obj):
        # Return the count of blogs associated with the author
        return obj.blogs.count()  # Use related_name defined in Blog model

    def create(self, validated_data):
        # Handle password securely
        password = validated_data.pop('password')
        author = Author(**validated_data)
        author.set_password(password)
        author.save()
        return author


class BlogSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField()

    class Meta:
        model = Blog
        fields = ['title', 'content', 'author', 'category', 'is_published', 'publish_date']
        read_only_fields = ['publish_date']


class BlogDetailSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField()

    class Meta:
        model = Blog
        fields = ['title', 'content', 'author', 'publish_date', 'is_published', 'category']


class AuthorSerializer(serializers.ModelSerializer):
    num_posts = serializers.IntegerField()
 
    class Meta:
        model = Author
        fields = ['username', 'num_posts']

class CategorySerializer(serializers.ModelSerializer):
    num_blogs = serializers.IntegerField(read_only=True)  

    class Meta:
        model = Category
        fields = ['name', 'description', 'num_blogs']

    
    def create(self, validated_data):
        # Remove num_blogs from validated_data to avoid the TypeError
        validated_data.pop('num_blogs', None)
        return Category.objects.create(**validated_data)