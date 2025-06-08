from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _

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
    name = models.CharField(max_length=200, blank=False, null=False)
    description = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to='bands/', blank=True, null=True)
    video_link = models.URLField(blank=True, null=True)
    spotify_link = models.URLField(blank=True, null=True)
    social_networks = models.ManyToManyField(SocialNetwork, through='BandSocialNetwork', related_name='bands')
    members = models.ManyToManyField(FeitioProfile, through='BandFeitioProfile', related_name='bands')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name}"

    class Meta:
        verbose_name = _('Band')
        verbose_name_plural = _('Bands')

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
    band = models.ForeignKey(Band, on_delete=models.CASCADE, related_name='releases')    #Uma banda pode ter vários lançamentos
    title = models.CharField(max_length=100, blank=False, null=False)
    image = models.ImageField(upload_to='releases/', blank=False, null=False)  #Imagem do lançamento (capa do álbum, single, etc.)
    release_date = models.DateField(blank=False, null=False)
    description = models.TextField(blank=False, null=False)
    video_link = models.URLField(blank=True, null=True)
    spotify_link = models.URLField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.band.name} - {self.title}"
    
    class Meta:
        verbose_name = _('Release')
        verbose_name_plural = _('Releases')

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
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')    #Um usuário pode ter zero ou vários posts
    title = models.CharField(max_length=100, blank=False, null=False)     #Título do post
    main_image = models.ImageField(upload_to='posts/', blank=True, null=True)   #Imagem principal do post (que aparece na listagem)
    main_description = models.TextField(blank=False, null=False)   #Descrição principal do post (que aparece na listagem)
    content = models.TextField(blank=False, null=False)   #Conteúdo do post
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title}"
    
    class Meta:
        verbose_name = _('Post')
        verbose_name_plural = _('Posts')
    
    def delete(self, *args, **kwargs):
        self.main_image.delete()
        super(Post, self).delete(*args, **kwargs)



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