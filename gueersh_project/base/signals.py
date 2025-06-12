from allauth.account.signals import email_confirmed
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mass_mail
from .models import FeitioProfile, NewsletterSubscriber, Post, Band, Release
from django.conf import settings
from django.urls import reverse

@receiver(email_confirmed)
def create_feitio_profile(sender, request, email_address, **kwargs):
    user = email_address.user

    #Cria FeitioProfile se ainda não existir:
    if not hasattr(user, 'feitio_profile'):
        FeitioProfile.objects.create(user=user)


#Signal para enviar newsletter quando um novo post é publicado:
#@receiver(post_save, sender=Post)
def send_newsletter_post(sender, instance, created, **kwargs):
    if instance.published_at and not instance.email_sent:
        subscribers = NewsletterSubscriber.objects.all()

        if not subscribers.exists():
            return

        subject = f"Novo post: {instance.title}"
        post_url = f"{settings.SITE_URL}/posts/{instance.pk}/"
        summary = instance.main_description

        messages = []
        for subscriber in subscribers:
            unsubscribe_url = f"{settings.SITE_URL}{reverse('newsletter_unsubscription', args=[subscriber.unsubscribe_token])}"
            body = f"""Olá!
            
Temos um novo post: {instance.title}

{summary}

Leia mais em: {post_url}

Se não quiser mais receber nossos e-mails, clique aqui para se descadastrar da newsletter:
{unsubscribe_url}
"""

            messages.append((
                subject,
                body,
                settings.DEFAULT_FROM_EMAIL,
                [subscriber.email]
            ))

        send_mass_mail(messages, fail_silently=True)
        instance.email_sent = True
        instance.save(update_fields=["email_sent"])


#Signal para enviar newsletter quando uma nova banda é publicada:
#@receiver(post_save, sender=Band)
def send_newsletter_band(sender, instance, created, **kwargs):
    if instance.published_at and not instance.email_sent:
        subscribers = NewsletterSubscriber.objects.all()

        if not subscribers.exists():
            return

        subject = f"{instance.name} se juntou ao Feitio!"
        post_url = f"{settings.SITE_URL}/band/{instance.pk}/"

        messages = []
        for subscriber in subscribers:
            unsubscribe_url = f"{settings.SITE_URL}{reverse('newsletter_unsubscription', args=[subscriber.unsubscribe_token])}"
            body = f"""Olá!
            
Uma nova banda acaba de entrar em nosso site: {instance.name}

Saiba mais em: {post_url}

Se não quiser mais receber nossos e-mails, clique aqui para se descadastrar da newsletter:
{unsubscribe_url}
"""

            messages.append((
                subject,
                body,
                settings.DEFAULT_FROM_EMAIL,
                [subscriber.email]
            ))

        send_mass_mail(messages, fail_silently=True)
        instance.email_sent = True
        instance.save(update_fields=["email_sent"])


#Signal para enviar newsletter quando um novo lançamento é publicado:
#@receiver(post_save, sender=Release)
def send_newsletter_release(sender, instance, created, **kwargs):
    if instance.published_at and not instance.email_sent:
        subscribers = NewsletterSubscriber.objects.all()

        if not subscribers.exists():
            return

        subject = f"Novo lançamento de {instance.band.name}: {instance.title}"
        post_url = f"{settings.SITE_URL}/release/{instance.pk}/"

        messages = []
        for subscriber in subscribers:
            unsubscribe_url = f"{settings.SITE_URL}{reverse('newsletter_unsubscription', args=[subscriber.unsubscribe_token])}"
            body = f"""Olá!
            
Um novo lançamento de {instance.band.name} acaba de chegar: {instance.title}

Saiba mais em: {post_url}

Se não quiser mais receber nossos e-mails, clique aqui para se descadastrar da newsletter:
{unsubscribe_url}
"""

            messages.append((
                subject,
                body,
                settings.DEFAULT_FROM_EMAIL,
                [subscriber.email]
            ))

        send_mass_mail(messages, fail_silently=True)
        instance.email_sent = True
        instance.save(update_fields=["email_sent"])