from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json

def chat_rules_view(request):
    """챗봇 대화 규칙 페이지 렌더링"""
    return render(request, 'chat_rules.html')

@csrf_exempt
def save_chat_rules(request):
    """사용자가 입력한 대화 규칙 저장"""
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            introduction = data.get('introduction', '')
            chat_rules = data.get('chat_rules', '')

            if not introduction or not chat_rules:
                return JsonResponse({'success': False, 'message': '모든 필드를 입력해주세요.'})

            # 세션에 데이터 저장 (테스트용, 추후 DB 연동 가능)
            request.session['introduction'] = introduction
            request.session['chat_rules'] = chat_rules

            return JsonResponse({'success': True})
        except json.JSONDecodeError:
            return JsonResponse({'success': False, 'message': '잘못된 요청입니다.'})
    
    return JsonResponse({'success': False, 'message': 'POST 요청만 허용됩니다.'})
