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
from . import database

# Create your views here.
@api_view(['POST'])
def user_registration(request):
    try:
        encrypted_password = make_password(request.data.get('password'))
        request.data['password'] = encrypted_password
        response = database.insert_user(request.data)
        print(response.inserted_id)
        if(response.inserted_id):
            return Response(json.dumps({"_id":str(response.inserted_id)}),status=status.HTTP_201_CREATED)
        else:
            return Response("Error in saving the data. Try again",status= status.HTTP_500_INTERNAL_SERVER_ERROR)
    except Exception as e:
        return Response("Internal Server Error",status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
def user_login(request):
    user = database.get_user_by_email(request.data)
    print(user)
    if(user != None):
        if(check_password(request.data.get('password'),user.get('password'))):
            return Response({"message":"Login SucssesFully"}, status=status.HTTP_200_OK )
        return Response({'message': 'Invalid Username and Password'}, status=status.HTTP_401_UNAUTHORIZED)
    else:
        return Response({f"message":"User doesn't exist"}, status=status.HTTP_200_OK )


@api_view(['POST'])
def test_fun(request):
    encrypted_password = make_password(request.data.get('password'))
    request.data['password'] = encrypted_password
    test = database.insert_test(request.data)
    return Response("success", status=status.HTTP_200_OK )

