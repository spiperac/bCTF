from django.views.generic import CreateView, DetailView, ListView, UpdateView, DeleteView
from apps.teams.models import Team
from apps.accounts.models import Account


class ListTeamView(ListView):
    model = Account
    context_object_name = 'teams'
    paginate_by = 100
    template_name = 'templates/team/list.html'

    def get_queryset(self):
        filter_val = self.request.GET.get('filter', '')
        if filter_val is '':
            return Account.objects.all()
        new_context = Account.objects.filter(
            username__contains=filter_val,
        )
        return new_context

    def get_context_data(self, **kwargs):
        context = super(ListTeamView, self).get_context_data(**kwargs)
        context['filter'] = self.request.GET.get('filter', 'give-default-value')
        return context


class CreateTeamView(CreateView):
    model = Team
    template_name = 'team/create.html'


class UpdateTeamView(UpdateView):
    model = Team
    template_name = 'team/update.html'


class DetailTeamView(DetailView):
    model = Team
    template_name = 'team/detail.html'


class DeleteTeamView(DeleteView):
    model = Team
    template_name = 'team/list.html'
