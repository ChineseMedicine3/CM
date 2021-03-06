from django.shortcuts import render
from rest_framework import viewsets,permissions,status
from models import MyUser
from django.db.models.query import QuerySet
from rest_framework.views import APIView
from django.template.context_processors import request
from rest_framework_jwt.settings import api_settings
from rest_framework.response import Response
from django.contrib.auth.models import User
from rest_framework_jwt.views import jwt_response_payload_handler
from rest_framework.renderers import JSONRenderer
from rest_framework.decorators import api_view, permission_classes
from serializers import UserSerializer
import jwt
from rest_framework.status import HTTP_400_BAD_REQUEST, HTTP_200_OK
from django.contrib import auth



@api_view(http_method_names=['POST'])  
@permission_classes((permissions.AllowAny,))  
def adduser(request):  
    adminKey=request.POST.get('adminkey', '')
    username= request.POST.get('username', '')
    password=request.POST.get('password', '')
    repeat_password = request.POST.get('repeat_password', '')
    if adminKey!='iamadministrator':
        return HttpResponse(HTTP_400_BAD_REQUEST)
    else:
        if password == '' or repeat_password == '':
            return HttpResponse(HTTP_400_BAD_REQUEST)
        elif password != repeat_password:
            return HttpResponse(HTTP_400_BAD_REQUEST)
        user=MyUser.objects.filter(username=request.POST.get('username', ''))
        if user is not None:
            return HttpResponse(HTTP_400_BAD_REQUEST)
        else:
            new_user=MyUser(username=request.POST.get('username', '')
                                ,password=request.POST.get('password', ''),
                                permission=request.POST.get('permission', ''))
            new_user.save()
            return HttpResponse(HTTP_200_OK)
    
@api_view(http_method_names=['POST'])  
@permission_classes((permissions.AllowAny,))  
def login(request):  
    user=MyUser.objects.filter(username=request.POST.get('username', '')
                                ,password=request.POST.get('password', ''))
    if user is None:
        return HttpResponse(HTTP_400_BAD_REQUEST)
    else:
        user=MyUser.objects.get(username=request.POST.get('username', ''))
        if user.permission==1:
            return Response({"adminkey":'iamadministrator'})
        else:
            return HttpResponse(HTTP_200_OK)
    
    
@api_view(http_method_names=['PUT'])  
@permission_classes((permissions.AllowAny,))  
def changePassword(request): 
    userName=request.data.get('username','')
    newpassword=request.data.get('password','')
    re_newpassword=request.data.get('re_password','')
    user=MyUser.objects.filter(username=userName)
    if user is None:
        return HttpResponse(HTTP_400_BAD_REQUEST)
    if newpassword == '' or re_newpassword == '':
        return HttpResponse(HTTP_400_BAD_REQUEST)
    elif newpassword != re_newpassword:
        return HttpResponse(HTTP_400_BAD_REQUEST)
    else:
        user=MyUser.objects.get(username=userName)
        user.password=newpassword
        user.save()
        return HttpResponse(HTTP_200_OK)
    

        
  
        
        
      
    
    
    
    
    
    
    
    
    
    
