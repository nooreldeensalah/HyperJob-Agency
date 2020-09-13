from django.views import View
from django.shortcuts import render
from .models import Resume


class ResumeView(View):
    def get(self, request, *args, **kwargs):
        return render(request, "resumes.html", context={"Resume": Resume.objects.all()})
