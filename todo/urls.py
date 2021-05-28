from django.urls import path
from .views import CreateGroupView, CreateTaskView, DeleteGroupView, DeleteTaskView, GroupList, IndividualOwnerGroups, OwnerListView, TaskList, TasksFromGroups, UpdateTaskView
from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = [
    path('owners/', OwnerListView.as_view(), name="owners"),
    path('groups/', GroupList.as_view(), name="groups"),
    path('tasks/', TaskList.as_view(), name='tasks/'),

    path('owner_groups/', IndividualOwnerGroups.as_view(), name='owner_groups'),
    path('group_tasks/', TasksFromGroups.as_view(), name='group_tasks'),

    path('create_group/', CreateGroupView.as_view(), name='create_group'),
    path('create_task/', CreateTaskView.as_view(), name='task_view'),

    path('delete_task/<int:pk>', DeleteTaskView.as_view(), name='delete_task'),
    path('delete_group/<int:pk>', DeleteGroupView.as_view(), name='delete_group'),
    
    path('update_task/<int:pk>', UpdateTaskView.as_view(), name='update_task')
]

urlpatterns = format_suffix_patterns(urlpatterns)