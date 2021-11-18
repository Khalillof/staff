from django.db import models
from django.urls import reverse
from accounts.models import User
from agency.models import Office
import datetime
from django.utils import timezone
from capstone.helper import images_upload_directory

class PostCategory(models.Model):
    name = models.CharField(max_length=64)
    discription = models.CharField(max_length=64)
    created = models.DateTimeField(auto_now=True, blank=True)
    def __str__(self):
      return self.name

class Blog(models.Model):
    name = models.CharField(max_length=200)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    discription = models.TextField(max_length=700)
    created = models.DateTimeField(auto_now=True, blank=True)
    image = models.FileField(blank=True, null=True,verbose_name="Logo optional",upload_to=images_upload_directory)
    imgUrl = models.CharField(max_length=200, blank=True, null=True)
    archived = models.BooleanField(default=False) 
    office = models.ForeignKey(Office, on_delete=models.RESTRICT, blank=True, null=True)
    isPublic = models.BooleanField(default=False)

    def get_absolute_url(self):
        return reverse('Blog-detail', kwargs={'pk': self.pk})
    class Meta:
        ordering = ['created']

    def __str__(self):
      return self.name

class BlogPost(models.Model):
    title = models.CharField(max_length=200)
    discription = models.TextField()
    content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now=True, blank=True)
    pub_date = models.DateTimeField('date published', blank=True, null=True)
    edited = models.DateTimeField(auto_now=True, blank=True)
    isPublic = models.BooleanField(default=False)
    imgUrl = models.CharField(max_length=200, blank=True, null=True)
    image = models.FileField(blank=True, null=True,verbose_name="image optional",upload_to=images_upload_directory)
    postUrl = models.CharField(max_length=100, blank=True, null=True)
    archived = models.BooleanField(default=False) 
    category = models.ForeignKey(PostCategory, on_delete=models.RESTRICT, blank=True, null=True)
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE)
    
    def publish(self):
        self.isPuplic = True
        self.archived = False
        self.pub_date = timezone.now() 
        self.save()      
        return self
        
    def published_recently(self):
        return self.pub_date >= timezone.now() - datetime.timedelta(days=1)

    def get_absolute_url(self):
        return reverse('blogpost-detail', kwargs={'pk': self.pk})
    class Meta:
        ordering = ['created']

    def __str__(self):
        return self.title


class Comment(models.Model):
    content = models.TextField(max_length=600)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now=True, blank=True)
    blogPost = models.ForeignKey(BlogPost, on_delete=models.CASCADE)

    def get_absolute_url(self):
        return reverse('comment-detail', kwargs={'pk': self.pk})
    class Meta:
        ordering = ['created']

    def __str__(self):
        return f"User : {self.user}; ## Content : {self.content}; ## date : {self.datetime}"

