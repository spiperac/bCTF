from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import CreateView, DetailView, ListView, DeleteView, UpdateView
from apps.pages.models import Page
from config.themes import get_theme_url


class UserIsAdminMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_staff


class PageView(DetailView):
    model = Page

    def get_template_names(self):
        return list(['templates/pages/page.html'])


class PageCreateView(UserIsAdminMixin, LoginRequiredMixin, CreateView):
    model = Page
    fields = '__all__'
    template_name = 'templates/pages/create_page.html'
    success_url = reverse_lazy('pages:list-pages')


class PageUpdateView(UserIsAdminMixin, LoginRequiredMixin, UpdateView):
    model = Page
    fields = '__all__'
    template_name = 'templates/pages/update_page.html'
    success_url = reverse_lazy('pages:list-pages')


class PageListView(UserIsAdminMixin, LoginRequiredMixin, ListView):
    model = Page
    template_name = 'templates/pages/list_pages.html'

    def get_context_data(self, **kwargs):
        context = super(PageListView, self).get_context_data(**kwargs)
        try:
            context['latest'] = Page.objects.all().latest().created_on
        except Page.DoesNotExist:
            context['latest'] = None
        return context


class PageDeleteView(UserIsAdminMixin, LoginRequiredMixin, DeleteView):
    model = Page
    success_url = reverse_lazy('pages:list-pages')

    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)
