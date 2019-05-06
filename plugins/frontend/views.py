from django.shortcuts import render
from django.views.generic import View


class FrontendView(View):
    def get(self, request, *args, **kwargs):
        return render(self.request, 'frontend/index.html')

