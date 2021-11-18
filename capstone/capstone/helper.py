from django.core.exceptions import ImproperlyConfigured, ValidationError
from django.core.paginator import InvalidPage, Paginator
from django.db.models import QuerySet
#from django.views.generic.base import TemplateView, View
from django.views import View
from django.conf import settings
from django.shortcuts import render, redirect, HttpResponse, HttpResponseRedirect, Http404
from django.utils import timezone
#from django.urls import reverse
from django.utils.decorators import classonlymethod
from django.core.mail import BadHeaderError, EmailMessage
from django.template.loader import render_to_string

def get_exist(model, qs):
    try:
        item = model.objects.get(pk=qs)
    except model.DoesNotExist:
        item = None
    return item


def docs_upload_directory(instance, filename):
    url = f'upload/docs/{filename}'
    instance.fileUrl = url
    return url


def images_upload_directory(instance, filename):
    url = f"upload/images/{filename}"
    instance.imgUrl = url
    return url

def get_htmlstring(template_name,context):
    return render_to_string(template_name,context)

def user_upload_directory(instance, filename):
    return f'upload/users/{instance.user.username}_{instance.user.id}/{filename}'


def sendEmail(request, form):
    with EmailMessage.get_connection() as connected:
        subject = form.cleaned_data['subject']
        body = form.cleaned_data['body']
        from_email = form.cleaned_data['from_email']
        files = request.FILES.getlist('attachment')

        if subject and body and from_email:
            try:
                mail = EmailMessage(
                    subject=subject,
                    body=body,
                    from_email= from_email, 
                    reply_to=form.cleaned_data['recipients'], 
                    connection=connected
                    )
                if files is not None:
                    for f in files:
                        mail.attach(f.name, f.read(), f.content_type)
                mail.send()

            except BadHeaderError:
                return HttpResponse('Invalid header found.')
            connected.close()
            return HttpResponseRedirect('/thank/you')
        else:
            # In reality we'd use a form class
            # to get proper validation errors.
            return HttpResponse('Make sure all fields are entered and valid.')

class App_Paginator:

    allow_empty = True
    paginate_by = 9
    paginate_orphans = 0
    page_kwarg = "page"
    paginator_class = Paginator
    #request = None

    def paginate_queryset(self, queryset, page_size):
        """Paginate the queryset, if needed."""
        paginator = self.get_paginator(
            queryset, page_size, orphans=self.get_paginate_orphans(),
            allow_empty_first_page=self.get_allow_empty())
        page_kwarg = self.page_kwarg
        page = self.kwargs.get(
            page_kwarg) or self.request.GET.get(page_kwarg) or 1
        try:
            page_number = int(page)
        except ValueError:
            if page == 'last':
                page_number = paginator.num_pages
            else:
                raise Http404(
                    ('Page is not “last”, nor can it be converted to an int.'))
        try:
            page = paginator.page(page_number)
            return (paginator, page, page.object_list, page.has_other_pages())
        except InvalidPage as e:
            raise Http404(_('Invalid page (%(page_number)s): %(message)s') % {
                'page_number': page_number,
                'message': str(e)
            })

    def get_paginate_by(self, queryset):
        """
        Get the number of items to paginate by, or ``None`` for no pagination.
        """
        return self.paginate_by

    def get_paginator(self, queryset, per_page, orphans=0, allow_empty_first_page=True, **kwargs):
        """Return an instance of the paginator for this view."""
        return self.paginator_class(
            queryset, per_page, orphans=orphans,
            allow_empty_first_page=allow_empty_first_page, **kwargs)

    def get_paginate_orphans(self):
        """
        Return the maximum number of orphans extend the last page by when
        paginating.
        """
        return self.paginate_orphans

    def get_allow_empty(self):
        """
        Return ``True`` if the view should display empty lists and ``False``
        if a 404 should be raised instead.
        """
        return self.allow_empty

    def get_pager(self, queryset):

        page_size = self.get_paginate_by(queryset)
        if page_size:
            paginator, page, queryset, is_paginated = self.paginate_queryset(
                queryset, page_size)
            return {
                'paginator': paginator,
                'page_obj': page,
                'is_paginated': is_paginated,
                'object_list': queryset
            }
        else:
            return {
                'paginator': None,
                'page_obj': None,
                'is_paginated': False,
                'object_list': queryset
            }

    def get_custom_pager(self, queryset):
        page_size = self.get_paginate_by(queryset)
        if not page_size:
            return {
                "object_list": queryset,
                "is_paginated": False,
                "page": None
            }
        paginator, page, queryset, is_paginated = self.paginate_queryset(
            queryset, page_size)

        prev = 0
        next = 0
        cureent_page = 0
        next_disabled = "disabled"
        prev_disabled = "disabled"
        next_url = ""
        prev_url = ""

        path = self.request.path
        path_list = path.split("/")
        del path_list[0]

        if is_paginated:
            if page.has_next() == True:
                next = page.next_page_number()
                cureent_page = next - 1
                next_disabled = ""

                path_list[len(path_list)-1] = next
                for n in path_list:
                    next_url += "/"+str(n)
                next_url.strip()

            if page.has_previous() == True:
                prev = page.previous_page_number()
                cureent_page = prev + 1
                prev_disabled = ""

                path_list[len(path_list)-1] = prev
                for n in path_list:
                    prev_url += "/"+str(n)
                prev_url.strip()
        return {
            "object_list": queryset,
            "is_paginated": is_paginated,
            "page": {
                "next": next,
                "prev": prev,
                "next_disabled": next_disabled,
                "prev_disabled": prev_disabled,
                "next_url": next_url,
                "prev_url": prev_url,
                "num_pages": paginator.num_pages,
                "current_page": cureent_page,
            }
        }


class appview(View):
    title = None
    template_name = None
    extra_context = None
    context = {}

    def get_title(self):
        return self.title
    def get_extra_context(self):
        return self.extra_context
    
    def _init_once(self):
        self.context.update({'now': timezone.now(), 'title': self.get_title})
        if self.get_extra_context() is not None:
           self.context.update(self.get_extra_context())
        return render(self.request, self.template_name, context=self.context)

    def post(self, request, *args, **kwargs):
        return self._init_once()

    def get(self, request, *args, **kwargs):
        return self._init_once()


class template_page(appview):

    def get_title(self):
        _title = "title"
        if _title in self.kwargs:
            self.title = self.kwargs.get("title")
        return self.title


class AppListView(appview, App_Paginator):
    queryset = None
    model = None
    ordering = None
    require_login = False
    isfilter = None
    reverse = False
    #extra_context = None
    
    def get_isfilter(self):
        return self.isfilter

    def get_ordering(self):
        """Return the field or fields to use for ordering the queryset."""
        return self.ordering

    def get_queryset(self):
        if self.queryset is not None:
            queryset = self.queryset
            if isinstance(queryset, QuerySet):
                queryset = queryset.all()
        elif self.model is not None:
            queryset = self.model._default_manager.all()
            if self.get_isfilter() is not None:
                for xq in  self.isfilter:                   
                   queryset = queryset.filter(xq)
        else:
            raise ImproperlyConfigured(
                "%(cls)s is missing a QuerySet. Define "
                "%(cls)s.model, %(cls)s.queryset, or override "
                "%(cls)s.get_queryset()." % {
                    'cls': self.__class__.__name__
                }
            )
        ordering = self.get_ordering()
        if ordering:
            if isinstance(ordering, str):
                ordering = (ordering,)

            queryset = queryset.order_by(*ordering)
            if self.reverse is True:
               queryset = queryset.reverse()
                           

        return queryset

    def get(self, request, *args, **kwargs):
        if self.require_login:
            if not request.user.is_authenticated:
                return redirect('%s?next=%s' % (settings.LOGIN_URL, self.request.path))

        #if not self.template_name:
        #    self.template_name = "agency/home/index.html"

        self.context.update(self.get_custom_pager(self.get_queryset()))
        #self.context.update({'title': self.get_title})
        #self.context.update(self.get_extra_context())

        return self._init_once()

