from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Group, Task

#Serializer for groups
class GroupSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    tasks = serializers.PrimaryKeyRelatedField(many=True, queryset=Task.objects.all())

    class Meta:
        model = Group
        fields = ['id', 'created', 'name', 'owner', 'tasks']

#Serializer for list of users with group ids also in list
class OwnerSerializer(serializers.ModelSerializer):
    grps = serializers.PrimaryKeyRelatedField(many=True, queryset=Group.objects.all())
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'grps']

class TaskSerializer(serializers.ModelSerializer):
    belongs_to = serializers.ReadOnlyField(source='belongs_to.name')
    class Meta:
        model = Task
        fields = ['id', 'created', 'data', 'completed', 'belongs_to']

#serializer for the form for getting tasks from groups
class IndividualGroupSerializer(serializers.Serializer):
    id = serializers.IntegerField()

#serializer to create new group
class CreateGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ['name']

#serializer to create new task
class CreateTaskSerializer(serializers.ModelSerializer):    
    class Meta:
        model = Task
        fields = ['data']

#serializer to update tasks
class UpdateTaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ['data','completed']