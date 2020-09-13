from django.views import View
from django.shortcuts import render
from .models import Vacancy


class VacancyView(View):
    def get(self, request, *args, **kwargs):
        return render(request, "vacancies.html", context={'Vacancies': Vacancy.objects.all()})
