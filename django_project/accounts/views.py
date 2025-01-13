from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import UserSerializer, AudioUploadSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from django.shortcuts import redirect, render
from django.core.files.storage import default_storage
from django.views import View
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
import json
from .STT import AudioRecorder
from openai import OpenAI
from dotenv import load_dotenv
import pyaudio
import wave
import os
import base64
import uuid
from datetime import datetime



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



@csrf_exempt
def save_audio(request):
    if request.method == 'POST' and request.FILES.get('audio_file'):
        audio_file = request.FILES['audio_file']

        # Generate a unique file name
        unique_id = uuid.uuid4().hex  # Unique ID for the file
        timestamp = datetime.now().strftime('%Y%m%d%H%M%S')  # Current timestamp
        file_extension = os.path.splitext(audio_file.name)[-1]  # Extract file extension
        unique_filename = f"audio_{timestamp}_{unique_id}{file_extension}"

        save_path = os.path.join(settings.BASE_DIR, 'static/audios', unique_filename)

        # Ensure the directory exists
        os.makedirs(os.path.dirname(save_path), exist_ok=True)

        # Save the file
        with open(save_path, 'wb') as f:
            for chunk in audio_file.chunks():
                f.write(chunk)

        return JsonResponse({'success': True, 'message': 'Audio saved successfully.', 'filename': unique_filename})
    return JsonResponse({'success': False, 'message': 'Invalid request.'})
