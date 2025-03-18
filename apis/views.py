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
import smtplib
import random
from .utils import read_properties
from email.mime.text import MIMEText

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
            return Response({f"message":"Error in saving the data. Try again"},status= status.HTTP_500_INTERNAL_SERVER_ERROR)
    except Exception as e:
        return Response({f"message":"Internal Server Error"},status=status.HTTP_500_INTERNAL_SERVER_ERROR)


def user_registration_email_verification(request):
    smtp_email_address = read_properties().get('smtp_email_address').data
    smtp_email_password = read_properties().get('smtp_email_password').data
    print(smtp_email_address)
    print(smtp_email_password)
    smtp_connection = smtplib.SMTP('smtp.gmail.com', 587)
    smtp_connection.starttls()
    otp = random.randint(0, 10000)
    subject = "OTP Verification"
    body = """
            <html>
            <body>
            <p>Your OTP : <b>"""+str(otp)+"""</b></p>
            </body>
            </html>
        """
    html_message = MIMEText(body, 'html')
    html_message['Subject'] = subject
    html_message['From'] = smtp_email_address
    html_message['To'] = request.data.get('email')
    smtp_connection.login(smtp_email_address,smtp_email_password)
    res = smtp_connection.sendmail(smtp_email_address, request.data.get('email'), html_message.as_string())
    print(res)
    smtp_connection.quit()
    response = database.insert_otp(request.data.get('email'),otp)
    return Response(json.dumps(str(response)),status=status.HTTP_201_CREATED)


@api_view(['POST'])
def verify_email_otp(request):
    is_verified = database.verify_otp(request.data)
    try:
        if(is_verified):
            database.delete_otp(request.data)
        return Response({"isVerified":is_verified}, status=status.HTTP_200_OK )
    except:
        return Response({"Internal Server Error"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
def user_login(request):
    user = database.get_user_by_email(request.data)
    print(user)
    try:
        if(user != None):
            if(check_password(request.data.get('password'),user.get('password'))):
                return Response({"isUserExists":True, "isPasswordTrue":True}, status=status.HTTP_200_OK )
            return Response({"isUserExists":True, "isPasswordTrue":True}, status=status.HTTP_200_OK)
        else:
            return Response({"isUserExists":False}, status=status.HTTP_200_OK)
    except:
        return Response({"Internal Server Error"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
def test_fun(request):
    encrypted_password = make_password(request.data.get('password'))
    request.data['password'] = encrypted_password
    test = database.insert_test(request.data)
    return Response("success", status=status.HTTP_200_OK )