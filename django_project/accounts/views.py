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
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login 
from django.contrib.auth.hashers import make_password
from django.contrib.auth.views import PasswordChangeView
from django.urls import reverse_lazy
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth import logout
from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth.hashers import check_password
from django.views.decorators.csrf import csrf_protect
from django.db import DatabaseError
from django.views.decorators.http import require_POST
import logging
from django.views.decorators.csrf import csrf_exempt



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

def chatbot_page(request):
    # /chatbot/ 경로에서 chatbot.html 템플릿 렌더링
    return render(request, 'chatbot.html')

@login_required  # 로그인한 사용자만 접근 가능
def profile_view(request):
    return render(request, 'profile.html')

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
        voice = data.get("voice", "nova")  # 요청에서 목소리 정보 가져오기 (기본값 "nova")

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
    

# 프로필 페이지
@login_required
def profile_view(request):
    try:
        if request.method == "POST":
            password_form = PasswordChangeForm(request.user, request.POST)
            if password_form.is_valid():
                password_form.save()  # 비밀번호 저장
                update_session_auth_hash(request, password_form.user)  # 세션 유지
                messages.success(request, "비밀번호가 성공적으로 변경되었습니다.")
                return redirect("profile")  # 성공 후 리다이렉트
            else:
                messages.error(request, "비밀번호 변경에 실패했습니다. 입력값을 확인해주세요.")
                logger.warning(f"비밀번호 변경 실패: {password_form.errors}")
        else:
            password_form = PasswordChangeForm(request.user)  # GET 요청 처리

        # 모든 경로에서 password_form을 초기화
        context = {
            "username": request.user.username,
            "email": request.user.email,
            "password_form": password_form,
        }
        return render(request, "profile.html", context)
    except Exception as e:
        logger.error(f"예외 발생: {str(e)}")
        messages.error(request, "알 수 없는 오류가 발생했습니다.")
        return redirect("profile")  # 예외 발생 시 리다이렉트


# 비밀번호 변경
class CustomPasswordChangeView(PasswordChangeView):
    template_name = 'profile.html'
    success_url = reverse_lazy('login')  # 로그인 페이지로 리디렉션

    def form_valid(self, form):
        # 비밀번호 변경 성공 시 기본 동작 유지
        response = super().form_valid(form)
        # 추가: 상태 코드와 JSON 응답 반환
        return JsonResponse({"message": "비밀번호가 성공적으로 변경되었습니다."}, status=200)

    def form_invalid(self, form):
        # 비밀번호 변경 실패 시 기본 동작 유지
        super().form_invalid(form)
        # 추가: 상태 코드와 JSON 응답 반환
        return JsonResponse(
            {"message": "비밀번호 변경에 실패했습니다. 입력 정보를 확인해주세요."},
            status=400,
        )

    def dispatch(self, request, *args, **kwargs):
        # 인증되지 않은 사용자 처리
        if not request.user.is_authenticated:
            return JsonResponse({"message": "인증되지 않은 사용자입니다."}, status=401)
        return super().dispatch(request, *args, **kwargs)


@login_required
@csrf_protect
def logout_view(request):
    if request.method == "POST":
        logout(request)  # 세션 종료
        messages.success(request, "로그아웃 되었습니다.")
        response = JsonResponse({"message": "로그아웃 되었습니다."}, status=200)
        response.set_cookie('csrftoken', request.META.get('CSRF_COOKIE', ''))  # 새 CSRF 토큰 전달
        return response
    return JsonResponse({'error': 'Invalid request method'}, status=400)


logger = logging.getLogger(__name__)


@require_POST
def delete_account_view(request):
    if not request.user.is_authenticated:
        return JsonResponse({"error": "인증되지 않은 사용자입니다."}, status=401)

    try:
        user = request.user
        user.delete()
        return JsonResponse({"message": "회원 탈퇴가 완료되었습니다."}, status=200)
    except Exception as e:
        return JsonResponse({"error": "서버 오류가 발생했습니다.", "details": str(e)}, status=500)