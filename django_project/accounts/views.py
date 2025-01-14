from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.permissions import AllowAny
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.views.decorators.csrf import csrf_exempt
import json
from .llm import generate_chat_response

# Create your views here.

def index(request):
    return JsonResponse({'message': 'Hello, this is accounts app!'})

# 회원가입
class RegisterView(APIView):
    permission_classes = [AllowAny]  # 회원가입은 인증 없이 접근 가능

    def post(self, request):
        data = request.data
        password = data.get('password')
        password2 = data.get('password2')

        if password != password2:
            return Response({'error': 'Passwords do not match.'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = User.objects.create_user(
                username=data.get('username'),
                email=data.get('email'),
                password=password
            )
            return Response({'message': 'User created successfully!'}, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

# 로그인 (Simple JWT)
class LoginView(TokenObtainPairView):
    permission_classes = [AllowAny]  # 로그인은 인증 없이 접근 가능

# HTML 로그인 페이지
def login_page(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('friends_selection')
        return render(request, 'login.html', {"error": "Invalid credentials"})
    return render(request, 'login.html')

# 리디렉션 처리
def login_redirect(request):
    return redirect('/account/friends-selection/')

# 챗봇 페이지
def chatbot_page(request):
    character = request.GET.get('character', 'Default')
    return render(request, 'chatbot.html', {'character': character})

# 등장인물 선택 화면
def friends_selection(request):
    return render(request, 'friends_selection.html')

# 챗봇 API
@csrf_exempt
def chatbot_api(request):
    if request.method == "POST":
        data = json.loads(request.body)
        character_name = data.get("character", "Default")
        user_query = data.get("message", "")

        try:
            response = generate_chat_response(character_name, user_query)
            return JsonResponse({"response": response})
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)
    return JsonResponse({"error": "Invalid request method"}, status=400)

