from django.shortcuts import render
from django.core.mail import send_mail
from django.http import JsonResponse
from django.conf import settings

def get_client_ip(request):
    """Kullanıcının gerçek IP adresini alır."""
    x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
    if x_forwarded_for:
        ip = x_forwarded_for.split(",")[0]
    else:
        ip = request.META.get("REMOTE_ADDR")
    return ip

def home(request):
    # Kullanıcının session sayacı yoksa oluştur
    if "vote_count" not in request.session:
        request.session["vote_count"] = {"yes": 0, "no": 0}
    return render(request, "index.html")

def vote(request):
    if request.method == "POST":
        choice = request.POST.get("choice")

        # Kullanıcı sayacı
        vote_count = request.session.get("vote_count", {"yes":0,"no":0})
        if choice == "yes":
            vote_count["yes"] += 1
        elif choice == "no":
            vote_count["no"] += 1

        # Session’a kaydet
        request.session["vote_count"] = vote_count

        # IP al
        user_ip = get_client_ip(request)

        # Mail gönder
        send_mail(
            subject=f"Yeni Oy: {choice.upper()}",
            message=f"Kullanıcı IP: {user_ip}\n"
                    f"Oy: {choice}\n"
                    f"Toplam Evet: {vote_count['yes']}, Toplam Hayır: {vote_count['no']}",
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[settings.NOTIFY_EMAIL],
            fail_silently=False
        )

        return JsonResponse({"status": "success", "counts": vote_count})
