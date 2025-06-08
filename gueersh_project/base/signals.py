from allauth.account.signals import email_confirmed
from django.dispatch import receiver
from .models import FeitioProfile

@receiver(email_confirmed)
def create_feitio_profile(sender, request, email_address, **kwargs):
    user = email_address.user

    #Cria FeitioProfile se ainda não existir:
    if not hasattr(user, 'feitio_profile'):
        FeitioProfile.objects.create(user=user)
