from rest_framework import generics, permissions
from .serializers import TodoSerializer, TodoUpdateSerializer
from django.contrib.auth.models import User
from django.db import IntegrityError
from todowo.models import Todo
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from django.http import JsonResponse
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate


@csrf_exempt
def signup(request):
    if request.method=='POST':
        try:
            data=JSONParser().parse(request)
            user = User.objects.create_user(username=data['username'],email=data['email'],password=data['password'])
            user.save()
            token=Token.objects.create(user=user)
            return JsonResponse({'token':str(token)},status=201)
        except IntegrityError:
            return JsonResponse({'error':'Username is already taken. Please try something else.'},status=400)

@csrf_exempt
def login(request):
    if request.method=='POST':
        data=JSONParser().parse(request)
        user = authenticate(request,username=data['username'],password=data['password'])
        if user is not None:
            try:
                token=Token.objects.get(user=user)
            except:
                token=Token.objects.create(user=user)
            return JsonResponse({'token':str(token)},status=200)
        else:
            return JsonResponse({'error':'Username or Password is invalid.'},status=400)
            
    
        





class TodoCompletedList(generics.ListAPIView):
    serializer_class=TodoSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Todo.objects.filter(user=user, datecompleted__isnull=False).order_by('-datecompleted')


class TodoListCreate(generics.ListCreateAPIView):
    serializer_class=TodoSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Todo.objects.filter(user=user, datecompleted__isnull=True)
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class TodoRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    serializer_class=TodoSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Todo.objects.filter(user=user)
    

class TodoComplete(generics.UpdateAPIView):
    serializer_class=TodoUpdateSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Todo.objects.filter(user=user)
    
    def perform_update(self, serializer):
        serializer.instance.datecompleted = timezone.now()
        serializer.save()
    


