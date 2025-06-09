from allauth.account.signals import email_confirmed
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mass_mail
from .models import FeitioProfile, NewsletterSubscriber, Post

@receiver(email_confirmed)
def create_feitio_profile(sender, request, email_address, **kwargs):
    user = email_address.user

    #Cria FeitioProfile se ainda não existir:
    if not hasattr(user, 'feitio_profile'):
        FeitioProfile.objects.create(user=user)


#Signal para enviar newsletter quando um novo post é criado:
"""
@receiver(post_save, sender=Post)
def send_newsletter(sender, instance, created, **kwargs):
    if created:
        emails = list(NewsletterSubscriber.objects.values_list('email', flat=True))
        messages = [
            (
                f"Novo post: {instance.title}",
                f"Olá!\n\nConfira nosso novo post: {instance.title}\n\n{instance.main_description}",
                'no-reply@seudominio.com',
                [email]
            ) for email in emails
        ]
        send_mass_mail(messages, fail_silently=True)
"""
