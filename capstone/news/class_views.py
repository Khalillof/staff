
from django.views.generic import detail, list, edit
from django.utils import timezone
from .models import  Blog,BlogPost,Comment, PostCategory
from django.contrib.auth.mixins import LoginRequiredMixin
from news.newsforms import BlogPostForm, BlogForm, CategoryForm

########### adverts views

class BlogPostList(list.ListView):
    model =BlogPost
    paginate_by = 10  # if pagination is desired
    template_name="news/blog/posts/index.html"
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['now'] = timezone.now()
        context['object_list'] = BlogPost.objects.filter(isPuplic=True).order_by("created")
        context['categories'] = PostCategory.objects.all()
        return context

class BlogPostDetail(detail.DetailView):
    model = BlogPost
    template_name="news/blog/posts/detail.html"
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['now'] = timezone.now()
        return context


class BlogPostCreate(LoginRequiredMixin, edit.CreateView):
    model = BlogPost
    template_name="news/Blog/posts/create.html"
    form_class = BlogPostForm
    #success_url = reverse(viewname="agency:thank-you", args={"message":"Yor application successfully created"})

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    
class BlogPostUpdate(LoginRequiredMixin, edit.UpdateView):
    model = BlogPost 
    template_name="news/blog/posts/update.html"
    form_class = BlogPostForm
    #fields = ['cover_letter', 'cv' 'Address']
    #success_url = reverse(viewname="agency:thank-you", args={"message":"Yor application successfully updated"})

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    
class BlogPostDelete(LoginRequiredMixin, edit.DeleteView):
    model = BlogPost
    template_name="news/blog/posts/delete.html"
    #success_url = reverse(viewname="agency:thank-you", args={"message":"Yor application successfully deleted"})

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)
    
################ Blog  views
class BlogList(list.ListView):
    model = Blog
    paginate_by = 10  # if pagination is desired
    template_name="news/blog/list.html"
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['now'] = timezone.now()
        return context

# BlogPost_catergory list
class BlogDetail(detail.DetailView):
    model = Blog
    template_name="news/blog/detail.html"
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['now'] = timezone.now()
        return context
    

class BlogCreate(LoginRequiredMixin, edit.CreateView):
    model = Blog
    template_name="news/Blog/create.html"
    form_class = BlogForm
    #success_url = reverse(viewname="agency:thank-you", args={"message":"Yor application successfully created"})

    def form_valid(self, form):
        form.instance.author = self.request.user
        advert_id = self.get("advert_id")
        return super().form_valid(form)

    
class BlogUpdate(LoginRequiredMixin, edit.UpdateView):
    model = Blog 
    template_name="news/blog/update.html"
    form_class = BlogForm
    #success_url = reverse(viewname="agency:thank-you", args={"message":"Yor application successfully updated"})

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    
class BlogDelete(LoginRequiredMixin, edit.DeleteView):
    model = Blog
    template_name="news/blog/delete.html"
    #success_url = reverse(viewname="agency:thank-you", args={"message":"Yor application successfully deleted"})

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

################### catregories

# Post category list
class CategoryList(list.ListView):
    model = BlogPost
    paginate_by = 9  # if pagination is desired
    template_name="news/blog/category/index.html"
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['now'] = timezone.now()
        context['object_list'] = BlogPost.objects.filter(category=self.request.get("category_id")).order_by("created")
        context['categories'] = PostCategory.objects.all()
        return context

class CategoryCreate(LoginRequiredMixin, edit.CreateView):
    model = PostCategory
    template_name="news/Blog/Category/create.html"
    form_class = CategoryForm
    #success_url = reverse(viewname="agency:thank-you", args={"message":"Yor application successfully created"})


    
class CategoryUpdate(LoginRequiredMixin, edit.UpdateView):
    model = Blog 
    template_name="news/blog/category/update.html"
    form_class = CategoryForm

    
class CategocyDelete(LoginRequiredMixin, edit.DeleteView):
    model = Blog
    template_name="news/blog/category/delete.html"
    #success_url = reverse(viewname="agency:thank-you", args={"message":"Yor application successfully deleted"})

    
    

    

    
    