
from django.urls import path
from . views import CustomUserLogin, TaskDelete, TaskDetail, TaskList,TaskCreate, TaskUpdate, RegisterUser,TaskReorder
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('login/',CustomUserLogin.as_view(),name='UserLogin'),
    path('logout/',LogoutView.as_view(next_page='UserLogin'),name='UserLogout'),
    path('register/',RegisterUser.as_view() ,name='UserRegister'),
    
    path('task/',TaskList.as_view(),name='TaskList'),
    path('task/<int:pk>/',TaskDetail.as_view(),name='TaskDetail'),
    path('task_update/<int:pk>/',TaskUpdate.as_view(),name='TaskUpdate'),
    path('task_delete/<int:pk>/',TaskDelete.as_view(),name='TaskDelete'),
    path('task_create/',TaskCreate.as_view(),name='TaskCreate'),
    path('task-reorder/', TaskReorder.as_view(), name='task-reorder'),
]   
