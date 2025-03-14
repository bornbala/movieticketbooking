from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .serializer import UserSerializer
from .models import User
from django.contrib import auth
from rest_framework.authtoken.models import Token
import rest_framework.status as status
from . import crypto
from django.contrib.auth.hashers import make_password,check_password
import json





# Create your views here.
@api_view(['POST'])
def user_registration(request):
    encrypted_password = make_password(request.data.get('password'))
    request.data['password'] = encrypted_password
    serialzer = UserSerializer(data=request.data)
    try:
        if(serialzer.is_valid()):
            serialzer.save()
            return Response(serialzer.data,status=status.HTTP_201_CREATED)
        else:
            return Response("Error in saving the data. Try again",status= status.HTTP_500_INTERNAL_SERVER_ERROR)
    except Exception as e:
        return Response("Internal Server Error",status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
def user_login(request):
    user = User.objects.get(email=request.data.get("email"))
    if(check_password(request.data.get('password'),user.password)):
        return Response({"Sucsses":"Login SucssesFully"}, status=status.HTTP_200_OK )
    return Response({'Failure': 'Invalid Username and Password'}, status=status.HTTP_401_UNAUTHORIZED)


@api_view(['POST'])
def test_fun(request):
    request.data['test'] = "test123"
    return Response(request.data)
        
    

