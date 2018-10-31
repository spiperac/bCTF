import json
from django.shortcuts import render
from django.urls import reverse_lazy
from django.db.models import Count
from django.http import HttpResponse
from django.views.generic import TemplateView, CreateView, UpdateView, DeleteView, ListView, DetailView, FormView, View
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from apps.accounts.models import Account
from apps.challenges.models import Challenge, Category, Flag, Hint, Attachment, Solves, FirstBlood
from apps.administration.forms import FlagAddForm, HintAddForm, HintDeleteForm, FlagDeleteForm, AttachmentAddForm, AttachmentDeleteForm, \
                                        DockerActionForm, DockerImageActionForm
from apps.administration.docker_utils import DockerTool


class UserIsAdminMixin(UserPassesTestMixin):
        def test_func(self):
                return self.request.user.is_staff

class IndexView(UserIsAdminMixin, TemplateView):
        template_name = 'administration/index.html'


class InformationsView(UserIsAdminMixin, TemplateView):
        template_name = 'administration/settings/informations.html'

        def get_context_data(self, **kwargs):
                context = super().get_context_data(**kwargs)
                context['challenges'] = Challenge.objects.all()
                context['categories'] = Category.objects.all()

                chall_stats = []
                total_challs = context['challenges'].count()
                solved_challs = Solves.objects.values('challenge__pk').distinct().count()
                unsolved_challs = int(total_challs) - int(solved_challs)

                accounts = Account.objects.all()
                account_stats = []
                total_accounts = accounts.count()
                accounts_with_points = [x for x in accounts if x.points > 0]
                accounts_with_zero = total_accounts - len(accounts_with_points)
                account_stats.append(len(accounts_with_points))
                account_stats.append(accounts_with_zero)

                first_bloods = FirstBlood.objects.all().values_list('account__username', flat=True).distinct()
                first_blood_accounts = [x for x in first_bloods]
                first_blood_data = []
                for account in first_blood_accounts:
                        solved = FirstBlood.objects.filter(account__username=account).count()
                        first_blood_data.append(solved)

                chall_stats.append(solved_challs)
                chall_stats.append(unsolved_challs)
                context['first_bloods_labels'] = first_blood_accounts
                context['first_bloods_data'] = first_blood_data
                context['chall_stats'] = chall_stats
                context['account_stats'] = account_stats
                context['accounts'] = accounts
                context['challenges'] = Challenge.objects.all()
                return context

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


class AccountsView(UserIsAdminMixin, ListView):
        model = Account
        context_object_name = 'accounts'
        template_name = 'administration/settings/accounts.html'


class UpdateAccountView(UserIsAdminMixin, UpdateView):
        model = Account
        fields = ['username', 'email', 'password', 'is_staff', 'is_superuser', 'is_active', 'banned']
        template_name = 'administration/settings/account/update_account.html'
        success_url = reverse_lazy('administration:list-accounts')


class ToggleAccountStateView(UserIsAdminMixin, UpdateView):
        model = Account
        fields = ['is_active']
        success_url = reverse_lazy('administration:list-accounts')


class DeleteAccountView(UserIsAdminMixin, DeleteView):
        model = Account
        template_name = 'administration/settings/account/delete_account.html'
        success_url = reverse_lazy('administration:list-accounts')


class DockerView(UserIsAdminMixin, TemplateView):
        template_name = 'administration/settings/docker.html'

        def get_context_data(self, **kwargs):
                context = super().get_context_data(**kwargs)
                dt = DockerTool()
                context['docker_containers'] = dt.list_containers()
                context['docker_images'] = dt.list_images()
                return context

class DockerLogsView(UserIsAdminMixin, TemplateView):
        template_name = 'administration/settings/docker/logs.html'

        def get_context_data(self, **kwargs):
                context = super().get_context_data(**kwargs)
                dt = DockerTool()
                container = dt.get_container(self.kwargs['id'])
                context['logs'] = container.logs()
                return context


class DockerActionsView(UserIsAdminMixin, View):
        form_class = DockerActionForm

        def post(self, request, *args, **kwargs):
                form = self.form_class(data=request.POST)
                if form.is_valid():
                        container_id = form.cleaned_data['container_id']
                        action = form.cleaned_data['action']
                        dt = DockerTool()
                        container = dt.get_container(container_id)

                        if action == "restart":
                                container.restart()
                        elif action == "stop":
                                container.stop()
                        elif action == "pause":
                                if container.status == "paused":
                                        container.unpause()
                                else:
                                        container.pause()
                        elif action == "start":
                                container.start()
                        elif action == "remove":
                                container.remove()
                        else:
                                return HttpResponse(status=400)

                        return HttpResponse(status=204)
                else:
                        return HttpResponse(status=400)

class DockerImageActionsView(UserIsAdminMixin, View):
        form_class = DockerImageActionForm

        def post(self, request, *args, **kwargs):
                form = self.form_class(data=request.POST)
                if form.is_valid():
                        image_id = form.cleaned_data['image_id']
                        action = form.cleaned_data['action']
                        dt = DockerTool()

                        if action == "create":
                                dt.create_container(image_id)
                        elif action == "remove":
                                image.remove()
                        else:
                                return HttpResponse(status=400)

                        return HttpResponse(status=204)
                else:
                        return HttpResponse(status=400)