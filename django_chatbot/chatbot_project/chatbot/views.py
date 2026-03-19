from django.shortcuts import render
from django.http import JsonResponse
from groq import Groq

# १. तुमची Groq API Key

client = Groq(api_key="   ITH Groq API Key geneerate karun takavi   ")

def chatbot_view(request):
    """चॅटबॉटचे HTML पेज दाखवण्यासाठी."""
    return render(request, "chatbot/chatbot.html")

def chatbot_api(request):
    """चॅटबॉट मेसेज प्रोसेस करण्यासाठी API."""
    if request.method == "POST":
        user_message = request.POST.get("message")

        if not user_message:
            return JsonResponse({"response": "कृपया काहीतरी मेसेज टाईप करा!"})

        try:
            # २. Groq API ला रिक्वेस्ट पाठवणे
            # मॉडेल: llama-3.3-70b-versatile (हे खूप फास्ट आहे)
            completion = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[
                    {
                        "role": "user",
                        "content": user_message
                    }
                ],
                temperature=0.7,
                max_tokens=1024,
            )

            # ३. रिस्पॉन्स मिळवणे
            reply = completion.choices[0].message.content
            return JsonResponse({"response": reply})

        except Exception as e:
            error_str = str(e)
            # जर रेट लिमिट आली तर (कोटा संपला तर)
            if "rate_limit_exceeded" in error_str:
                return JsonResponse({"response": "🤖 सध्या खूप मेसेजेस झाले आहेत. कृपया थोडा वेळ थांबून पुन्हा प्रयत्न करा."})
            
            return JsonResponse({"response": f"🤖 Groq तांत्रिक अडचण: {error_str}"})

    return JsonResponse({"response": "Invalid Request Method"}, status=400)