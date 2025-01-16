from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import UserSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from django.shortcuts import redirect
from django.core.files.storage import default_storage
from django.conf import settings
from django.views import View
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from .llm import generate_chat_response
from langchain_openai import OpenAIEmbeddings
from openai import OpenAI
from openai import OpenAIError
from dotenv import load_dotenv
import pyaudio
import wave
import os
import base64
import uuid
from datetime import datetime
import logging
import time
from pathlib import Path



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

load_dotenv()

client = OpenAI(
    api_key = os.getenv("OPENAI_API_KEY")
)


@csrf_exempt
def chatbot_api(request):
    if request.method == "POST":
        data = json.loads(request.body)
        character_name = data.get("character", "Default")  # 요청에서 캐릭터 이름 가져오기
        user_query = data.get("message", "")  # 요청에서 사용자 메시지 가져오기

        if not user_query:
            return JsonResponse({"error": "Message is required"}, status=400)

        try:
            # LLM의 generate_chat_response 호출 (캐릭터 이름과 메시지 전달)
            response = generate_chat_response(character_name, user_query)

            # TTS 생성 파일 경로
            timestamp = int(time.time())
            audio_filename = f"response_{timestamp}.mp3"
            audio_dir = os.path.join(settings.BASE_DIR, 'static', 'audios')
            os.makedirs(audio_dir, exist_ok=True)  # 디렉토리 없을 시 생성
            audio_path = os.path.join(audio_dir, audio_filename)

            # OpenAI TTS 생성
            try:
                tts_response = client.audio.speech.create(
                    model="tts-1-hd",
                    voice="nova",  # 목소리 선택 alloy, ash, coral, echo, fable, onyx, nova, sage, shimmer
                    input=response,  # `generate_chat_response`로 반환된 응답을 TTS로 변환
                    speed="1"
                )
                with open(audio_path, 'wb') as f:
                    f.write(tts_response.read())
            except client.error.OpenAIError as e:
                return JsonResponse({"error": f"TTS generation failed: {str(e)}"}, status=500)

            # 오디오 URL 생성
            audio_url = f"{request.scheme}://{request.get_host()}/static/audios/{audio_filename}"

            # 생성된 텍스트 응답과 오디오 URL 반환
            return JsonResponse({"response": response, "audio_url": audio_url})

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

    return JsonResponse({"error": "Invalid request method"}, status=400)

logger = logging.getLogger(__name__)

@csrf_exempt
def save_audio(request):
    if request.method == 'POST' and request.FILES.get('audio_file'):
        audio_file = request.FILES['audio_file']

        # Generate a unique file name
        unique_id = uuid.uuid4().hex
        timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
        file_extension = os.path.splitext(audio_file.name)[-1]
        unique_filename = f"audio_{timestamp}_{unique_id}{file_extension}"

        save_path = os.path.join(settings.BASE_DIR, 'static/audios', unique_filename)

        # Debug: Log the generated file path and name
        logger.debug(f"Generated file path: {save_path}")

        # Ensure the directory exists
        try:
            os.makedirs(os.path.dirname(save_path), exist_ok=True)
        except Exception as e:
            logger.error(f"Error creating directories: {e}")
            return JsonResponse({'success': False, 'message': 'Error creating directories.'})
        # Save the file
        try:
            with open(save_path, 'wb') as f:
                for chunk in audio_file.chunks():
                    f.write(chunk)
        except Exception as e:
            logger.error(f"Error saving the audio file: {e}")
            return JsonResponse({'success': False, 'message': 'Error saving audio file.'})

        # Call Whisper API to transcribe the audio
        transcription = transcribe_audio_with_whisper(save_path)

        if transcription:
            return JsonResponse({
                'success': True,
                'message': 'Audio saved and transcribed successfully.',
                'filename': unique_filename,
                'transcription': transcription
            })
        else:
            return JsonResponse({
                'success': False,
                'message': 'Audio saved, but transcription failed.'
            })

    return JsonResponse({'success': False, 'message': 'Invalid request.'})

def transcribe_audio_with_whisper(audio_path):
    try:
        # Open the audio file
        with open(audio_path, 'rb') as audio_file:
            # Send the audio file to OpenAI Whisper API
            response = client.audio.transcriptions.create(
                model="whisper-1",  # Whisper 모델 사용
                file=audio_file,
                language="en", # 언어 설정
            )
        
        # Log the API response to check the returned data
        logger.debug(f"Whisper API response: {response}")

        # Extract the transcription from the response
        transcription = response.text
        return transcription

    except Exception as e:
        logger.error(f"Error during transcription: {e}")
        return None