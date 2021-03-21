from django.shortcuts import render
from rest_framework.views import  APIView 
from rest_framework.response import Response
from .serializers import UserSerializer
from .models import User
from rest_framework.exceptions import AuthenticationFailed

# Create your views here.


class register(APIView):
   def post(self,request):
       serializer = UserSerializer(data=request.data)
       serializer.is_valid(raise_exception=True)
       serializer.save()
       return Response(serializer.data)


class login(APIView):
    def post(self , request):
        email = request.data['email']
        password= request.data['password']

        user =User.objects.filter(email=email).first()

        if user is None:
            raise AuthenticationFailed('User not found')
       
        if not user.check_password(password) :
            raise AuthenticationFailed('Incorrect password')

        return Response({
            'message':'authentification sucsses'
        })           