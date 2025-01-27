from django.shortcuts import render, redirect
from django.contrib.auth import logout, update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
import logging

logger = logging.getLogger(__name__)

@login_required
def profile_view(request):
    """사용자 프로필 페이지 (비밀번호 변경, 로그아웃, 회원 탈퇴 기능 포함)"""
    
    # 디버깅: 로그인 상태 출력
    if request.user.is_authenticated:
        logger.info(f"접속한 사용자: {request.user.username}")
    else:
        logger.warning("사용자가 인증되지 않았습니다.")

    if request.method == 'POST':
        if 'password_change' in request.POST:  # 비밀번호 변경 처리
            password_form = PasswordChangeForm(request.user, request.POST)
            if password_form.is_valid():
                user = password_form.save()
                update_session_auth_hash(request, user)  # 세션 유지
                messages.success(request, "비밀번호가 성공적으로 변경되었습니다.")
                return redirect('login')
            else:
                messages.error(request, "비밀번호 변경에 실패했습니다. 다시 시도해 주세요.")
        elif 'delete_account' in request.POST:  # 회원 탈퇴 처리
            request.user.delete()
            messages.success(request, "회원 탈퇴가 완료되었습니다.")
            return redirect('index')
        elif 'logout' in request.POST:  # 로그아웃 처리
            logout(request)
            messages.success(request, "로그아웃되었습니다.")
            return redirect('login')

    else:
        password_form = PasswordChangeForm(request.user)

    context = {
        'username': request.user.username,
        'email': request.user.email,
        'password_form': password_form,
    }

    # 디버깅 정보 추가
    logger.debug(f"렌더링 프로필 페이지: {request.user.username}")

    return render(request, 'profile.html', context)
