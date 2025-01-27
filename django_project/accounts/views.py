from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import UserSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from django.shortcuts import redirect
from .user_profile import profile_view as handle_profile_view
from django.core.files.storage import default_storage
from django.conf import settings
from django.views import View
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.deprecation import MiddlewareMixin
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
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth.hashers import check_password
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from .chat_rules import chat_rules_view, save_chat_rules # 대화 규칙 저장 기능 추가
from .custom_chat import get_user_chat_rules # 저장한 대화 규칙을 챗봇 프롬프트 활용
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login 
from django.contrib.auth.hashers import make_password
from .models import Conversation
from django.db import models
from .models import ChatMessage
# Create your views here.

def index(request):
    return JsonResponse({'message': 'Hello, this is accounts app!'})


class RegisterView(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            validated_data = serializer.validated_data
            # 비밀번호를 해싱
            validated_data['password'] = make_password(validated_data['password'])
            
            # 사용자 객체 생성 및 저장
            user = User.objects.create(**validated_data)

            return Response({'message': 'User created successfully!'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


User = get_user_model()

class UserLoginAPI(APIView):
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        # 현재 설정된 사용자 모델을 동적으로 가져옴
        user = User.objects.filter(username=username).first()

        if user is None:
            return Response(
                {"message": "존재하지 않는 아이디입니다."}, status=status.HTTP_400_BAD_REQUEST
            )

        if not check_password(password, user.password):
            return Response(
                {"message": "비밀번호가 틀렸습니다."}, status=status.HTTP_400_BAD_REQUEST
            )
        
        # Django 세션에 로그인 처리 추가
        login(request, user)  # 로그인 성공 시 세션 생성

        token = TokenObtainPairSerializer.get_token(user)
        refresh_token = str(token)
        access_token = str(token.access_token)

        response = Response(
            {
                "user": UserSerializer(user).data,
                "message": "login success",
                "jwt_token": {
                    "access_token": access_token,
                    "refresh_token": refresh_token
                },
            },
            status=status.HTTP_200_OK
        )
        response.set_cookie("access_token", access_token, httponly=True)
        response.set_cookie("refresh_token", refresh_token, httponly=True)
        return response

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

@login_required
def chatbot_page(request):
    character = request.GET.get('character', 'Default')
    user_chat_rules = get_user_chat_rules(request.user)

    # 사용자 정보 반영한 맞춤형 인트로 생성
    introduction = user_chat_rules.get('introduction', '멋진 하루야!')
    chat_rules = user_chat_rules.get('chat_rules', '자연스럽게 대화하고 싶어요.')

    # 캐릭터 별 맞춤 인트로 설정
    character_intros = {
        "Rachel": f"안녕 나는 Rachel이야. 너는 '{introduction}'한 사람이구나? '{chat_rules}'처럼 대화하고 싶다고 들었어. 나랑 대화하자!",
        "Ross": f"Hey! 나는 Ross야. '{introduction}'가 멋지네. '{chat_rules}' 방식으로 대화해볼까?",
        "Chandler": f"Chandler Bing here! '{introduction}', huh? '{chat_rules}'라니. 재미있겠는걸?",
        "Monica": f"안녕! 나는 Monica야. '{introduction}'이 참 좋아보여! '{chat_rules}'에 따라 대화할게.",
        "Joey": f"How you doin'? '{introduction}'... '{chat_rules}'로 이야기해볼까?",
        "Phoebe": f"Hi! 나는 Phoebe야! '{introduction}', 좋다! '{chat_rules}' 좋아해!",
    }

    display_intro = character_intros.get(character, f"Hello! I'm {character}, let's talk.")

    return render(request, 'chatbot.html', {
        'character': character,
        'introduction': display_intro,  # 인트로가 항상 보이도록 수정
        'chat_rules': ''
    })

@login_required  # 로그인한 사용자만 접근 가능
def profile_view(request):
    return render(request, 'profile.html')

def friends_selection(request):
    # 등장인물 선택 화면 렌더링
    return render(request, 'friends_selection.html')

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
@login_required  # 로그인된 사용자만 접근 가능
def chatbot_api(request):
    if request.method == "POST":
        data = json.loads(request.body)
        character_name = data.get("character", "Default")
        user_query = data.get("message", "")
        voice = data.get("voice", "nova")
        user_id = request.user.id  # 로그인한 사용자의 ID 가져오기

        if not user_query:
            return JsonResponse({"error": "Message is required"}, status=400)

        # 채팅 기록 저장 (사용자 메시지 저장)
        chat_message = ChatMessage.objects.create(user=request.user, character=character_name, message=user_query)

        try:
            # 사용자 정보를 포함하여 챗봇 응답 생성
            response = generate_chat_response(character_name, user_query, user=request.user)

            # 챗봇의 응답을 모델에 저장
            chat_message.response = response  # 챗봇의 응답 저장
            chat_message.save()  # 변경 사항 저장

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
                    voice=voice,  # 전달받은 목소리 사용
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
            audio_url = f"/static/audios/{unique_filename}"  # 생성된 오디오 파일 URL

            return JsonResponse({
                'success': True,
                'message': 'Audio saved and transcribed successfully.',
                'filename': unique_filename,
                'transcription': transcription,
                'audio_url': audio_url  # 오디오 URL 반환
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
    

logger = logging.getLogger(__name__)

@csrf_exempt
def save_conversation(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            conversation_text = data.get('conversation', '')
            
            if not conversation_text:
                return JsonResponse({'status': 'error', 'message': '대화 내용이 없습니다.'})
            
            # 대화 저장
            conversation = Conversation.objects.create(
                user=request.user,
                content=conversation_text
            )
            
            return JsonResponse({'status': 'success'})
            
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)})
    
    return JsonResponse({'status': 'error', 'message': 'POST 요청이 필요합니다.'})




@login_required
def get_conversations(request):
    conversations = Conversation.objects.filter(user=request.user).order_by('-created_at')
    conversation_list = [{'content': c.content, 'created_at': c.created_at} for c in conversations]
    return JsonResponse({'status': 'success', 'conversations': conversation_list})
    
@login_required
def chat_history(request):
    # 로그인한 사용자의 채팅 기록을 가져옵니다. 오름차순으로 정렬
    messages = ChatMessage.objects.filter(user=request.user).order_by('timestamp')
    return render(request, 'chat_history.html', {'messages': messages})

@login_required
def clear_chat_history(request):
    if request.method == "POST":
        try:
            ChatMessage.objects.filter(user=request.user).delete()  # 현재 사용자의 모든 채팅 기록 삭제
            return JsonResponse({"success": True, "message": "Chat history cleared."})
        except Exception as e:
            return JsonResponse({"success": False, "message": str(e)})  # 예외 메시지 반환
    return JsonResponse({"success": False, "message": "Invalid request."})