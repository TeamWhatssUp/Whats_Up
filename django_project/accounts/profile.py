from django.contrib.auth import update_session_auth_hash, logout
from django.contrib.auth.forms import PasswordChangeForm
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.contrib import messages

@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])  # 인증된 사용자만 접근 가능
def profile_view(request):
    """
    사용자 프로필 보기 및 업데이트.
    """
    if request.method == 'GET':
        # 사용자 정보 반환
        return Response({
            'username': request.user.username,
            'email': request.user.email,
        })

    elif request.method == 'POST':
        # 요청에 따라 비밀번호 변경 또는 계정 삭제 처리
        if 'delete_account' in request.data:
            request.user.delete()
            return Response({'message': 'Account successfully deleted.'})

        elif 'password_change' in request.data:
            form = PasswordChangeForm(request.user, request.data)
            if form.is_valid():
                user = form.save()
                update_session_auth_hash(request, user)  # 세션 무효화 방지
                return Response({'message': 'Password successfully changed.'})
            else:
                return Response({'error': 'Error changing password.'}, status=400)


@api_view(['POST'])
@permission_classes([IsAuthenticated])  # 인증된 사용자만 접근 가능
def logout_view(request):
    """
    사용자 로그아웃 처리.
    """
    logout(request)
    return Response({'message': 'Successfully logged out.'})
