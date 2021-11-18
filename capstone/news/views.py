from django.shortcuts import render
from django.views.generic import detail, edit
from .models import Blog, BlogPost, PostCategory
from .newsforms import BlogForm, BlogPostForm, CategoryForm
from django.utils import timezone
from django.contrib.auth.mixins import LoginRequiredMixin
from capstone.helper import get_exist, AppListView

# Create your views here.

def index(request):
    
    return render(request, "news/index.html")

####################################################### Blog

class BlogList(AppListView):
    model = Blog
    title = "Blog list"
    ordering ="created"
    template_name="news/list.html"
    reverse = True

class BlogDetail(detail.DetailView):
    model = Blog
    template_name="news/detail.html"

    def get_object(self):
        obj = get_exist(Blog,self.kwargs["pk"])
        self.extra_context= {"title": obj.name}
        return obj
    
class BlogCreate(LoginRequiredMixin,edit.CreateView):
    #title = "Create new Blog"
    model = Blog
    template_name="shared/create_update.html"
    form_class = BlogForm
    success_url = "/news/blogs/1"

    def get_initial (self):
        self.extra_context = {"title":"Create new Blog", "html":True}
        return {'author': self.request.user.id}
       
class BlogUpdate(LoginRequiredMixin, edit.UpdateView):
    model = Blog 
    template_name="shared/create_update.html"
    form_class = BlogForm
    success_url = "/news/blogs/1"

    def get_object(self):
        obj = get_exist(Blog,self.kwargs["pk"])
        self.extra_context= {"title": obj.name, "html":True}
        return obj

class BlogDelete(LoginRequiredMixin, edit.DeleteView):
    model = Blog
    title ="Delete Blog"
    template_name="news/delete.html"
    success_url = "/news/blogs/1"

################################################################# Posts

class PostList(AppListView):
    model = BlogPost
    title = "Posts"
    ordering ="created"
    template_name="news/post/list.html"
    extra_context = {'categories': PostCategory.objects.all().order_by("created")}
    isfilter = [('isPublic',True)]
    reverse = True

class PostCategory_View(AppListView):
    model = BlogPost
    ordering ="created"
    template_name="news/post/list.html"
    extra_context = {'categories': PostCategory.objects.all().order_by("created")}
    isfilter = [('isPublic',True)]
    reverse = True

    def get_title(self):
        cat_id = self.kwargs["category_id"]
        data_num = BlogPost.objects.filter(category=cat_id).count()
        cat = get_exist(PostCategory, cat_id)         
        self.title = f"posts for categoy : {cat.name} { str(data_num)}  found"
        return self.title

    def get_queryset(self):
        return BlogPost.objects.filter(category=self.kwargs["category_id"])

class PostDetail(detail.DetailView):
    model = BlogPost
    template_name="news/post/detail.html"

    def get_object(self):
        obj = get_exist(BlogPost,self.kwargs["pk"])
        self.title = obj.title
        return obj    
    
class PostCreate(LoginRequiredMixin,edit.CreateView):
    #title = "Create new Post"
    model = BlogPost
    template_name="shared/create_update.html"
    form_class = BlogPostForm
    success_url = "/news/posts/1"

    def get_initial (self):
        self.extra_context = {"title":"Create new Post", "html":True}
        return {'author': self.request.user.id}
 
class PostUpdate(LoginRequiredMixin, edit.UpdateView):
    model = BlogPost 
    template_name="shared/create_update.html"
    form_class = BlogPostForm
    success_url = "/news/posts/1"
    

    def get_object(self):
        obj = get_exist(BlogPost,self.kwargs["pk"])
        self.extra_context = {"title":obj.title, "html":True} 
        return obj 

class PostDelete(LoginRequiredMixin, edit.DeleteView):
    model = BlogPost
    title ="Delete Post"
    template_name="news/post/delete.html"
    success_url = "/news/posts/1"
