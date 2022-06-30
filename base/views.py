from operator import contains
from django.shortcuts import redirect
from base.models import Task
# Create your views here.
'''
introduction into class based views
''' 
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView,UpdateView,DeleteView,FormView
from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login



# Import for reordering Features
from django.views import View
from django.shortcuts import redirect
from django.db import transaction

from .models import Task
from .forms import PositionForm



class CustomUserLogin(LoginView):
    template_name='base/login.html'
    fields='__all__'
    redirect_authenticated_user=True

    def get_success_url(self) -> str: 
        return reverse_lazy('TaskList')

class RegisterUser(FormView):
    template_name='base/register.html'
    form_class=UserCreationForm
    redirect_authenticated_user=True
    
    def get_success_url(self):
        return reverse_lazy('TaskList')

    def form_valid(self, form):
        user=form.save()
        if user is not None:
            login(self.request, user)
        return super(RegisterUser, self).form_valid(form)

    def get(self,*args, **kwargs):
        if self.request.user.is_authenticated:
            redirect("TaskList")
        return super(RegisterUser,self).get(*args, **kwargs)



class TaskList(LoginRequiredMixin,ListView):
    model=Task
    context_object_name='tasks'

    def get_context_data(self, **kwargs):
        context=super().get_context_data(**kwargs)
        context['tasks']=context['tasks'].filter(user=self.request.user)
        context['count']=context['tasks'].filter(complete=False).count()
        search_input=self.request.GET.get('search-area') or ' '
        if search_input:
            context['tasks']=context['tasks'].filter(
                title__icontains=search_input)
        context['search']=search_input
        return context

class TaskDetail(LoginRequiredMixin,DetailView):
    model=Task
    context_object_name='tasks'


class TaskCreate(LoginRequiredMixin,CreateView):
    model=Task
    
    fields=['title','description','complete']
    success_url=reverse_lazy('TaskList')

    def form_valid(self, form) :
        form.instance.user=self.request.user
        return super().form_valid(form)

class TaskUpdate(LoginRequiredMixin,UpdateView):
    model=Task
    fields=['title','description','complete']
    success_url=reverse_lazy('TaskList')



class TaskDelete(LoginRequiredMixin,DeleteView):
    model=Task
    context_object_name='task'
    success_url=reverse_lazy('TaskList')

    def get_queryset(self):
        owner = self.request.user
        return self.model.objects.filter(user=owner)

class TaskReorder(View):
    def post(self, request):
        form = PositionForm(request.POST)

        if form.is_valid():
            positionList = form.cleaned_data["position"].split(',')

            with transaction.atomic():
                self.request.user.set_task_order(positionList)

        return redirect(reverse_lazy('tasks'))