from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import UserSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from django.shortcuts import redirect
from django.views import View
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from django.contrib.auth.decorators import login_required  # 로그인 필요 데코레이터 추가
from django.contrib.auth.forms import PasswordChangeForm  # 비밀번호 변경 폼 추가
from django.contrib.auth import update_session_auth_hash  # 비밀번호가 변경된 후, 사용자의 세션을 업데이트하여 로그인 상태를 유지

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

def login_redirect(request):
    return redirect('chatbot_page')

def register_page(request):
    return render(request, 'register.html')

def index(request):
    # 기본 경로에서 JSON 응답 반환
    return JsonResponse({'message': 'Hello, this is accounts app!'})

def chatbot_page(request):
    # /chatbot/ 경로에서 chatbot.html 템플릿 렌더링
    return render(request, 'chatbot.html')

@csrf_exempt
def chatbot_api(request):
    if request.method == "POST":
        data = json.loads(request.body)
        user_message = data.get("message", "")

        # 간단한 봇 응답 로직
        bot_response = f"You said: {user_message}"
        return JsonResponse({"response": bot_response})
    return JsonResponse({"error": "Invalid request method"}, status=400)

def friends_selection(request):
    # 등장인물 선택 화면 렌더링
    return render(request, 'friends_selection.html')

def chatbot_page(request):
    # URL 쿼리 파라미터에서 캐릭터 이름 가져오기
    character = request.GET.get('character', 'Default')
    return render(request, 'chatbot.html', {'character': character})

def chatbot_api(request):
    if request.method == "POST":
        data = json.loads(request.body)
        user_message = data.get("message", "")
        character = data.get("character", "Default")

        # 캐릭터별 페르소나 설정
        personas = {
            "Rachel": "You are Rachel Green, a fashion enthusiast.",
            "Ross": "You are Ross Geller, a paleontologist.",
            "Monica": "You are Monica Geller, a chef.",
            "Chandler": "You are Chandler Bing, a sarcastic guy.",
            "Joey": "You are Joey Tribbiani, an actor who loves food.",
            "Phoebe": "You are Phoebe Buffay, a quirky musician.",
        }

        persona = personas.get(character, "You are a generic chatbot.")
        bot_response = f"{persona} You said: {user_message}"
        return JsonResponse({"response": bot_response})

    return JsonResponse({"error": "Invalid request"}, status=400)

# 프로필 뷰 추가
@login_required  # 로그인된 사용자만 접근 가능
def profile(request):
    # 비밀번호 변경 폼 처리
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # 세션 유지
            return redirect('profile')  # 프로필 페이지로 리다이렉트
    else:
        form = PasswordChangeForm(request.user)

    return render(request, 'profile.html', {
        'form': form,
        'username': request.user.username,
        'email': request.user.email,
    })

@login_required  # 로그인된 사용자만 접근 가능
def delete_account(request):
    # 계정 삭제 처리
    if request.method == 'POST':
        user = request.user
        user.delete()  # 회원 삭제
        return redirect('login')  # 로그인 화면으로 리다이렉트

    return render(request, 'delete_account.html')  # 삭제 확인 페이지 렌더링