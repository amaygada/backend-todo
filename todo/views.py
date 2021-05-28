from os import stat
from re import S
from django.shortcuts import render

#view imports
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

#permission imports
from rest_framework.permissions import IsAuthenticated

#other imports
from django.contrib.auth.models import User

#imports from project
from .models import Group, Task
from .serializers import CreateGroupSerializer, CreateTaskSerializer, IndividualGroupSerializer, OwnerSerializer, GroupSerializer, TaskSerializer, UpdateTaskSerializer


'''
FOR ALL PROTECTED VIEW USE THIS IN THE HEADER:-

headers: { 
    '': '', 
    'Authorization': 'Bearer <access token here>', 
    'Content-Type': 'application/json'
  }

'''


# classes for full access to all user stuff
class OwnerListView(APIView):
    '''
    GET
    returns list of users:-
    [
        {
            "id": 1,
            "username": "amay",
            "email": "amaygada@gmail.com",
            "grps": [
                2,
                3,
                4
            ]
        }
    ]
    '''
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        user_list = User.objects.all()
        serializer = OwnerSerializer(user_list, many=True)
        return Response({"data" : serializer.data}, status.HTTP_200_OK)


class GroupList(APIView):
    '''
    GET
    returns list of groups:-
    [
        {
            "id": 2,
            "created": "2021-05-25T07:31:02.901866Z",
            "name": "abc",
            "owner": "amay",
            "tasks": [
                1
            ]
        },
        {
            "id": 3,
            "created": "2021-05-25T07:33:14.803976Z",
            "name": "lala",
            "owner": "amay",
            "tasks": []
        }
    ]
    '''

    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        group_list = Group.objects.all()
        serializer = GroupSerializer(group_list, many=True)
        return Response({"data" : serializer.data}, status=status.HTTP_200_OK)


class TaskList(APIView):
    '''
    GET
    returns list of tasks:-
    [
        {
            "id": 1,
            "created": "2021-05-25T07:42:47.692406Z",
            "data": "updated task data",
            "completed": true,
            "belongs_to": "abc"
        }
    ]
    '''

    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        tasklist = Task.objects.all()
        serializer = TaskSerializer(tasklist, many=True)
        return Response({"data" : serializer.data}, status=status.HTTP_200_OK)



#Views for individual goups and tasks access wrt user logged in

class IndividualOwnerGroups(APIView):
    '''
    GET
    returns list of group objects created by the logged in user:-
    {
        "groups": [
            {
                "id": 2,
                "created": "2021-05-25T07:31:02.901866Z",
                "name": "abc",
                "owner_id": 1
            },
            {
                "id": 3,
                "created": "2021-05-25T07:33:14.803976Z",
                "name": "lala",
                "owner_id": 1
            },
            {
                "id": 4,
                "created": "2021-05-25T16:20:52.575575Z",
                "name": "new",
                "owner_id": 1
            }
        ]
    }
    '''
    permission_classes = [IsAuthenticated]
    
    #get groups
    def get(self, request, format=None):
        user = request.user
        print(Group.objects.filter(owner=user))
        serializer = OwnerSerializer(user)
        group_pk_list = serializer.data['grps']
        group_list = Group.objects.filter(pk__in=group_pk_list)
        group_list = list(group_list.values())
        return Response({"data" : {"groups":group_list}}, status=status.HTTP_200_OK)
    

class TasksFromGroups(APIView):
    '''
    POST
    returns list of tasks corresponding to a group upon sending the group id:-
    
    #send this via post
    Body: {"id" : <integer id>}      

    #receive this as response:
    {
        "tasks": [
            {
                "id": 1,
                "created": "2021-05-25T07:42:47.692406Z",
                "data": "updated task data",
                "completed": true,
                "belongs_to_id": 2
            }
        ]
    }
    '''
    #veiw to send tasks corresponding to respective groups
    permission_classes = [IsAuthenticated]

    def post(self, request, format=None):
        serializer = IndividualGroupSerializer(data=request.data)
        if serializer.is_valid():
            id = serializer.data["id"]
            try:
                group = Group.objects.get(id=id)
                task = Task.objects.filter(belongs_to = group)
                tasklist = list(task.values())
                return Response({"data":{"tasks":tasklist}}, status=status.HTTP_200_OK)
            except:
                return Response({"data" : {"msg": "ID doesn't exist"}}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class CreateGroupView(APIView):
    '''
    POST
    creates group for logged in user by taking post request

    #send this via post
    {"name": <str group name>}

    #recieve this as response
    null
    '''
    permission_classes = [IsAuthenticated]

    def post(self, request, format=None):
        serializer = CreateGroupSerializer(data=request.data)
        if serializer.is_valid():
            group = serializer.save(owner=self.request.user)
            s = GroupSerializer(group)
            print(s.data)
            return Response({"data" : s.data} , status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CreateTaskView(APIView):
    '''
    POST
    create new tasks corresponding to a group

    #send this via post
    { "group_id" : <int grp id> , "task" : {"data": <str task data>} }

    #receive this as response 
    null
    '''
    permission_classes = [IsAuthenticated]

    def post(self, request, format=None):
        group_id = request.data["group_id"]
        group = Group.objects.get(id=group_id)
        serializer = CreateTaskSerializer(data=request.data["task"])
        if serializer.is_valid():
            task = serializer.save(belongs_to = group)
            s = TaskSerializer(task)
            return Response({"data" : s.data},status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class DeleteTaskView(APIView):
    '''
    DELETE
    deletes individual tasks by passing into the url, the task id
    '''
    permission_classes = [IsAuthenticated]

    def delete(self, request, pk, format=None):
        task = Task.objects.get(pk=pk)
        task.delete()
        return Response(status = status.HTTP_200_OK)


class DeleteGroupView(APIView):
    '''
    DELETE
    deletes individual tasks by passing into the url, the group id
    '''
    permission_classes = [IsAuthenticated]

    def delete(self, request, pk, format=None):
        group = Group.objects.get(pk=pk)
        group.delete()
        return Response(status = status.HTTP_200_OK)


class UpdateTaskView(APIView):
    '''
    PUT
    used to update tasks mostly for the completed status
    can be also used to update the task data 

    #send this via put
    {
        "data" : <str updated data>,
        "completed" : <boolean updated completed>
    }
    #receive this as response
    null
    '''
    permission_classes = [IsAuthenticated]
    
    def put(self, request, pk, format=None):
        task = Task.objects.get(pk=pk)
        serializer = UpdateTaskSerializer(task, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(status=status.HTTP_200_OK)
        return Response(status = status.HTTP_400_BAD_REQUEST)