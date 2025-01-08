from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import UserSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from django.shortcuts import redirect
from django.views import View




# Create your views here.

def index(request):
    return JsonResponse({'message': 'Hello, this is accounts app!'})


class RegisterView(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'User created successfully!'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(TokenObtainPairView):
    pass


class InitialSetupPage(View):
    def get(self, request):
        return HttpResponse("Initial setup page loaded.")
    

def login_page(request):
    return render(request, 'login.html')

def chatbot_page(request):
    return render(request, 'chatbot.html')

def login_redirect(request):
    return redirect('chatbot_page')