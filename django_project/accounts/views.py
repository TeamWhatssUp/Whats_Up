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
from .llm import generate_chat_response
from langchain_openai import OpenAIEmbeddings




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

# 캐릭터 정보 (예제)
characters = {
    "Rachel": "I'm Rachel Green, your fashion guru!",
    "Ross": "Hi, I'm Ross Geller. Let's talk about science and love!",
    "Monica": "I'm Monica Geller, the perfectionist chef. Need tips?",
    "Chandler": "Chandler Bing here! Ready for some sarcasm?",
    "Joey": "Joey Tribbiani! 'How you doin'?'",
    "Phoebe": "Phoebe Buffay, quirky musician at your service.",
}

@csrf_exempt
def chatbot_api(request):
    if request.method == "POST":
        data = json.loads(request.body)
        character_name = data.get("character", "Default")  # 요청에서 캐릭터 이름 가져오기
        user_query = data.get("message", "")  # 요청에서 사용자 메시지 가져오기

        try:
            # LLM의 generate_chat_response 호출 (캐릭터 이름과 메시지 전달)
            response = generate_chat_response(character_name, user_query)
            return JsonResponse({"response": response})  # JSON 응답 반환
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)  # 예외 처리
    return JsonResponse({"error": "Invalid request method"}, status=400)  # POST가 아닌 경우 처리
