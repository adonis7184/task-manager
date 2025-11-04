from django.dispatch import receiver
from allauth.account.signals import user_logged_in
from django.core.mail import send_mail
from django.conf import settings

@receiver(user_logged_in)
def send_welcome_email(request, user, **kwargs):
    print("User logged in signal received for user:", user.email, user.username)
    # Only trigger if the login is via a social account (Google)
    if user.socialaccount_set.filter(provider='google').exists():
        send_mail(
            subject="Welcome Back!",
            message=f"Hi {user.get_full_name() or user.username}, thanks for logging in with Google!",
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[user.email],
            fail_silently=False,
        )