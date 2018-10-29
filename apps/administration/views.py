from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import TemplateView, CreateView, UpdateView, DeleteView, ListView, FormView, View
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from apps.challenges.models import Challenge, Category, Flag, Hint

class IndexView(UserPassesTestMixin, TemplateView):
    template_name = 'administration/index.html'

    def test_func(self):
            return self.request.user.is_staff


class InformationsView(UserPassesTestMixin, TemplateView):
    template_name = 'administration/settings/informations.html'

    def test_func(self):
            return self.request.user.is_staff


class CTFView(UserPassesTestMixin, TemplateView):
    template_name = 'administration/settings/ctf.html'

    def test_func(self):
            return self.request.user.is_staff
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['challenges'] = Challenge.objects.all()
        context['categories'] = Category.objects.all()
        return context


class AddChallengeView(UserPassesTestMixin, CreateView):
    model = Challenge
    fields = '__all__'
    template_name = 'administration/settings/challenge/add_challenge.html'
    success_url = reverse_lazy('administration:ctf')

    def test_func(self):
            return self.request.user.is_staff

class UpdateChallengeView(UserPassesTestMixin, UpdateView):
    model = Challenge
    fields = '__all__'
    template_name = 'administration/settings/challenge/update_challenge.html'
    success_url = reverse_lazy('administration:ctf')

    def test_func(self):
            return self.request.user.is_staff

class DeleteChallengeView(UserPassesTestMixin, DeleteView):
    model = Challenge
    template_name = 'administration/settings/challenge/delete_challenge.html'
    success_url = reverse_lazy('administration:ctf')

    def test_func(self):
            return self.request.user.is_staff

class AddCategoryView(UserPassesTestMixin, CreateView):
    model = Category
    fields = '__all__'
    template_name = 'administration/settings/category/add_category.html'
    success_url = reverse_lazy('administration:ctf')

    def test_func(self):
            return self.request.user.is_staff

class UpdateCategoryView(UserPassesTestMixin, UpdateView):
    model = Category
    fields = '__all__'
    template_name = 'administration/settings/category/update_category.html'
    success_url = reverse_lazy('administration:ctf')

    def test_func(self):
            return self.request.user.is_staff

class DeleteCategoryView(UserPassesTestMixin, DeleteView):
    model = Category
    template_name = 'administration/settings/category/delete_category.html'
    success_url = reverse_lazy('administration:ctf')

    def test_func(self):
            return self.request.user.is_staff