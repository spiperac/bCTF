from django.shortcuts import render
from django.urls import reverse_lazy
from django.http import HttpResponse
from django.views.generic import TemplateView, CreateView, UpdateView, DeleteView, ListView, DetailView, FormView, View
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from apps.challenges.models import Challenge, Category, Flag, Hint, Attachment
from apps.administration.forms import FlagAddForm, HintAddForm, HintDeleteForm, FlagDeleteForm, AttachmentAddForm, AttachmentDeleteForm

class UserIsAdminMixin(UserPassesTestMixin):
        def test_func(self):
                return self.request.user.is_staff

class IndexView(UserIsAdminMixin, TemplateView):
        template_name = 'administration/index.html'


class InformationsView(UserIsAdminMixin, TemplateView):
        template_name = 'administration/settings/informations.html'


class CTFView(UserIsAdminMixin, TemplateView):
        template_name = 'administration/settings/ctf.html'
        
        def get_context_data(self, **kwargs):
                context = super().get_context_data(**kwargs)
                context['challenges'] = Challenge.objects.all()
                context['categories'] = Category.objects.all()
                return context


class AddChallengeView(UserIsAdminMixin, CreateView):
        model = Challenge
        fields = '__all__'
        template_name = 'administration/settings/challenge/add_challenge.html'
        success_url = reverse_lazy('administration:ctf')

class UpdateChallengeView(UserIsAdminMixin, UpdateView):
        model = Challenge
        fields = '__all__'
        template_name = 'administration/settings/challenge/update_challenge.html'
        success_url = reverse_lazy('administration:ctf')


class DeleteChallengeView(UserIsAdminMixin, DeleteView):
        model = Challenge
        template_name = 'administration/settings/challenge/delete_challenge.html'
        success_url = reverse_lazy('administration:ctf')


class AddCategoryView(UserIsAdminMixin, CreateView):
        model = Category
        fields = '__all__'
        template_name = 'administration/settings/category/add_category.html'
        success_url = reverse_lazy('administration:ctf')


class UpdateCategoryView(UserIsAdminMixin, UpdateView):
        model = Category
        fields = '__all__'
        template_name = 'administration/settings/category/update_category.html'
        success_url = reverse_lazy('administration:ctf')


class DeleteCategoryView(UserIsAdminMixin, DeleteView):
        model = Category
        template_name = 'administration/settings/category/delete_category.html'
        success_url = reverse_lazy('administration:ctf')


class FlagsView(UserIsAdminMixin, DetailView):
        model = Challenge
        template_name = 'administration/settings/challenge/flags.html'


class FlagAddView(UserIsAdminMixin, FormView):
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


class FlagDeleteView(UserIsAdminMixin, View):
        form_class = FlagDeleteForm

        def post(self, request, *args, **kwargs):
                form = self.form_class(request.POST)
                if form.is_valid():
                        flag = form.cleaned_data['flag']
                        flag = Flag.objects.get(
                                pk=flag
                        )
                        flag.delete()

                        return HttpResponse(status=204)
                else:
                        return HttpResponse(status=400)


class HintsView(UserIsAdminMixin, DetailView):
        model = Challenge
        template_name = 'administration/settings/challenge/hints.html'


class HintAddView(UserIsAdminMixin, View):
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


class HintDeleteView(UserIsAdminMixin, View):
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


class AttachmentsView(UserIsAdminMixin, DetailView):
        model = Challenge
        template_name = 'administration/settings/challenge/attachments.html'


class AttachmentAddView(UserIsAdminMixin, View):
        form_class = AttachmentAddForm

        def post(self, request, *args, **kwargs):
                form = self.form_class(data=request.POST, files=request.FILES)
                if form.is_valid():
                        challenge_id = form.cleaned_data['challenge_id']
                        attachment = form.cleaned_data['data']
                        challenge = Challenge.objects.get(pk=challenge_id)

                        new_attachment = Attachment.objects.create(
                                challenge=challenge,
                                data=attachment
                        )

                        return HttpResponse(status=204)
                else:
                        return HttpResponse(status=400)


class AttachmentDeleteView(UserIsAdminMixin, View):
        form_class = AttachmentDeleteForm

        def post(self, request, *args, **kwargs):
                form = self.form_class(request.POST)
                if form.is_valid():
                        attachment = form.cleaned_data['attachment']
                        attachment = Attachment.objects.get(
                                pk=attachment
                        )
                        attachment.delete()

                        return HttpResponse(status=204)
                else:
                        return HttpResponse(status=400)