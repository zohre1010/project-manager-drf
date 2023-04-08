from django.urls import path
from . import views


app_name = 'project'
urlpatterns = [
    path('create/',views.ProjectCreateView.as_view(),name='project_create'),
    path('list/',views.ProjectListView.as_view(),name='project_list'),
    path('list/<int:pk>/',views.ProjectListViewForOneUser.as_view(),name='project_list'),  
    path('delete/<int:pk>/',views.ProjectDeleteView.as_view(),name='project-delete'),  
    path('update/<int:pk>/',views.ProjectUpdateView.as_view(),name='project_update'),
    # ________________________________________________________________________________________________________________________
    path('task/list/<int:pk>/',views.TaskListViewForOneUser.as_view(),name='task_list'),
    path('task/create/',views.TaskCreateView.as_view(),name='task_create'),
    path('task/update/<int:pk>/',views.TaskUpdateView.as_view(),name='task_update'),
    path('task/change-status/<int:pk>/',views.TaskUpdateForUser.as_view(),name='status-task'),
    path('task/doing/<int:pk>/',views.DoingTaskView.as_view(),name='going-task'),
    path('task/late/<int:pk>/',views.LateTaskView.as_view(),name='late-task'),
    path('task/done/<int:pk>/',views.DoneTaskView.as_view(),name='done-task'),
    path('task/delete/<int:pk>/',views.TaskDeleteView.as_view(),name='task-delete'),
    path('task/percents/<int:pk>/',views.PercentTask.as_view(),name='percents-task'),
    path('task/<int:pk>/',views.TaskOfTheProject.as_view(),name='tasks'),
    # ________________________________________________________________________________________________________________________
    path('<int:pk>/search/',views.ProjectListSearchView.as_view(),name='search'),#do
    
    path('note/create/',views.NoteCreateView.as_view(),name='create-note'),#do
    path('note/list/<int:pk>/',views.NoteOfTheProjectView.as_view(),name='list-note'),#do


    
]
