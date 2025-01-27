from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from .models import ChatRules

def chat_rules_view(request):
    """챗봇 대화 규칙 페이지 렌더링"""
    if request.user.is_authenticated:
        chat_rules, created = ChatRules.objects.get_or_create(user=request.user)
        return render(request, 'chat_rules.html', {
            'introduction': chat_rules.introduction or '',
            'chat_rules': chat_rules.chat_rules or '',
        })
    return render(request, 'chat_rules.html')

@csrf_exempt
def save_chat_rules(request):
    """사용자가 입력한 대화 규칙 저장 후 friends_selection으로 리디렉션"""
    if request.method == 'POST':
        if not request.user.is_authenticated:
            return JsonResponse({'success': False, 'message': '로그인이 필요합니다.'})

        try:
            data = json.loads(request.body)
            introduction = data.get('introduction', '').strip()
            chat_rules = data.get('chat_rules', '').strip()

            # 하나 이상의 필드가 입력되었는지 확인
            if not introduction and not chat_rules:
                return JsonResponse({'success': False, 'message': '하나 이상의 필드를 입력해주세요.'})

            # 사용자별 데이터 저장 또는 업데이트
            chat_rules_obj, created = ChatRules.objects.get_or_create(user=request.user)
            chat_rules_obj.introduction = introduction
            chat_rules_obj.chat_rules = chat_rules
            chat_rules_obj.save()

            # 성공 메시지 추가
            messages.success(request, '저장이 완료되었습니다!')

            # 성공적으로 저장되었을 때 friends_selection 페이지로 리디렉션
            return redirect('friends_selection')

        except json.JSONDecodeError:
            messages.error(request, '잘못된 요청입니다.')
            return redirect('friends_selection')
    
    messages.error(request, 'POST 요청만 허용됩니다.')
    return redirect('friends_selection')

def get_user_chat_rules(user):
    """사용자의 저장된 챗봇 대화 규칙 및 자기소개를 가져오는 헬퍼 함수"""
    if not user.is_authenticated:
        return {'introduction': '', 'chat_rules': ''}

    try:
        chat_rules = ChatRules.objects.get(user=user)
        return {
            'introduction': chat_rules.introduction or '',
            'chat_rules': chat_rules.chat_rules or '',
        }
    except ChatRules.DoesNotExist:
        return {'introduction': '', 'chat_rules': ''}
