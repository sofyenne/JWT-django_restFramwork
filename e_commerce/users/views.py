from django.shortcuts import render
from rest_framework.views import  APIView 
from rest_framework.response import Response
from .serializers import UserSerializer
from .models import User
from rest_framework.exceptions import AuthenticationFailed
import jwt 
from datetime import datetime, timedelta

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
        
        payload = {
          'id' : user.id,
          'exp' : datetime.utcnow() + timedelta(minutes=60),
          'iat' :datetime.utcnow()
        }

        token = jwt.encode(payload , 'secret' , algorithm = 'HS256').decode('utf-8')

        response = Response()

        response.set_cookie(key = 'jwt' , value = token , httponly = True)

        response.data={
            'jwt' :token
        }


        return response         


class getuser(APIView):
    def get(self , request):
        token=request.COOKIES.get('jwt')
        if not token:
            raise AuthenticationFailed('Unitentificate')
        try:
            pyload = jwt.decode(token , 'secret', algorithm=['HS256'])
        except jwt.ExpiredSignature:
            raise AuthenticationFailed('Unitentificate')    

        user = User.objects.filter(id =pyload['id']).first()
        serializer = UserSerializer(user)

        return Response(serializer.data)        
class logout(APIView):
    def post(self , request):
        response = Response()
        response.delete_cookie('jwt')
        response.data = {

            'message' : 'success'
        }
        return response