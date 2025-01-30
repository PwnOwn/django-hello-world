# example/views.py
from datetime import datetime

from django.http import HttpResponse

from django.http import JsonResponse
from groq import Groq

def index(request):
    if request.method == 'POST':
        prompt = request.POST.get('prompt', '请用中文描述Django的主要特点。')
        messages = [{"role": "user", "content": prompt}]
    else:
        messages = [{"role": "user", "content": "请用中文描述Django的主要特点。"}]
    
    client = Groq()
    
    try:
        completion = client.chat.completions.create(
            model="deepseek-r1-distill-llama-70b",
            messages=messages,
            temperature=0.6,
            max_completion_tokens=4096,
            top_p=0.95,
            stream=True,
            stop=None,
        )
        
        response = ""
        for chunk in completion:
            response += chunk.choices[0].delta.content or ""
        
        return JsonResponse({
            "status": "success",
            "result": response
        })
    except Exception as e:
        return JsonResponse({
            "status": "error",
            "message": str(e)
        }, status=500)