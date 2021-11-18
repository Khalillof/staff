from django.contrib import admin
from news.models import Blog, PostCategory, BlogPost, Comment
# Register your models here.

class NewsAdmin(admin.ModelAdmin):
    #formfield_overrides = {
    #    PostCategory.TextField: {'widget': QuillEditorWidget},
    #}

    """
    class Media:

        js = (
             'agency/plugins/jquery/jquery.min.js', # jquery
            'agency/plugins/summernote/summernote-bs4.min.js',   
            'agency/js/html.js', 
        )
        css = {
           'all': ('agency/plugins/summernote/summernote-bs4.min.css',)
        }
    """
#news
admin.site.register(Blog)
admin.site.register(BlogPost, NewsAdmin)

admin.site.register(PostCategory)
admin.site.register(Comment)