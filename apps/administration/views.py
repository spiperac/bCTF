from django.shortcuts import render
from django.urls import reverse_lazy
from django.http import HttpResponse
from django.views.generic import TemplateView, CreateView, UpdateView, DeleteView, ListView, DetailView, FormView, View
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from apps.challenges.models import Challenge, Category, Flag, Hint
from apps.administration.forms import FlagAddForm, HintAddForm, HintDeleteForm


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


class FlagsView(UserPassesTestMixin, DetailView):
        model = Challenge
        template_name = 'administration/settings/challenge/flags.html'

        def test_func(self):
                return self.request.user.is_staff


class FlagAddView(UserPassesTestMixin, FormView):
        form_class = FlagAddForm
        template_name = 'administration/settings/challenge/add_flag.html'

        def get_context_data(self, **kwargs):
                context = super(FlagAddView, self).get_context_data(**kwargs)
                context['challenge'] = Challenge.objects.get(pk=self.kwargs['pk'])
                return context

        def form_valid(self, form):
                challenge_id = form.cleaned_data['challenge_id']
                flag = form.cleaned_data['flag']
                challenge = Challenge.objects.get(pk=challenge_id)

                new_flag = Flag.objects.create(
                        challenge=challenge,
                        text=flag
                )

                return HttpResponse(status=204)

        def test_func(self):
                return self.request.user.is_staff


class HintsView(UserPassesTestMixin, DetailView):
        model = Challenge
        template_name = 'administration/settings/challenge/hints.html'

        def test_func(self):
                return self.request.user.is_staff


class HintAddView(UserPassesTestMixin, View):
        form_class = HintAddForm

        def post(self, request, *args, **kwargs):
                form = self.form_class(request.POST)
                if form.is_valid():
                        challenge_id = form.cleaned_data['challenge_id']
                        hint = form.cleaned_data['hint']
                        challenge = Challenge.objects.get(pk=challenge_id)

                        new_hint = Hint.objects.create(
                                challenge=challenge,
                                text=hint
                        )

                        return HttpResponse(status=204)
                else:
                        return HttpResponse(status=400)
                        
        def test_func(self):
                return self.request.user.is_staff


class HintDeleteView(UserPassesTestMixin, View):
        form_class = HintDeleteForm

        def post(self, request, *args, **kwargs):
                form = self.form_class(request.POST)
                if form.is_valid():
                        hint = form.cleaned_data['hint']
                        hint = Hint.objects.get(
                                pk=hint
                        )
                        hint.delete()

                        return HttpResponse(status=204)
                else:
                        return HttpResponse(status=400)

        def test_func(self):
                return self.request.user.is_staff