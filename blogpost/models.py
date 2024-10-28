

from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from django.core.exceptions import ValidationError


from django.db.models import Count
from textstat import textstat 
import re


# models.py


class Author(AbstractUser):
    bio = models.TextField(blank=True, null=True)
    contact_info = models.CharField(max_length=255, blank=True, null=True)

    # Resolve clashes by specifying unique related names
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='author_groups',
        blank=True,
        help_text="The groups this user belongs to."
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='author_user_permissions',
        blank=True,
        help_text="Specific permissions for this user."
    )


# Category model
class Category(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField()
    date_created = models.DateTimeField(auto_now_add=True)

    def _str_(self):
        return self.name

# Blog model with required fields and validations
class Blog(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name='blogs')
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    is_published = models.BooleanField(default=False)
    publish_date = models.DateTimeField(blank=True, null=True)

    # Forbidden words list
    FORBIDDEN_WORDS = ["free money", "win cash", "cocaine", "heroin", "kill", "bomb", "attack", "terrorist", "click here"]

    def save(self, *args, **kwargs):
        # Validation: Content length for Draft status
        if len(self.content) < 500:
            self.is_published = False
        elif len(self.content) >= 500: 
            #raise ValidationError("Content over 500 characters cannot be categorized as Draft.")
            self.is_published = True
            self.publish_date = timezone.now()

        # Validation: Flesch Reading Ease for General category
        if self.category.name.lower() == "general" and self.is_published:
            readability_score = textstat.flesch_reading_ease(self.content)
            if readability_score < 30:
                raise ValidationError("Flesch Reading Ease score must be at least 30 for the General category.")

        # Validation: Plagiarism check for similar content by same author
        similar_posts = Blog.objects.filter(author=self.author).exclude(id=self.id)
        for post in similar_posts:
            similarity_ratio = self.calculate_similarity(self.content, post.content)
            if similarity_ratio > 0.6:
                raise ValidationError("Content similarity with other posts exceeds 60%. This is considered plagiarism.")

        # Validation: Forbidden words
        for word in self.FORBIDDEN_WORDS:
            if re.search(r'\b' + re.escape(word) + r'\b', self.content, re.IGNORECASE):
                raise ValidationError(f"The content contains forbidden words: {word}")

        # Validation: Author monthly post limit
        current_month_posts = Blog.objects.filter(
            author=self.author,
            publish_date__year=timezone.now().year,
            publish_date__month=timezone.now().month
        ).count()
        if current_month_posts >= 5:
            raise ValidationError("Authors are limited to publishing 5 posts per month.")

        super().save(*args, **kwargs)

    # Helper function for content similarity check
    def calculate_similarity(self, content1, content2):
        return len(set(content1.split()).intersection(set(content2.split()))) / max(len(content1.split()), len(content2.split()))

    def _str_(self):
        return self.title