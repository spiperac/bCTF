from django.views.generic import CreateView, DetailView, ListView, UpdateView, DeleteView
from apps.teams.models import Team


class CreateTeamView(CreateView):
    model = Team
    template_name = 'team/create.html'


class UpdateTeamView(UpdateView):
    model = Team
    template_name = 'team/update.html'


class DetailTeamView(DetailView):
    model = Team
    template_name = 'team/detail.html'


class ListTeamView(ListView):
    model = Team
    template_name = 'team/list.html'


class DeleteTeamView(DeleteView):
    model = Team
    template_name = 'team/list.html'
