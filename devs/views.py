import time
import json

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views import generic, View
from django.views.generic.detail import SingleObjectMixin
from django.urls import reverse
from django.shortcuts import get_object_or_404, resolve_url
from django.core.cache import cache
from django.forms import formset_factory

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

from django.core.mail import send_mail, EmailMultiAlternatives
from django.conf import settings
from celery import shared_task

@shared_task
def send_welcome_email(user_email, image):
    subject = "Welcome!"
    text_content = "Welcome to our site."
    html_content = f"{image} uploaded!"

    msg = EmailMultiAlternatives(
        subject, text_content, settings.DEFAULT_FROM_EMAIL, [user_email]
    )
    msg.attach_alternative(html_content, "text/html")
    msg.send()

from operator import itemgetter

from .models import Developer, Team, Tech
from .forms.tech_form import TechForm
from .forms.team_form import TeamForm
from .forms.developer_form import DeveloperForm
from .forms.user_form import UserForm
# from django.template.loaders.cached.Loader

# Developers
class DeveloperIndexView(generic.ListView):
    # login_url = '/devs/login'
    model = Developer
    template_name = 'devs/developers/index.html'
    context_object_name = 'developers'

class DeveloperCreateView(SingleObjectMixin, View):
    # login_url = '/devs/login'
    def post(self, req, *args, **kwargs):
        form = DeveloperForm(req.POST, req.FILES)
        if form.is_valid():
            if 'pk' in kwargs:
                print('pk exists')
                developer = get_object_or_404(Developer, pk=kwargs['pk'])
                form = DeveloperForm(data=req.POST, files=req.FILES, instance=developer)

            form.save()
            # send_welcome_email.delay('adonis7184@gmail.com')

        else:
            template_name = 'devs/developers/create.html'
            return render(req, template_name, {'form': form})

        return HttpResponseRedirect(reverse('devs:developer_list'))
        
    def get(self, req, *args, **kwargs):
        if 'pk' in kwargs:
            developer = get_object_or_404(Developer, pk=kwargs['pk'])
            form = DeveloperForm(instance=developer)
        else:
            form = DeveloperForm()

        template_name = 'devs/developers/create.html'

        return render(req, template_name, {'form': form})

class DeveloperDetailView(generic.DeleteView):
    # login_url = '/devs/login'
    model = Developer
    template_name = 'devs/developers/detail.html'
    context_object_name = 'developer'

# Teams
class TeamIndexView(generic.ListView):
    # login_url = '/devs/login'
    model = Team
    template_name = 'devs/teams/index.html'
    context_object_name = 'teams'    

# @login_required(login_url='/devs/login')
def create_team(request):
    if request.method == 'POST':
        form = TeamForm(request.POST)

        if form.is_valid():
            name, teches = itemgetter('name', 'teches')(form.cleaned_data)

            team = Team.objects.create(name=name)
            team.teches.set(teches)
            send_welcome_email.delay('adonis7184@gmail.com', '1234')

            # send_mail(subject, message, sender, recipients)

            return HttpResponseRedirect(reverse('devs:team_list'))
    else:
        form = TeamForm()

    template_name = 'devs/teams/create.html'

    return render(request, template_name, {'form': form})

# @login_required(login_url='/devs/login')
def edit_team(request, pk):
    before_time = time.time()

    team = cache.get(f'team{pk}')
    if not team:
        team = Team.objects.get(id=pk)
        cache.set(f'team{pk}', team, 300)  # cache for 5 minutes

    print(time.time() - before_time)

    if request.method == 'POST':
        if 'delete' in request.POST:
            team.delete()
        else:
            form = TeamForm(request.POST)

            if form.is_valid():
                name, teches = itemgetter('name', 'teches')(form.cleaned_data)
                
                team.name = name
                team.teches.set(teches)
                team.save()

        return HttpResponseRedirect(reverse('devs:team_list'))
    else:
        form = TeamForm(initial={
            'name': team.name,
            'teches': team.teches.all(),  # pre-select the related Tech objects
        })

    template_name = 'devs/teams/detail.html'

    return render(request, template_name, {'form': form})

class TeamDetailView(generic.DetailView):
    # login_url = '/devs/login'
    model = Team
    template_name = 'devs/teams/detail.html'
    context_object_name = 'team'    

# Teches
class TechIndexView(generic.ListView):
    # login_url = '/devs/login'
    model = Tech
    template_name = 'devs/teches/index.html'
    context_object_name = 'teches'

# @login_required(login_url='/devs/login')
def create_tech(request):
    TechFormSet = formset_factory(TechForm, extra=2)
    if request.method == 'POST':
        formsets = TechFormSet(request.POST)

        if formsets.is_valid():
            for form in formsets:
                name, description = itemgetter('name', 'description')(form.cleaned_data)
                tech = Tech(name = name, description = description)
                tech.save()

            # send_mail(subject, message, sender, recipients)

            return HttpResponseRedirect(reverse('devs:tech_list'))
    else:
        formsets = TechFormSet()

    template_name = 'devs/teches/create.html'

    return render(request, template_name, {'form': formsets})

# @login_required(login_url='/devs/login')
def edit_tech(request, pk):
    tech = get_object_or_404(Tech, pk=pk)

    if request.method == 'POST':
        if 'delete' in request.POST:
            tech.delete()
        else:
            form = TechForm(request.POST)
            
            if form.is_valid():
                name, description = itemgetter('name', 'description')(form.cleaned_data)
                tech.name = name
                tech.description = description
                tech.save()
        
        return HttpResponseRedirect(reverse('devs:tech_list'))
    else:
        form = TechForm({'name': tech.name, 'description': tech.description})
    
    template_name = 'devs/teches/detail.html'

    return render(request, template_name, {'form': form})

# Testing
def autoescape(request):
    template_name = 'devs/test/autoescape.html'
    context = {'context': '<b>context</b>'}  # dictionary, not Context()

    return render(request, template_name, context)

class MyLogin(LoginView):
    template_name = 'devs/auth/login.html' 

    def get_success_url(self):
        # Check if a `next` parameter exists
        redirect_to = self.request.GET.get('next')
        if redirect_to:
            return redirect_to
        # Otherwise, return your default URL
        return resolve_url(reverse('devs:developer_list')) 

class MyRegister(SingleObjectMixin, View):
    def get(self, req, *args, **kwargs):
        
        form = UserCreationForm()

        template_name = 'devs/auth/register.html'

        return render(req, template_name, {'form': form})

    def post(self, req, *args, **kwargs):
        form = UserCreationForm(req.POST)

        if form.is_valid():
            form.save()

            return HttpResponseRedirect(reverse('devs:developer_list'))
        
        template_name = 'devs/auth/register.html'
        
        return render(req, template_name, {'form': form})
    
class MyLogout(LogoutView):
    def get_redirect_url(self):
        return reverse('devs:login')
    
@csrf_exempt
def s3_upload_notify(request):
    if request.method == "POST":
        data = json.loads(request.body)
        # Example: process info about uploaded file
        filename = data.get("filename")
        bucket = data.get("bucket")
        print(f"Received notification: {bucket}/{filename}")
        send_welcome_email('adonis7184@gmail.com', f"{bucket}/{filename}")
        return JsonResponse({"status": "received"})
    return JsonResponse({"error": "POST request required"}, status=400)