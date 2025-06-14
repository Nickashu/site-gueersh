from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _
import uuid
from django.utils.text import slugify

class FeitioProfile(models.Model):    #Model para usuário personalizado
    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE, related_name='feitio_profile')
    bio = models.TextField(blank=True, null=True)
    #profile_image = models.ImageField(upload_to='profile_images/', blank=True, null=True)

    def __str__(self):
        return self.user.username
    
    class Meta:
        verbose_name = _('Feitio Profile')
        verbose_name_plural = _('Feitio Profiles')

class SocialNetwork(models.Model):     #Model que vai armazenar as redes sociais disponíveis
    name = models.CharField(max_length=50)
    html_icon = models.CharField(max_length=100, help_text="Ex: i class='bi bi-instagram'> i")

    def __str__(self):
        return f"{self.name}"

    class Meta:
        verbose_name = _('Social Network')
        verbose_name_plural = _('Social Networks')

class Band(models.Model):    #Model para informações de bandas
    name = models.CharField("Nome", max_length=200, blank=False, null=False)
    description = models.TextField("Descrição", blank=True, null=True)
    image = models.ImageField("Imagem principal", upload_to='bands/', blank=False, null=False)
    video_link = models.URLField("Link para vídeo", blank=True, null=True)
    spotify_link = models.URLField("Link para Spotify", blank=True, null=True)
    social_networks = models.ManyToManyField(SocialNetwork, through='BandSocialNetwork', related_name='bands')
    members = models.ManyToManyField(FeitioProfile, through='BandFeitioProfile', related_name='bands')
    created_at = models.DateTimeField(auto_now_add=True)
    
    published_at = models.DateTimeField(null=True, blank=True)  #Data de publicação (é feito manualmente pelo admin)
    email_sent = models.BooleanField(default=False)             #Indica se o email de notificação foi enviado para os assinantes da newsletter
    slug = models.SlugField(unique=True, blank=True)    #Slug para URL amigável (gerado automaticamente)

    def __str__(self):
        return f"{self.name}"

    class Meta:
        verbose_name = _('Band')
        verbose_name_plural = _('Bands')
    
    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.name)
            slug = base_slug
            count = 1
            while Band.objects.filter(slug=slug).exists():   #Garante que o slug seja único
                slug = f"{base_slug}-{count}"
                count += 1
            self.slug = slug
        super().save(*args, **kwargs)

class Concert(models.Model):    #Model para informações de shows
    tour = models.ForeignKey('Tour', on_delete=models.CASCADE, related_name='concerts')    #Uma turnê pode ter vários shows
    date = models.DateField(blank=False, null=False, help_text="Data do show")
    city = models.CharField(max_length=100, blank=False, null=False, help_text="Cidade onde o show ocorrerá. Ex: São Paulo", default="")
    state = models.CharField(max_length=100, blank=True, null=True, help_text="Estado onde o show ocorrerá (pode deixar em branco). Ex: SP", default="")
    country = models.CharField(max_length=100, blank=True, null=True, help_text="País onde o show ocorrerá. Ex: Brasil")
    venue = models.CharField(max_length=100, blank=False, null=False, help_text="Local onde o show ocorrerá. Ex: Espaço das Américas")
    
    def __str__(self):
        return f"{self.tour} - Show de {self.date}: {self.city}, {self.state}, {self.country} - {self.venue}"

    class Meta:
        verbose_name = _('Concert')
        verbose_name_plural = _('Concerts')

class Tour(models.Model):    #Model para informações de turnês
    band = models.ForeignKey(Band, on_delete=models.CASCADE, related_name='tours')   #Uma banda pode ter várias turnês
    year = models.CharField(max_length=4, blank=False, null=False)

    def __str__(self):
        return f"{self.band.name} - Tour {self.year}"

    class Meta:
        verbose_name = _('Tour')
        verbose_name_plural = _('Tours')

class Contact(models.Model):    #Model para informações de contato das bandas
    band = models.ForeignKey(Band, on_delete=models.CASCADE, related_name='contacts')   #Uma banda pode ter vários contatos
    role = models.CharField(max_length=100)  #Ex: Imprensa, Booking, Selo...
    name = models.CharField(max_length=100, blank=False, null=False)
    email = models.EmailField()

    def __str__(self):
        return f"{self.band.name}: {self.role} - {self.name}"
    
    class Meta:
        verbose_name = _('Contact')
        verbose_name_plural = _('Contacts')
        
        
class Release(models.Model):    #Model para informações de lançamentos das bandas
    band = models.ForeignKey(Band, on_delete=models.CASCADE, related_name='releases', verbose_name="Banda")    #Uma banda pode ter vários lançamentos
    title = models.CharField("Título", max_length=100, blank=False, null=False)
    image = models.ImageField("Imagem principal", upload_to='releases/', blank=False, null=False)  #Imagem do lançamento (capa do álbum, single, etc.)
    release_date = models.DateField("Data de lançamento", blank=False, null=False)
    description = models.TextField("Descrição", blank=False, null=False)
    video_link = models.URLField("Link para vídeo", blank=True, null=True)
    spotify_link = models.URLField("Link para Spotify", blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    published_at = models.DateTimeField(null=True, blank=True)  #Data de publicação (é feito manualmente pelo admin)
    email_sent = models.BooleanField(default=False)             #Indica se o email de notificação foi enviado para os assinantes da newsletter
    slug = models.SlugField(unique=True, blank=True)    #Slug para URL amigável (gerado automaticamente)

    def __str__(self):
        return f"{self.band.name} - {self.title}"
    
    class Meta:
        verbose_name = _('Release')
        verbose_name_plural = _('Releases')
    
    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.title)
            slug = base_slug
            count = 1
            while Release.objects.filter(slug=slug).exists():   #Garante que o slug seja único
                slug = f"{base_slug}-{count}"
                count += 1
            self.slug = slug
        super().save(*args, **kwargs)

class ReleaseCredits(models.Model):    #Model para informações de créditos dos lançamentos
    release = models.ForeignKey(Release, on_delete=models.CASCADE, related_name='credits')    #Um lançamento pode ter vários créditos
    role = models.CharField(max_length=100, blank=False, null=False)  #Ex: Produção, Mixagem, Masterização...
    crew = models.TextField(blank=False, null=False)    #Equipe responsável pela função

    def __str__(self):
        return f"{self.release.title} - {self.role}"
    
    class Meta:
        verbose_name = _('Release Credit')
        verbose_name_plural = _('Release Credits')


class Post(models.Model):    #Model para informações de posts das bandas
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')    #Um usuário pode ter zero ou vários posts
    title = models.CharField("Título", max_length=200, blank=False, null=False)     #Título do post
    main_image = models.ImageField("Imagem principal", upload_to='posts/', blank=False, null=False)   #Imagem principal do post (que aparece na listagem)
    main_description = models.TextField("Resumo", blank=False, null=False)   #Descrição principal do post (que aparece na listagem)
    content = models.TextField("Conteúdo", blank=False, null=False)   #Conteúdo do post
    created_at = models.DateTimeField(auto_now_add=True)
    
    published_at = models.DateTimeField(null=True, blank=True)  #Data de publicação (é feito manualmente pelo admin)
    email_sent = models.BooleanField(default=False)             #Indica se o email de notificação foi enviado para os assinantes da newsletter

    def __str__(self):
        return f"{self.title}"
    
    class Meta:
        verbose_name = _('Post')
        verbose_name_plural = _('Posts')
    
    def delete(self, *args, **kwargs):
        self.main_image.delete()
        super(Post, self).delete(*args, **kwargs)


class NewsletterSubscriber(models.Model):
    email = models.EmailField(unique=True, null=False, blank=False)
    unsubscribe_token = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)   #Token para cancelar a inscrição
    subscribed_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email
    
    class Meta:
        verbose_name = _('Newsletter Subscriber')
        verbose_name_plural = _('Newsletter Subscribers')


#Tabelas de relação:
class BandSocialNetwork(models.Model):
    band = models.ForeignKey(Band, on_delete=models.CASCADE)
    social_network = models.ForeignKey(SocialNetwork, on_delete=models.CASCADE)
    link = models.URLField(blank=True, null=True)   #Link para a rede social da banda

    def __str__(self):
        return f"{self.band.name} - {self.social_network.name}"

class BandFeitioProfile(models.Model):
    band = models.ForeignKey(Band, on_delete=models.CASCADE)
    feitio_profile = models.ForeignKey(FeitioProfile, on_delete=models.CASCADE)
    role = models.CharField(max_length=100, blank=True, null=True)  #Ex: Vocalista, Guitarrista, Baixista...

    def __str__(self):
        return f"{self.feitio_profile.user.username} - {self.band.name}"
    
    class Meta:
        unique_together = ('feitio_profile', 'band')  #Garante que a dupla (pefil, banda) seja única