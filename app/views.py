from random import randint
from django.conf import settings
from django.shortcuts import redirect, render
from django.core.mail import send_mail
from .models import VerifiedEmail

# Create your views here.
def login_view(request):
    if request.method == "POST":
        email = request.POST.get("email", "").strip()
        if not email:
            return render(request, 'app/login.html', {
                'error': 'Enter an email address.',
                'step': 1,
            })

        otp = str(randint(100000, 999999))
        request.session['user_email'] = email
        request.session['user_otp'] = otp
        send_mail(
            'Your OTP Code',
            f'Your OTP code is: {otp}',
            settings.DEFAULT_FROM_EMAIL,
            [email],
        )
        return redirect('verify_otp')
    return render(request, 'app/login.html')

def verify_otp(request):
    expected_otp = request.session.get('user_otp')
    if request.method == "POST":
        submitted_otp = request.POST.get('user_otp', '').strip()
        if expected_otp and submitted_otp == expected_otp:
            email = request.session.get('user_email', '').strip().lower()
            if email:
                VerifiedEmail.objects.get_or_create(email=email)
            request.session.pop('user_otp', None)
            return render(request, 'app/success.html', {'email': email, 'step': 2})
        return render(request, 'app/failure.html', {'step': 2})

    if not expected_otp:
        return render(request, 'app/failure.html', {'step': 2})
    return render(request, 'app/verify_otp.html', {
        'email': request.session.get('user_email', ''),
        'step': 2,
    })