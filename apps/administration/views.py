
from django.conf import settings
from django.contrib.auth.mixins import UserPassesTestMixin
from django.http import HttpResponse
from django.urls import reverse_lazy
from django.views.generic import (CreateView, DeleteView, DetailView, FormView,
                                  ListView, TemplateView, UpdateView, View)

from apps.accounts.models import Account
from apps.administration.docker_utils import DockerTool
from apps.administration.forms import (ConfigUpdateForm, DockerActionForm,
                                       DockerImageActionForm)
from apps.challenges.models import (Attachment, BadSubmission, Category,
                                    Challenge, FirstBlood, Flag, Hint, Solves)
from apps.scoreboard.models import News
from apps.scoreboard.utils import get_key, set_key, get_themes, set_theme, get_theme


class UserIsAdminMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_staff


class IndexView(UserIsAdminMixin, TemplateView):
    template_name = 'templates/informations.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['challenges'] = Challenge.objects.prefetch_related('category')
        context['categories'] = Category.objects.all()

        chall_stats = []
        total_challs = context['challenges'].count()
        solved_challs = Solves.objects.values(
            'challenge__pk').distinct().count()
        unsolved_challs = int(total_challs) - int(solved_challs)

        accounts = Account.objects.prefetch_related('solves_set')
        account_stats = []
        total_accounts = accounts.count()
        accounts_with_points = [
            x for x in accounts if x.solves_set.count() > 0]
        accounts_with_zero = total_accounts - len(accounts_with_points)
        account_stats.append(len(accounts_with_points))
        account_stats.append(accounts_with_zero)

        first_bloods = FirstBlood.objects.all().values_list(
            'account__username', flat=True).distinct()
        first_blood_accounts = [
            x for x in first_bloods.prefetch_related('account')]
        first_blood_data = []
        for account in first_blood_accounts:
            solved = FirstBlood.objects.filter(
                account__username=account).count()
            first_blood_data.append(solved)

        chall_stats.append(solved_challs)
        chall_stats.append(unsolved_challs)
        context['first_bloods_labels'] = first_blood_accounts
        context['first_bloods_data'] = first_blood_data
        context['chall_stats'] = chall_stats
        context['account_stats'] = account_stats
        context['accounts'] = accounts
        context['uptime'] = settings.GET_UPTIME()
        context['bad_submissions'] = BadSubmission.objects.prefetch_related(
            'account').prefetch_related('challenge').all()
        context['challenges'] = Challenge.objects.all()
        return context


class CTFView(UserIsAdminMixin, TemplateView):
    template_name = 'templates/ctf.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['challenges'] = Challenge.objects.prefetch_related('category')
        context['categories'] = Category.objects.all()
        return context


class AccountsView(UserIsAdminMixin, ListView):
    model = Account
    context_object_name = 'accounts'
    template_name = 'templates/accounts.html'


class UpdateAccountView(UserIsAdminMixin, UpdateView):
    model = Account
    fields = ['username', 'email', 'password',
              'is_staff', 'is_superuser', 'is_active', 'banned']
    template_name = 'templates/account/update_account.html'
    success_url = reverse_lazy('administration:list-accounts')


class ToggleAccountStateView(UserIsAdminMixin, UpdateView):
    model = Account
    fields = ['is_active']
    success_url = reverse_lazy('administration:list-accounts')


class DeleteAccountView(UserIsAdminMixin, DeleteView):
    model = Account
    template_name = 'templates/account/delete_account.html'
    success_url = reverse_lazy('administration:list-accounts')


class DockerView(UserIsAdminMixin, TemplateView):
    template_name = 'templates/docker.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        dt = DockerTool()
        context['docker_containers'] = dt.list_containers()
        context['docker_images'] = dt.list_images()
        return context


class DockerLogsView(UserIsAdminMixin, TemplateView):
    template_name = 'templates/docker/logs.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        dt = DockerTool()
        container = dt.get_container(self.kwargs['id'])
        context['logs'] = container.logs().decode('utf-8')
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


class GeneralView(UserIsAdminMixin, TemplateView):
    template_name = 'templates/general.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        CURRENT_THEME = get_theme()
        context['form'] = ConfigUpdateForm(initial={'theme': CURRENT_THEME})
        context['themes'] = get_themes()
        context['title'] = get_key("ctf_name")
        context['start_time'] = get_key('start_time')
        context['end_time'] = get_key('end_time')
        return context


class GeneralUpdateView(UserIsAdminMixin, View):
    form_class = ConfigUpdateForm

    def post(self, request, *args, **kwargs):
        form = self.form_class(data=request.POST)
        if form.is_valid():
            if 'theme' in request.POST:
                set_theme(request.POST['theme'])

            if 'start_time' in request.POST:
                if request.POST['start_time']:
                    set_key("start_time", request.POST['start_time'])
                else:
                    set_key("start_time", None)

            if 'end_time' in request.POST:
                if request.POST['end_time']:
                    set_key("end_time", request.POST['end_time'])
                else:
                    set_key("end_time", None)

            set_key("ctf_name", request.POST['title'])

            return HttpResponse(status=204)
        else:
            return HttpResponse(status=400)


class NewListView(UserIsAdminMixin, ListView):
    model = News
    ordering = '-created_at'
    template_name = 'templates/news.html'


class NewsCreateView(UserIsAdminMixin, CreateView):
    model = News
    fields = ['text']
    template_name = 'templates/news/create_news.html'
    success_url = reverse_lazy('administration:news')


class NewsUpdateView(UserIsAdminMixin, UpdateView):
    model = News
    fields = ['text']
    template_name = 'templates/news/update_news.html'
    success_url = reverse_lazy('administration:news')


class NewsDeleteView(UserIsAdminMixin, DeleteView):
    model = News
    success_url = reverse_lazy('administration:news')
