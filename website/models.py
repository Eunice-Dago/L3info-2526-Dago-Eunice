from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User


class Banner(models.Model):
    PAGE_CHOICES = [
        ('Home', 'Home'),
        ('About', 'About'),
        ('Contact', 'Contact'),
        ('Service', 'Service'),
        ('Service_Detail', 'Service Detail'),
        ('Gallery', 'Gallery'),
        ('Team', 'Team'),
        ('Pricing', 'Pricing'),
        ('Blog', 'Blog'),
    ]
    
    page = models.CharField(max_length=20, choices=PAGE_CHOICES)
    title = models.CharField(max_length=200)
    nom = models.CharField(max_length=200, blank=True)
    image = models.ImageField(upload_to="banner/")
    
    def __str__(self):
        return f"{self.page} - {self.title}"

class About(models.Model):
    """Section À propos simple"""
    section_title = models.CharField(max_length=100, default="À propos de nous")
    about_title = models.CharField(max_length=200)
    description = models.TextField()
    about_author = models.CharField(max_length=100, blank=True)
    about_fonction = models.CharField(max_length=150, blank=True)
    main_image = models.ImageField(upload_to="about/", blank=True, null=True)
    
    def __str__(self):
        return self.about_title


class ServiceAbout(models.Model):
    """Service dans la section À propos"""
    about = models.ForeignKey(About, on_delete=models.CASCADE, related_name="about_service")
    title = models.CharField(max_length=100)
    description = models.TextField(max_length=300)
    img = models.CharField(max_length=100, help_text="Nom du fichier image (ex: 'icon1.png')")
    
    def __str__(self):
        return self.title


class Collection(models.Model):
    """Section Collections/Exclusives"""
    section_title = models.CharField(max_length=100, default="NOS COLLECTIONS EXCLUSIVES")
    main_title = models.CharField(max_length=200, default="Découvrez nos gammes de bijoux raffinés")
    description = models.TextField(default="Des créations uniques pour chaque occasion, de l'élégance discrète à la pièce statement")
    
    def __str__(self):
        return "Section Collections"


class CollectionItem(models.Model):
    """Élément d'une collection"""
    collection = models.ForeignKey(Collection, on_delete=models.CASCADE, related_name="items")
    title = models.CharField(max_length=100, help_text="Ex: Collection Or")
    image = models.ImageField(upload_to="collections/", help_text="Image de la collection")
    link = models.CharField(max_length=200, blank=True, help_text="Lien vers la page de détail")
    display_order = models.IntegerField(default=1, help_text="Ordre d'affichage")
    
    class Meta:
        ordering = ['display_order']
    
    def __str__(self):
        return self.title
    

class CTA(models.Model):
    """Section Call To Action / Pourquoi Nous Choisir"""
    section_title = models.CharField(
        max_length=100, 
        default="Pourquoi Nous Choisir"
    )
    main_title = models.CharField(
        max_length=200, 
        default="Des bijoux qui racontent votre histoire !"
    )
    description = models.TextField(
        default="Chaque pièce est une œuvre d'art unique, créée avec passion et expertise. De la conception à la réalisation, nous nous engageons pour l'excellence et l'authenticité."
    )
    
    # Section téléphone
    phone_label = models.CharField(
        max_length=100, 
        default="CONSEIL PERSONNALISÉ"
    )
    phone_number = models.CharField(
        max_length=50, 
        default="+33 1 23 45 67 89"
    )
    phone_display = models.CharField(
        max_length=50, 
        default="+33 1 23 45 67 89"
    )
    
    # Image de fond
    background_image = models.ImageField(
        upload_to="cta/", 
        blank=True, 
        null=True,
        help_text="Image de fond pour la section"
    )
    
    # Options d'affichage
    is_active = models.BooleanField(default=True)
    
    def __str__(self):
        return "Section CTA - Pourquoi Nous Choisir"
    
    def get_phone_url(self):
        """Retourne le numéro formaté pour les liens tel:"""
        return self.phone_number.replace(" ", "")


from django_resized import ResizedImageField  # Assure-toi que c'est importé

class Service(models.Model):
    """Service/avantage à mettre en avant"""
    title = models.CharField(max_length=100, verbose_name="Titre")
    description = models.TextField(max_length=200, verbose_name="Description")
    
    # REMPLACE ImageField par ResizedImageField
    icon_image = ResizedImageField(
        upload_to='services/icons/',
        size=[120, 120],  # TAILLE FIXE : 120x120px (change selon tes besoins)
        quality=85,
        force_format='WEBP',
        blank=True,
        null=True,
        verbose_name="Image icône"
    )
    
    icon_filename = models.CharField(
        max_length=100,
        blank=True,
        help_text="Nom du fichier dans static (ex: '1.svg')"
    )
    order = models.IntegerField(default=1, verbose_name="Ordre d'affichage")
    is_active = models.BooleanField(default=True, verbose_name="Actif")
    
    class Meta:
        verbose_name = "Service"
        verbose_name_plural = "Services"
        ordering = ['order', 'title']
    
    def __str__(self):
        return self.title
    
    def get_icon_url(self):
        """Retourne l'URL de l'icône"""
        if self.icon_image and hasattr(self.icon_image, 'url'):
            return self.icon_image.url
        elif self.icon_filename:
            return f"/static/website/assets/imgs/about/{self.icon_filename}"
        return ""
    
    def get_icon_thumbnail_url(self, size=80):
        """Retourne une miniature de taille spécifique"""
        if self.icon_image and hasattr(self.icon_image, 'url'):
            # Pour ResizedImageField, tu peux créer différentes tailles
            base_url = self.icon_image.url.rsplit('.', 1)[0]
            return f"{base_url}_{size}x{size}.webp"
        return self.get_icon_url()
    
class PricingPlan(models.Model):
    """Modèle simple pour les plans de tarification"""
    
    PLAN_CHOICES = [
        ('basic', 'Basic'),
        ('popular', 'Popular'),
        ('enterprise', 'Enterprise'),
    ]
    
    # Données principales du template
    plan_type = models.CharField(max_length=20, choices=PLAN_CHOICES, default='basic')
    title = models.CharField(max_length=100, default="", blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    period = models.CharField(max_length=20, default="/month")
    description = models.CharField(max_length=200, default="All plans include a 30 day trial!")
    
    # Caractéristiques (features) - une par ligne
    feature1 = models.CharField(max_length=200, blank=True)
    feature2 = models.CharField(max_length=200, blank=True)
    feature3 = models.CharField(max_length=200, blank=True)
    feature4 = models.CharField(max_length=200, blank=True)
    feature5 = models.CharField(max_length=200, blank=True)
    feature6 = models.CharField(max_length=200, blank=True)
    
    # Bouton
    button_text = models.CharField(max_length=50, default="CHOOSE PLAN")
    button_url = models.CharField(max_length=200, default="#", blank=True)
    
    # Ordre d'affichage
    order = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)
    
    class Meta:
        ordering = ['order']
    
    def __str__(self):
        return f"{self.get_plan_type_display()} - ${self.price}{self.period}"
    
    def get_features_list(self):
        """Retourne une liste des caractéristiques non vides"""
        features = []
        for i in range(1, 7):
            feature = getattr(self, f'feature{i}', '')
            if feature:  # Ne pas inclure les caractéristiques vides
                features.append(feature)
        return features

class GalleryCategory(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    is_active = models.BooleanField(default=True)
    
    def __str__(self):
        return self.name

class GalleryItem(models.Model):
    MEDIA_TYPES = [
        ('image', 'Image'),
        ('video', 'Video'),
    ]
    
    VIDEO_SOURCES = [
        ('youtube', 'YouTube'),
        ('vimeo', 'Vimeo'),
    ]
    
    title = models.CharField(max_length=200)
    category = models.ForeignKey(GalleryCategory, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='gallery/')
    media_type = models.CharField(max_length=10, choices=MEDIA_TYPES, default='image')
    video_url = models.URLField(blank=True, null=True)
    video_source = models.CharField(max_length=10, choices=VIDEO_SOURCES, blank=True, null=True)
    is_active = models.BooleanField(default=True)
    order = models.IntegerField(default=0)
    
    class Meta:
        ordering = ['order']
    
    def __str__(self):
        return self.title
    

class PortfolioSection(models.Model):
    """Section Portfolio/Galerie"""
    section_title = models.CharField(max_length=100, default="Our Gallery")
    main_title = models.CharField(max_length=200, default="Seamless logistics, faster deliveries")
    description = models.TextField(default="Whatever item needs to be delivered or shipped, we're capable to do that!")
    
    # Options
    is_active = models.BooleanField(default=True)
    
    def __str__(self):
        return "Section Portfolio"


class PortfolioCategory(models.Model):
    """Catégorie de portfolio (filtres)"""
    name = models.CharField(max_length=100, verbose_name="Nom")
    slug = models.SlugField(max_length=100, unique=True)
    css_class = models.CharField(max_length=100, verbose_name="Classe CSS", 
                                 help_text="Classe pour le filtrage (ex: 'roadandtruck')")
    display_order = models.IntegerField(default=1)
    is_active = models.BooleanField(default=True, verbose_name="Actif")
    
    class Meta:
        verbose_name = "Catégorie Portfolio"
        verbose_name_plural = "Catégories Portfolio"
        ordering = ['display_order', 'name']
    
    def __str__(self):
        return self.name


class PortfolioItem(models.Model):
    """Élément du portfolio"""
    ITEM_TYPE_CHOICES = [
        ('image', 'Image'),
        ('video_youtube', 'Vidéo YouTube'),
        ('video_vimeo', 'Vidéo Vimeo'),
    ]
    
    # Informations principales
    title = models.CharField(max_length=200, verbose_name="Titre")
    category = models.ForeignKey(PortfolioCategory, on_delete=models.SET_NULL, 
                                 null=True, related_name='items', verbose_name="Catégorie")
    item_type = models.CharField(max_length=20, choices=ITEM_TYPE_CHOICES, 
                                 default='image', verbose_name="Type")
    
    # Images
    thumbnail = models.ImageField(upload_to='portfolio/thumbnails/', verbose_name="Miniature")
    full_image = models.ImageField(upload_to='portfolio/full/', blank=True, null=True,
                                   verbose_name="Image pleine taille")
    
    # Pour les vidéos
    video_url = models.URLField(blank=True, verbose_name="URL vidéo")
    video_id = models.CharField(max_length=100, blank=True, verbose_name="ID vidéo")
    
    # Ordre et statut
    display_order = models.IntegerField(default=1, verbose_name="Ordre d'affichage")
    is_featured = models.BooleanField(default=False, verbose_name="En vedette")
    is_active = models.BooleanField(default=True, verbose_name="Actif")
    
    # Dates
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Date de création")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Date de modification")
    
    class Meta:
        verbose_name = "Élément Portfolio"
        verbose_name_plural = "Éléments Portfolio"
        ordering = ['display_order', '-created_at']
    
    def __str__(self):
        return self.title
    
    def get_media_url(self):
        """Retourne l'URL appropriée selon le type"""
        if self.item_type == 'image':
            if self.full_image:
                return self.full_image.url
            return self.thumbnail.url
        return self.video_url
    
    def get_popup_class(self):
        """Retourne la classe CSS pour la popup"""
        if self.item_type == 'image':
            return 'image-popup-vertical-fit'
        elif self.item_type == 'video_youtube':
            return 'popup-youtube'
        elif self.item_type == 'video_vimeo':
            return 'popup-vimeo'
        return ''
    
    def is_video(self):
        """Vérifie si c'est une vidéo"""
        return self.item_type in ['video_youtube', 'video_vimeo']
    

class ContactInfo(models.Model):
    """Informations de contact"""
    section_title = models.CharField(max_length=100, default="Get In Touch")
    main_title = models.CharField(max_length=200, default="Talk or Meet with Us")
    
    # Adresse
    address_title = models.CharField(max_length=100, default="Get Us Here")
    address_line1 = models.CharField(max_length=200, default="1355 Market St, Suite 900")
    address_line2 = models.CharField(max_length=200, default="San Francisco, CA 94")
    
    # Téléphone
    phone_title = models.CharField(max_length=100, default="Call Us")
    phone_number = models.CharField(max_length=50, default="+1 123 456 7890")
    
    # Email
    email_title = models.CharField(max_length=100, default="Write Us")
    email_address = models.EmailField(default="info@thisone.com")
    
    # Section formulaire
    form_title = models.CharField(max_length=100, default="Estimate Project")
    form_heading = models.CharField(max_length=200, default="Let Us Know Here")
    submit_button_text = models.CharField(max_length=50, default="SEND MESSAGE")
    
    # Options
    is_active = models.BooleanField(default=True)
    
    def __str__(self):
        return "Informations de contact"


class ContactMessage(models.Model):
    """Messages envoyés via le formulaire de contact"""
    STATUS_CHOICES = [
        ('new', 'Nouveau'),
        ('read', 'Lu'),
        ('replied', 'Répondu'),
        ('archived', 'Archivé'),
    ]
    
    name = models.CharField(max_length=100, verbose_name="Nom")
    email = models.EmailField(verbose_name="Email")
    website = models.URLField(blank=True, null=True, verbose_name="Site web")
    message = models.TextField(verbose_name="Message")
    
    # Métadonnées
    ip_address = models.GenericIPAddressField(blank=True, null=True, verbose_name="Adresse IP")
    user_agent = models.TextField(blank=True, verbose_name="User Agent")
    
    # Statut
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='new', verbose_name="Statut")
    
    # Dates
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Date d'envoi")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Date de modification")
    
    class Meta:
        verbose_name = "Message de contact"
        verbose_name_plural = "Messages de contact"
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Message de {self.name} - {self.created_at.strftime('%d/%m/%Y')}"

class SiteSetting(models.Model):
    site_name = models.CharField(max_length=100, default="TP WEB L3 Info")
    site_description = models.TextField(blank=True)
    contact_email = models.EmailField(default="contact@example.com")
    contact_phone = models.CharField(max_length=20, default="+1 234 567890")
    address = models.TextField(blank=True)
    twitter_url = models.URLField(blank=True)
    facebook_url = models.URLField(blank=True)
    linkedin_url = models.URLField(blank=True)
    
    def __str__(self):
        return "Site Settings"
    
    class Meta:
        verbose_name_plural = "Site Settings"



class NavigationItem(models.Model):
    """Élément de menu de navigation"""
    title = models.CharField(max_length=100, help_text="Texte du lien")
    url = models.CharField(max_length=200, help_text="URL ou nom de route Django")
    is_external = models.BooleanField(default=False, help_text="Lien externe?")
    order = models.IntegerField(default=1, help_text="Ordre d'affichage")
    is_active = models.BooleanField(default=True)
    
    # Pour les éléments avec dropdown
    has_dropdown = models.BooleanField(default=False)
    parent = models.ForeignKey(
        'self', 
        on_delete=models.CASCADE, 
        null=True, 
        blank=True, 
        related_name='children'
    )
    
    class Meta:
        ordering = ['order', 'title']
        verbose_name = "Élément de navigation"
        verbose_name_plural = "Éléments de navigation"
    
    def __str__(self):
        return self.title


class SiteSettings(models.Model):
    """Paramètres généraux du site"""
    site_name = models.CharField(max_length=100, default="Bijoux & Créations")
    logo = models.ImageField(upload_to="logo/", blank=True, null=True)
    logo_white = models.ImageField(upload_to="logo/", blank=True, null=True)
    buy_button_text = models.CharField(max_length=50, default="ACHETER MAINTENANT")
    buy_button_url = models.CharField(max_length=200, default="#")
    
    def __str__(self):
        return "Paramètres du site"
    
    class Meta:
        verbose_name = "Paramètres du site"
        verbose_name_plural = "Paramètres du site"


from django.utils.text import slugify

class BlogCategory(models.Model):
    """Catégorie d'article de blog"""
    name = models.CharField(max_length=100, verbose_name="Nom")
    slug = models.SlugField(unique=True, max_length=100)
    description = models.TextField(blank=True, verbose_name="Description")
    icon_class = models.CharField(max_length=50, blank=True, verbose_name="Classe icône")
    order = models.IntegerField(default=1, verbose_name="Ordre d'affichage")
    
    class Meta:
        verbose_name = "Catégorie"
        verbose_name_plural = "Catégories"
        ordering = ['order', 'name']
    
    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class Tag(models.Model):
    """Tag pour les articles"""
    name = models.CharField(max_length=50, verbose_name="Nom")
    slug = models.SlugField(unique=True, max_length=50)
    
    class Meta:
        verbose_name = "Tag"
        verbose_name_plural = "Tags"
    
    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


from django.db import models
from django.utils import timezone
from django_resized import ResizedImageField
from django.utils.text import slugify
from django.urls import reverse

class BlogPost(models.Model):
    """Modèle simple pour les articles de blog"""
    
    CATEGORY_CHOICES = [
        ('inspiration', 'Inspiration'),
        ('news', 'News'),
        ('tips', 'Tips & Tricks'),
        ('company', 'Company News'),
        ('industry', 'Industry Insights'),
    ]
    
    # Titre et contenu
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True, blank=True)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, default='inspiration')
    excerpt = models.TextField(max_length=300, help_text="Court extrait affiché sur la page d'accueil")
    content = models.TextField(help_text="Contenu complet de l'article")
    
    # Image
    image = ResizedImageField(
        size=[800, 450],
        quality=85,
        upload_to='blog/',
        help_text="Image d'illustration (format recommandé: 800x450px)"
    )
    
    # Auteur et dates
    author = models.CharField(max_length=100, default="Admin")
    published_date = models.DateField(default=timezone.now)
    
    # Métriques (peuvent être mises à jour automatiquement ou manuellement)
    view_count = models.PositiveIntegerField(default=0)
    comment_count = models.PositiveIntegerField(default=0)
    
    # SEO et organisation
    meta_description = models.CharField(max_length=160, blank=True)
    is_featured = models.BooleanField(default=False, help_text="Mettre en avant sur la page d'accueil")
    is_published = models.BooleanField(default=True)
    order = models.PositiveIntegerField(default=0)
    
    # Dates automatiques
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-published_date', '-created_at']
        verbose_name = "Article de blog"
        verbose_name_plural = "Articles de blog"
    
    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        """Génère automatiquement le slug si vide"""
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)
    
    def get_absolute_url(self):
        """URL pour accéder à l'article en détail"""
        return reverse('blog_detail', kwargs={'slug': self.slug})
    
    def increment_view_count(self):
        """Incrémente le compteur de vues"""
        self.view_count += 1
        self.save(update_fields=['view_count'])
    
    @property
    def formatted_date(self):
        """Retourne la date formatée joliment"""
        return self.published_date.strftime("%d %b, %Y")
    


class Comment(models.Model):
    """Commentaire sur un article"""
    post = models.ForeignKey(BlogPost, on_delete=models.CASCADE, 
                             related_name='comments', verbose_name="Article")
    author_name = models.CharField(max_length=100, verbose_name="Nom")
    author_email = models.EmailField(verbose_name="Email")
    content = models.TextField(verbose_name="Commentaire")
    is_approved = models.BooleanField(default=False, verbose_name="Approuvé")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Date")
    
    class Meta:
        verbose_name = "Commentaire"
        verbose_name_plural = "Commentaires"
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Commentaire par {self.author_name} sur {self.post.title}"


class SidebarContent(models.Model):
    """Contenu pour la sidebar du blog"""
    CONTENT_TYPE_CHOICES = [
        ('about', 'À propos'),
        ('popular_posts', 'Articles populaires'),
        ('gallery', 'Galerie'),
        ('tags', 'Tags'),
    ]
    
    content_type = models.CharField(max_length=20, choices=CONTENT_TYPE_CHOICES, 
                                    verbose_name="Type de contenu")
    title = models.CharField(max_length=100, verbose_name="Titre")
    content = models.TextField(blank=True, verbose_name="Contenu")
    is_active = models.BooleanField(default=True, verbose_name="Actif")
    order = models.IntegerField(default=1, verbose_name="Ordre")
    
    class Meta:
        verbose_name = "Contenu sidebar"
        verbose_name_plural = "Contenus sidebar"
        ordering = ['order', 'content_type']
    
    def __str__(self):
        return f"{self.get_content_type_display()} - {self.title}"


class Testimonial(models.Model):
    """Témoignage client"""
    name = models.CharField(max_length=100, verbose_name="Nom")
    location = models.CharField(max_length=100, verbose_name="Localisation", help_text="Ex: Los Angeles, USA")
    content = models.TextField(verbose_name="Témoignage")
    photo = models.ImageField(
        upload_to='testimonials/',
        blank=True,
        null=True,
        verbose_name="Photo"
    )
    photo_filename = models.CharField(
        max_length=100,
        blank=True,
        help_text="Nom du fichier dans static (ex: '1.jpg')"
    )
    order = models.IntegerField(default=1, verbose_name="Ordre d'affichage")
    is_active = models.BooleanField(default=True, verbose_name="Actif")
    
    class Meta:
        verbose_name = "Témoignage"
        verbose_name_plural = "Témoignages"
        ordering = ['order', 'name']
    
    def __str__(self):
        return f"{self.name} - {self.location}"
    
    def get_photo_url(self):
        """Retourne l'URL de la photo"""
        if self.photo and hasattr(self.photo, 'url'):
            return self.photo.url
        elif self.photo_filename:
            return f"/static/website/assets/imgs/testimonials/{self.photo_filename}"
        return ""
    
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.utils.translation import gettext_lazy as _
from ckeditor.fields import RichTextField
from django_resized import ResizedImageField

class Slider(models.Model):
    """Modèle pour gérer les slides du slider"""
    
    class TransitionType(models.TextChoices):
        ZOOMOUT = 'zoomout', _('Zoom Out')
        FADE = 'fade', _('Fondu')
        SLIDE = 'slide', _('Glissement')
        PARALLAX = 'parallax', _('Parallaxe')
    
    title = models.CharField(_('Titre'), max_length=200)
    subtitle = models.CharField(_('Sous-titre'), max_length=500, blank=True)
    description = RichTextField(_('Description'), blank=True)
    
    # Image principale du slide
    image = ResizedImageField(
        _('Image'),
        upload_to='slider/images/',
        size=[1920, 1080],
        quality=85,
        force_format='WEBP',
        help_text=_('Image optimisée pour le slider (1920x1080 recommandé)')
    )
    
    # Image miniature pour la navigation
    thumbnail = ResizedImageField(
        _('Miniature'),
        upload_to='slider/thumbnails/',
        size=[60, 60],
        quality=75,
        force_format='WEBP',
        blank=True,
        null=True,
        help_text=_('Miniature 60x60 pour la navigation')
    )
    
    # Vidéo optionnelle en fond
    video = models.FileField(
        _('Vidéo de fond'),
        upload_to='slider/videos/',
        blank=True,
        null=True,
        help_text=_('Vidéo MP4 pour fond (optionnelle)')
    )
    
    # Paramètres du slide
    transition = models.CharField(
        _('Transition'),
        max_length=50,
        choices=TransitionType.choices,
        default=TransitionType.ZOOMOUT
    )
    
    button_text = models.CharField(
        _('Texte du bouton'),
        max_length=50,
        default='BOOK NOW'
    )
    
    button_link = models.CharField(
        _('Lien du bouton'),
        max_length=500,
        default='#',
        help_text=_('URL ou #anchor')
    )
    
    # Ordre d'affichage
    display_order = models.PositiveIntegerField(
        _('Ordre d\'affichage'),
        default=0,
        help_text=_('Plus petit = affiché en premier')
    )
    
    # Activation
    is_active = models.BooleanField(_('Actif'), default=True)
    
    # Durée d'affichage (en secondes)
    display_duration = models.PositiveIntegerField(
        _('Durée d\'affichage (s)'),
        default=5,
        help_text=_('Durée avant changement automatique')
    )
    
    # Dates
    created_at = models.DateTimeField(_('Créé le'), auto_now_add=True)
    updated_at = models.DateTimeField(_('Mis à jour le'), auto_now=True)
    published_date = models.DateTimeField(_('Date de publication'), auto_now_add=True)
    
    class Meta:
        verbose_name = _('Slide')
        verbose_name_plural = _('Slider')
        ordering = ['display_order', 'created_at']
    
    def __str__(self):
        return self.title
    
    @property
    def has_video(self):
        """Vérifie si le slide a une vidéo"""
        return bool(self.video)
    
    def get_background_media(self):
        """Retourne le média de fond approprié"""
        if self.video:
            return {
                'type': 'video',
                'url': self.video.url,
                'poster': self.image.url
            }
        return {
            'type': 'image',
            'url': self.image.url
        }


class SliderSettings(models.Model):
    """Paramètres globaux du slider"""
    
    name = models.CharField(
        _('Nom des paramètres'),
        max_length=100,
        default='Paramètres du Slider'
    )
    
    # Paramètres d'animation
    animation_speed = models.PositiveIntegerField(
        _('Vitesse d\'animation (ms)'),
        default=2000,
        help_text=_('Durée des animations en millisecondes')
    )
    
    autoplay = models.BooleanField(
        _('Lecture automatique'),
        default=True
    )
    
    autoplay_delay = models.PositiveIntegerField(
        _('Délai autoplay (ms)'),
        default=5000,
        help_text=_('Délai entre les slides en millisecondes')
    )
    
    loop = models.BooleanField(
        _('Boucle infinie'),
        default=True
    )
    
    # Navigation
    show_navigation = models.BooleanField(
        _('Afficher la navigation'),
        default=True
    )
    
    show_bullets = models.BooleanField(
        _('Afficher les indicateurs'),
        default=True
    )
    
    show_timer = models.BooleanField(
        _('Afficher la barre de progression'),
        default=True,
        help_text=_('Barre colorée en bas du slider')
    )
    
    timer_color = models.CharField(
        _('Couleur de la barre de progression'),
        max_length=7,
        default='#D22701',
        help_text=_('Couleur hexadécimale (#RRGGBB)')
    )
    
    # Responsive
    mobile_breakpoint = models.PositiveIntegerField(
        _('Point de rupture mobile (px)'),
        default=768,
        help_text=_('Largeur d\'écran pour le mode mobile')
    )
    
    # Ombre noire semi-transparente
    overlay_opacity = models.FloatField(
        _('Opacité de l\'overlay'),
        default=0.5,
        help_text=_('0 = transparent, 1 = opaque'),
        validators=[MinValueValidator(0), MaxValueValidator(1)]
    )
    
    # Paramètres de performance
    lazy_load = models.BooleanField(
        _('Chargement différé'),
        default=True,
        help_text=_('Charge les images seulement quand nécessaire')
    )
    
    preload_images = models.BooleanField(
        _('Préchargement des images'),
        default=True
    )
    
    updated_at = models.DateTimeField(_('Mis à jour le'), auto_now=True)
    
    class Meta:
        verbose_name = _('Paramètres du slider')
        verbose_name_plural = _('Paramètres du slider')
    
    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        # S'assurer qu'il n'y a qu'une seule instance
        self.pk = 1
        super().save(*args, **kwargs)
    
    @classmethod
    def get_settings(cls):
        """Récupère les paramètres (crée une instance par défaut si nécessaire)"""
        obj, created = cls.objects.get_or_create(pk=1, defaults={
            'name': 'Paramètres du Slider',
            'animation_speed': 2000,
            'autoplay': True,
            'autoplay_delay': 5000,
            'loop': True,
            'show_navigation': True,
            'show_bullets': True,
            'show_timer': True,
            'timer_color': '#D22701',
            'mobile_breakpoint': 768,
            'overlay_opacity': 0.5,
            'lazy_load': True,
            'preload_images': True,
        })
        return obj


class CallToAction(models.Model):
    """Modèle pour gérer les appels à action dans le slider"""
    
    slide = models.ForeignKey(
        Slider,
        on_delete=models.CASCADE,
        related_name='ctas',
        verbose_name=_('Slide')
    )
    
    text = models.CharField(_('Texte'), max_length=100)
    link = models.CharField(_('Lien'), max_length=500)
    button_color = models.CharField(
        _('Couleur du bouton'),
        max_length=7,
        default='#D22701'
    )
    
    # Position
    vertical_offset = models.IntegerField(
        _('Décalage vertical'),
        default=120,
        help_text=_('Position verticale depuis le centre')
    )
    
    # Animation
    animation_delay = models.PositiveIntegerField(
        _('Délai d\'animation (ms)'),
        default=1000
    )
    
    is_active = models.BooleanField(_('Actif'), default=True)
    
    class Meta:
        verbose_name = _('Appel à action')
        verbose_name_plural = _('Appels à action')
    
    def __str__(self):
        return f"{self.text} - {self.slide.title}"
    

class ExpertiseSection(models.Model):
    """Section "Notre savoir-faire d'exception" """
    
    SECTION_TITLE_CHOICES = [
        ('excellence', 'Notre Excellence'),
        ('savoir-faire', 'Notre Savoir-faire'),
        ('expertise', 'Notre Expertise'),
    ]
    
    section_title = models.CharField(
        _('Titre de section'),
        max_length=50,
        choices=SECTION_TITLE_CHOICES,
        default='excellence'
    )
    
    main_title = models.CharField(
        _('Titre principal'),
        max_length=200,
        default='Un savoir-faire<br>d\'exception'
    )
    
    description = models.TextField(
        _('Description principale'),
        max_length=500,
        default='Chaque bijou est le fruit d\'un processus créatif rigoureux et d\'une expertise transmise de génération en génération.'
    )
    
    image = models.ImageField(
        _('Image principale'),
        upload_to='expertise/',
        help_text=_('Image pour la section (atelier, artisan, etc.)')
    )
    
    # Ordre et activation
    display_order = models.PositiveIntegerField(
        _('Ordre d\'affichage'),
        default=0,
        help_text=_('Plus petit = affiché en premier')
    )
    
    is_active = models.BooleanField(
        _('Actif'),
        default=True,
        help_text=_('Afficher cette section sur le site')
    )
    
    # Dates
    created_at = models.DateTimeField(_('Créé le'), auto_now_add=True)
    updated_at = models.DateTimeField(_('Mis à jour le'), auto_now=True)
    
    class Meta:
        verbose_name = _('Section Savoir-faire')
        verbose_name_plural = _('Sections Savoir-faire')
        ordering = ['display_order', '-created_at']
    
    def __str__(self):
        return f"Savoir-faire: {self.get_section_title_display()}"
    
    def get_main_title_html(self):
        """Retourne le titre avec les sauts de ligne HTML"""
        return self.main_title.replace('<br>', '<br>')


class ExpertiseItem(models.Model):
    """Éléments de l'accordéon dans la section savoir-faire"""
    
    expertise_section = models.ForeignKey(
        ExpertiseSection,
        on_delete=models.CASCADE,
        related_name='items',
        verbose_name=_('Section Savoir-faire')
    )
    
    title = models.CharField(
        _('Titre de l\'élément'),
        max_length=100,
        help_text=_('Ex: Sélection des Matériaux, Création sur Mesure, etc.')
    )
    
    content = models.TextField(
        _('Contenu'),
        max_length=1000,
        help_text=_('Texte détaillé affiché dans l\'accordéon')
    )
    
    # Identifiant pour l'accordéon Bootstrap
    accordion_id = models.CharField(
        _('ID Accordéon'),
        max_length=50,
        unique=True,
        help_text=_('Identifiant unique pour l\'accordéon (ex: collapseOne, collapseTwo)')
    )
    
    # Paramètres d'affichage
    is_expanded = models.BooleanField(
        _('Déployé par défaut'),
        default=False,
        help_text=_('Si coché, l\'élément sera ouvert au chargement de la page')
    )
    
    display_order = models.PositiveIntegerField(
        _('Ordre d\'affichage'),
        default=0,
        help_text=_('Ordre dans l\'accordéon')
    )
    
    is_active = models.BooleanField(_('Actif'), default=True)
    
    class Meta:
        verbose_name = _('Élément de savoir-faire')
        verbose_name_plural = _('Éléments de savoir-faire')
        ordering = ['display_order', 'title']
        unique_together = ['expertise_section', 'accordion_id']
    
    def __str__(self):
        return f"{self.title} - {self.expertise_section}"
    
    def get_heading_id(self):
        """Génère l'ID pour le header de l'accordéon"""
        return f"heading{self.accordion_id.capitalize().replace('collapse', '')}"
    
    def get_button_class(self):
        """Retourne la classe CSS pour le bouton accordéon"""
        return "accordion-button" + ("" if self.is_expanded else " collapsed")
    
    def get_collapse_class(self):
        """Retourne la classe CSS pour le contenu accordéon"""
        return "accordion-collapse collapse" + (" show" if self.is_expanded else "")
    

class TeamMember(models.Model):
    """Membre de l'équipe"""
    
    SOCIAL_MEDIA_CHOICES = [
        ('twitter', 'Twitter'),
        ('facebook', 'Facebook'),
        ('linkedin', 'LinkedIn'),
        ('dribbble', 'Dribbble'),
        ('behance', 'Behance'),
        ('instagram', 'Instagram'),
        ('github', 'GitHub'),
    ]
    
    name = models.CharField(
        _('Nom'),
        max_length=100,
        help_text=_('Prénom ou nom complet')
    )
    
    position = models.CharField(
        _('Poste'),
        max_length=100,
        help_text=_('Ex: CEO, Director, Manager, etc.')
    )
    
    image = models.ImageField(
        _('Photo'),
        upload_to='team/',
        help_text=_('Photo du membre (format carré recommandé: 400x400px)')
    )
    
    bio = models.TextField(
        _('Biographie'),
        max_length=500,
        blank=True,
        help_text=_('Description courte du membre (optionnel)')
    )
    
    # Réseaux sociaux (stockés dans un JSONField pour flexibilité)
    social_media = models.JSONField(
        _('Réseaux sociaux'),
        default=dict,
        blank=True,
        help_text=_('Format: {"twitter": "url", "linkedin": "url"}')
    )
    
    # Ordre et visibilité
    display_order = models.PositiveIntegerField(
        _('Ordre d\'affichage'),
        default=0,
        help_text=_('Plus petit = affiché en premier')
    )
    
    is_active = models.BooleanField(
        _('Actif'),
        default=True,
        help_text=_('Afficher ce membre dans l\'équipe')
    )
    
    # Dates
    created_at = models.DateTimeField(_('Créé le'), auto_now_add=True)
    updated_at = models.DateTimeField(_('Mis à jour le'), auto_now=True)
    
    class Meta:
        verbose_name = _('Membre d\'équipe')
        verbose_name_plural = _('Membres d\'équipe')
        ordering = ['display_order', 'name']
    
    def __str__(self):
        return f"{self.name} - {self.position}"
    
    def get_social_media_list(self):
        """Retourne les réseaux sociaux sous forme de liste pour le template"""
        social_list = []
        for platform, url in self.social_media.items():
            if url:  # Ne pas inclure les URLs vides
                social_list.append({
                    'platform': platform,
                    'url': url,
                    'icon_class': self.get_icon_class(platform)
                })
        return social_list
    
    def get_icon_class(self, platform):
        """Retourne la classe CSS pour l'icône du réseau social"""
        icon_map = {
            'twitter': 'lab la-twitter',
            'facebook': 'lab la-facebook-f',
            'linkedin': 'lab la-linkedin-in',
            'dribbble': 'lab la-dribbble',
            'behance': 'lab la-behance',
            'instagram': 'lab la-instagram',
            'github': 'lab la-github',
        }
        return icon_map.get(platform, 'lab la-link')


class TeamSection(models.Model):
    """Section "Our Team" avec titre et description"""
    
    section_title = models.CharField(
        _('Titre de section'),
        max_length=100,
        default='Our Team'
    )
    
    main_title = models.CharField(
        _('Titre principal'),
        max_length=200,
        default='Meet our the best crew'
    )
    
    description = models.TextField(
        _('Description'),
        max_length=500,
        default='Whatever item needs to be delivered or shipped, we\'re capable to do that!'
    )
    
    # Relation avec les membres
    members = models.ManyToManyField(
        TeamMember,
        related_name='team_sections',
        verbose_name=_('Membres de l\'équipe'),
        blank=True
    )
    
    # Configuration
    is_active = models.BooleanField(
        _('Actif'),
        default=True,
        help_text=_('Afficher cette section sur le site')
    )
    
    display_order = models.PositiveIntegerField(
        _('Ordre d\'affichage'),
        default=0,
        help_text=_('Position de la section sur la page')
    )
    
    # Style
    background_color = models.CharField(
        _('Couleur de fond'),
        max_length=7,
        default='#f8f9fa',
        help_text=_('Couleur hexadécimale (#RRGGBB)')
    )
    
    created_at = models.DateTimeField(_('Créé le'), auto_now_add=True)
    updated_at = models.DateTimeField(_('Mis à jour le'), auto_now=True)
    
    class Meta:
        verbose_name = _('Section Équipe')
        verbose_name_plural = _('Sections Équipe')
        ordering = ['display_order', '-created_at']
    
    def __str__(self):
        return f"Équipe: {self.main_title}"
    
    def get_active_members(self):
        """Retourne les membres actifs triés"""
        return self.members.filter(is_active=True).order_by('display_order')
    

from django.db import models
from django_resized import ResizedImageField

class Client(models.Model):
    """Modèle pour les clients et récompenses"""
    
    TYPE_CHOICES = [
        ('award', 'Récompense/Prix'),
        ('client', 'Client'),
        ('partner', 'Partenaire'),
        ('certification', 'Certification'),
    ]
    
    # Informations de base
    name = models.CharField(max_length=200, help_text="Nom du client/de la récompense")
    type = models.CharField(max_length=50, choices=TYPE_CHOICES, default='client')
    
    # Image du logo
    logo = ResizedImageField(
        size=[200, 100],
        quality=85,
        upload_to='clients/',
        help_text="Logo (format recommandé: 200x100px)"
    )
    
    # Lien optionnel
    url = models.URLField(blank=True, help_text="Site web du client (optionnel)")
    
    # Description courte
    description = models.TextField(blank=True, help_text="Description courte (optionnel)")
    
    # Ordre d'affichage
    order = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)
    
    # Année de la récompense (optionnel)
    year = models.CharField(max_length=4, blank=True, help_text="Année (ex: 2024)")
    
    # Dates
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['order', 'name']
        verbose_name = "Client/Récompense"
        verbose_name_plural = "Clients/Récompenses"
    
    def __str__(self):
        return self.name
    

class VideoSection(models.Model):
    """Modèle pour la section vidéo"""
    
    # Vidéo
    video_url = models.URLField(
        help_text="URL de la vidéo (Vimeo, YouTube, etc.)",
        default="https://vimeo.com/45830194"
    )
    
    # Icône du bouton play
    play_icon = models.CharField(
        max_length=50,
        default="las la-play",
        help_text="Classe CSS de l'icône (ex: las la-play, fas fa-play)"
    )
    
    # Texte optionnel à côté de l'icône
    button_text = models.CharField(
        max_length=100,
        blank=True,
        help_text="Texte à afficher à côté du bouton play (optionnel)"
    )
    
    # Image de fond
    background_image = models.ImageField(
        upload_to='video/',
        blank=True,
        null=True,
        help_text="Image de fond pour la section vidéo"
    )
    
    # Couleur de fond (alternative à l'image)
    background_color = models.CharField(
        max_length=20,
        default="#000000",
        help_text="Couleur de fond (format hex: #000000) si pas d'image"
    )
    
    # Options d'affichage
    is_active = models.BooleanField(default=True)
    
    # Ordre d'affichage (si tu as plusieurs sections vidéo)
    order = models.IntegerField(default=0)
    
    # Dates
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['order']
        verbose_name = "Section Vidéo"
        verbose_name_plural = "Sections Vidéo"
    
    def __str__(self):
        return f"Section Vidéo {self.order if self.order else ''}".strip()
    
    def get_background_style(self):
        """Retourne le style CSS pour l'arrière-plan"""
        if self.background_image:
            return f"background-image: url('{self.background_image.url}');"
        return f"background-color: {self.background_color};"
    
class ConnectSection(models.Model):
    """Modèle pour la section "Let's Connect" (nouveau nom)"""
    
    # Titres
    section_title = models.CharField(
        max_length=100,
        default="LET's Connect",
        help_text="Titre en haut (ex: LET's Connect)"
    )
    main_title = models.CharField(
        max_length=200,
        default="Ready to Ship with Confidence?",
        help_text="Titre principal"
    )
    subtitle = models.CharField(
        max_length=300,
        default="Effortless Cargo Shipping: Solutions for Businesses of all sizes",
        blank=True,
        help_text="Sous-titre (optionnel)"
    )
    
    # Bouton principal
    button_text = models.CharField(
        max_length=50,
        default="GET A QUOTE",
        help_text="Texte du bouton"
    )
    button_url = models.CharField(
        max_length=200,
        default="#",
        help_text="URL du bouton"
    )
    
    # Style
    background_color = models.CharField(
        max_length=20,
        default="#f5f5f5",
        help_text="Couleur de fond (format hex: #f5f5f5)"
    )
    
    # Options
    is_active = models.BooleanField(default=True)
    display_order = models.IntegerField(
        default=0,
        help_text="Ordre d'affichage (plus petit = en premier)"
    )
    
    # Métadonnées
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['display_order']
        verbose_name = "Section Connexion"
        verbose_name_plural = "Sections Connexion"
    
    def __str__(self):
        return f"Connect: {self.main_title[:30]}..."
    
    def get_background_style(self):
        """Retourne le style CSS pour l'arrière-plan"""
        return f"background-color: {self.background_color};"
    
from django_resized import ResizedImageField
from django.utils.text import slugify

class JewelryCollection(models.Model):
    """Modèle pour les collections de bijoux"""
    
    CATEGORY_CHOICES = [
        ('gold', 'Collection Or'),
        ('silver', 'Collection Argent'),
        ('platinum', 'Collection Platine'),
        ('wedding', 'Bijoux de Mariage'),
        ('custom', 'Création Sur Mesure'),
        ('repair', 'Réparation & Restauration'),
    ]
    
    # Informations de base
    name = models.CharField(max_length=200, help_text="Nom de la collection")
    slug = models.SlugField(max_length=200, unique=True, blank=True)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    
    # Description
    short_description = models.TextField(max_length=300, help_text="Description courte")
    long_description = models.TextField(help_text="Description détaillée")
    
    # Images
    main_image = ResizedImageField(
        size=[800, 600],
        quality=85,
        upload_to='collections/main/',
        help_text="Image principale de la collection"
    )
    featured_image = ResizedImageField(
        size=[400, 300],
        quality=85,
        upload_to='collections/featured/',
        blank=True,
        null=True,
        help_text="Image pour la liste des collections"
    )
    
    # Caractéristiques
    material = models.CharField(max_length=100, default="Argent 925", help_text="Matériau principal")
    purity = models.CharField(max_length=50, blank=True, help_text="Pureté (ex: 925, 18K)")
    
    # Processus
    fabrication_process = models.TextField(blank=True, help_text="Description du processus de fabrication")
    delivery_time = models.CharField(max_length=100, blank=True, default="2-5 jours ouvrables")
    custom_order_time = models.CharField(max_length=100, blank=True, default="3-4 semaines")
    
    # Options
    is_active = models.BooleanField(default=True)
    is_featured = models.BooleanField(default=False, help_text="Mettre en avant sur la page d'accueil")
    order = models.IntegerField(default=0)
    
    # Métadonnées
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['order', 'name']
        verbose_name = "Collection de bijoux"
        verbose_name_plural = "Collections de bijoux"
    
    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)
    
    def get_absolute_url(self):
        return f"/collections/{self.slug}/"

class CollectionFeature(models.Model):
    """Caractéristiques/avantages d'une collection"""
    
    collection = models.ForeignKey(
        JewelryCollection, 
        on_delete=models.CASCADE, 
        related_name='features'
    )
    
    title = models.CharField(max_length=200)
    icon = models.CharField(
        max_length=50, 
        default="las la-gem",
        help_text="Classe d'icône (ex: las la-gem, las la-award)"
    )
    order = models.IntegerField(default=0)
    
    class Meta:
        ordering = ['order']
        verbose_name = "Caractéristique"
        verbose_name_plural = "Caractéristiques"
    
    def __str__(self):
        return f"{self.collection.name} - {self.title}"

class CollectionFAQ(models.Model):
    """FAQ pour une collection"""
    
    collection = models.ForeignKey(
        JewelryCollection, 
        on_delete=models.CASCADE, 
        related_name='faqs'
    )
    
    question = models.CharField(max_length=300)
    answer = models.TextField()
    order = models.IntegerField(default=0)
    
    class Meta:
        ordering = ['order']
        verbose_name = "Question/Réponse"
        verbose_name_plural = "Questions/Réponses"
    
    def __str__(self):
        return f"{self.collection.name}: {self.question[:50]}..."


from django.db import models
from django.utils import timezone
from django.utils.html import format_html
from django.urls import reverse
from django_resized import ResizedImageField
from django.core.validators import MinValueValidator

class BlogBanner(models.Model):
    """Modèle pour les bannières d'articles de blog"""
    
    # Page d'affichage (optionnel - si vous voulez filtrer par page)
    PAGE_CHOICES = [
        ('blog_1', 'Blog_1'),
        ('blog_2', 'Blog_2'),
        ('blog_3', 'Blog_3'),
    ]
    
    page = models.CharField(
        max_length=50,
        choices=PAGE_CHOICES,
        default='blog',
        verbose_name="Page d'affichage",
        help_text="Sélectionnez sur quelle page cette bannière s'affichera"
    )
    
    # Catégorie (comme "transportation" dans votre exemple)
    category = models.CharField(
        max_length=100,
        verbose_name="Catégorie",
        help_text="Ex: Transportation, Fashion, Lifestyle, etc."
    )
    
    # Titre principal (peut contenir du HTML pour les sauts de ligne)
    title = models.TextField(
        verbose_name="Titre principal",
        help_text="Peut contenir des balises <br> pour les sauts de ligne"
    )
    
    # URL de l'article associé
    article_url = models.CharField(
        max_length=500,
        verbose_name="URL de l'article",
        blank=True,
        null=True,
        help_text="Lien vers l'article complet (optionnel)"
    )
    
    # Informations de l'auteur
    author = models.CharField(
        max_length=100,
        verbose_name="Auteur",
        default="John"
    )
    
    # Date de publication
    published_date = models.DateTimeField(
        verbose_name="Date de publication",
        default=timezone.now
    )
    
    # Nombre de commentaires
    comment_count = models.PositiveIntegerField(
        verbose_name="Nombre de commentaires",
        default=0,
        validators=[MinValueValidator(0)]
    )
    
    # Nombre de vues (format "5.5K" dans votre exemple)
    view_count = models.PositiveIntegerField(
        verbose_name="Nombre de vues",
        default=0,
        validators=[MinValueValidator(0)]
    )
    
    # Image de fond (optionnel)
    background_image = ResizedImageField(
        upload_to='blog_banners/%Y/%m/%d/',
        size=[1920, 600],
        quality=85,
        force_format='WEBP',
        verbose_name="Image de fond",
        blank=True,
        null=True,
        help_text="Image de fond recommandée: 1920x600px"
    )
    
    # Image alternative (pour CSS background)
    background_color = models.CharField(
        max_length=7,
        default='#1a1a1a',
        verbose_name="Couleur de fond",
        help_text="Couleur hexadécimale (ex: #1a1a1a) si pas d'image"
    )
    
    # Statut d'activation
    is_active = models.BooleanField(
        verbose_name="Actif",
        default=True,
        help_text="Cocher pour afficher cette bannière"
    )
    
    # Ordre d'affichage
    display_order = models.IntegerField(
        verbose_name="Ordre d'affichage",
        default=0,
        help_text="Plus petit = affiché en premier"
    )
    
    # Métadonnées
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Créé le")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Modifié le")
    
    class Meta:
        verbose_name = "Bannière Blog"
        verbose_name_plural = "Bannières Blog"
        ordering = ['display_order', '-published_date']
        indexes = [
            models.Index(fields=['is_active', 'display_order']),
            models.Index(fields=['page', 'is_active']),
        ]
    
    def __str__(self):
        return f"{self.category} - {self.title[:50]}..."
    
    # Méthodes utilitaires
    def get_background_style(self):
        """Retourne le style CSS pour l'arrière-plan"""
        if self.background_image:
            return format_html(
                'background-image: url("{}"); background-size: cover; background-position: center;',
                self.background_image.url
            )
        return f'background-color: {self.background_color};'
    
    def formatted_date(self):
        """Formatte la date pour l'affichage (ex: 10 Jan, 2020)"""
        return self.published_date.strftime("%d %b, %Y")
    
    def formatted_views(self):
        """Formatte le nombre de vues (ex: 5.5K)"""
        if self.view_count >= 1000:
            return f"{self.view_count/1000:.1f}K"
        return str(self.view_count)
    
    def short_title(self):
        """Titre raccourci sans HTML"""
        import re
        clean_title = re.sub(r'<br[^>]*>', ' ', self.title)
        return clean_title[:100] + '...' if len(clean_title) > 100 else clean_title
    
    def get_absolute_url(self):
        """URL absolue pour le modèle"""
        if self.article_url:
            return self.article_url
        return reverse('blog_detail', kwargs={'slug': self.slug}) if hasattr(self, 'slug') else '#'
    
    # Méthode pour l'admin
    def image_preview(self):
        """Aperçu de l'image pour l'admin"""
        if self.background_image:
            return format_html(
                '<img src="{}" width="150" height="50" style="object-fit: cover;" />',
                self.background_image.url
            )
        return "Aucune image"
    image_preview.short_description = "Aperçu"

class ArticleBlog(models.Model):  # Au lieu de BlogPost
    """Article de blog principal (nouveau nom)"""
    
    # Titre et contenu
    titre = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True, blank=True)
    resume = models.TextField(max_length=300, help_text="Résumé court")
    contenu = models.TextField(help_text="Contenu complet")
    
    # Images
    image_principale = ResizedImageField(
        size=[800, 450],
        quality=85,
        upload_to='articles/principal/',
        help_text="Image principale (800x450px)"
    )
    image_galerie_1 = ResizedImageField(
        size=[800, 450],
        quality=85,
        upload_to='articles/galerie/',
        blank=True,
        null=True
    )
    image_galerie_2 = ResizedImageField(
        size=[800, 450],
        quality=85,
        upload_to='articles/galerie/',
        blank=True,
        null=True
    )
    
    # Auteur
    auteur = models.ForeignKey('AuteurArticle', on_delete=models.SET_NULL, null=True, blank=True)
    
    # Catégorie et tags
    categorie = models.ForeignKey('CategorieArticle', on_delete=models.SET_NULL, null=True)
    mots_cles = models.ManyToManyField('MotCleArticle', blank=True)
    
    # Métadonnées
    date_publication = models.DateTimeField(default=timezone.now)
    est_publie = models.BooleanField(default=True)
    est_en_vedette = models.BooleanField(default=False)
    nombre_vues = models.PositiveIntegerField(default=0)
    
    # Social sharing
    url_facebook = models.CharField(max_length=200, blank=True)
    url_twitter = models.CharField(max_length=200, blank=True)
    url_linkedin = models.CharField(max_length=200, blank=True)
    
    # Citation (blockquote)
    citation = models.TextField(blank=True, help_text="Citation mise en évidence")
    
    class Meta:
        ordering = ['-date_publication']
        verbose_name = "Article"
        verbose_name_plural = "Articles"
    
    def __str__(self):
        return self.titre
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.titre)
        super().save(*args, **kwargs)
    
    def get_absolute_url(self):
        return f"/article/{self.slug}/"
    
    @property
    def nombre_commentaires(self):
        return self.commentaires.filter(est_approuve=True).count()

class AuteurArticle(models.Model):  # Au lieu de BlogAuthor
    """Auteur des articles"""
    nom = models.CharField(max_length=100)
    biographie = models.TextField(blank=True)
    photo = ResizedImageField(
        size=[150, 150],
        quality=85,
        upload_to='auteurs/',
        blank=True,
        null=True
    )
    facebook = models.CharField(max_length=200, blank=True)
    twitter = models.CharField(max_length=200, blank=True)
    linkedin = models.CharField(max_length=200, blank=True)
    
    def __str__(self):
        return self.nom

class CategorieArticle(models.Model):  # Au lieu de BlogCategory
    """Catégorie d'articles"""
    nom = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, unique=True, blank=True)
    description = models.TextField(blank=True)
    ordre = models.IntegerField(default=0)
    
    class Meta:
        ordering = ['ordre', 'nom']
        verbose_name = "Catégorie"
        verbose_name_plural = "Catégories"
    
    def __str__(self):
        return self.nom
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.nom)
        super().save(*args, **kwargs)
    
    def nombre_articles(self):
        return ArticleBlog.objects.filter(categorie=self, est_publie=True).count()

class MotCleArticle(models.Model):  # Au lieu de BlogTag
    """Mots-clés pour les articles"""
    nom = models.CharField(max_length=50)
    slug = models.SlugField(max_length=50, unique=True, blank=True)
    
    def __str__(self):
        return self.nom
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.nom)
        super().save(*args, **kwargs)

class CommentaireArticle(models.Model):  # Au lieu de BlogComment
    """Commentaires sur les articles"""
    article = models.ForeignKey(ArticleBlog, on_delete=models.CASCADE, related_name='commentaires')
    nom = models.CharField(max_length=100)
    email = models.EmailField()
    site_web = models.URLField(blank=True)
    contenu = models.TextField()
    date_creation = models.DateTimeField(auto_now_add=True)
    est_approuve = models.BooleanField(default=True)
    
    # Pour les réponses imbriquées
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='reponses')
    
    class Meta:
        ordering = ['-date_creation']
    
    def __str__(self):
        return f"Commentaire de {self.nom} sur {self.article.titre}"

class SidebarBlog(models.Model):  # Au lieu de BlogSidebarContent
    """Contenu dynamique pour la sidebar du blog"""
    
    TYPE_CHOICES = [
        ('a_propos', 'À propos'),
        ('galerie', 'Galerie photo'),
        ('populaires', 'Articles populaires'),
        ('recents', 'Articles récents'),
    ]
    
    type_section = models.CharField(max_length=50, choices=TYPE_CHOICES)
    titre = models.CharField(max_length=200)
    contenu = models.TextField(blank=True)
    est_actif = models.BooleanField(default=True)
    ordre = models.IntegerField(default=0)
    
    class Meta:
        ordering = ['ordre']
        verbose_name = "Section Sidebar"
        verbose_name_plural = "Sections Sidebar"
    
    def __str__(self):
        return f"{self.get_type_section_display()}: {self.titre}"

class ImageGalerieSidebar(models.Model):  # Au lieu de BlogGalleryImage
    """Images pour la galerie sidebar"""
    section_sidebar = models.ForeignKey(SidebarBlog, on_delete=models.CASCADE, related_name='images_galerie')
    image = ResizedImageField(
        size=[100, 100],
        quality=85,
        upload_to='blog/sidebar/galerie/'
    )
    titre = models.CharField(max_length=100, blank=True)
    ordre = models.IntegerField(default=0)
    
    class Meta:
        ordering = ['ordre']

class ArticlePopulaire(models.Model):  # Au lieu de BlogPopularPost
    """Articles populaires pour la sidebar"""
    article = models.ForeignKey(ArticleBlog, on_delete=models.CASCADE)
    clics = models.PositiveIntegerField(default=0)
    
    class Meta:
        ordering = ['-clics']
        verbose_name = "Article Populaire"
        verbose_name_plural = "Articles Populaires"

# Optionnel : Historique de recherche
class RechercheBlog(models.Model):  # Au lieu de BlogSearch
    """Historique de recherche du blog"""
    requete = models.CharField(max_length=200)
    adresse_ip = models.GenericIPAddressField()
    date_creation = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.requete} - {self.date_creation}"
    

from django.db import models
from django_resized import ResizedImageField
from django.utils import timezone
from django.utils.text import slugify

class ArticleDetail(models.Model):  # Nouveau nom pour éviter conflit
    """Article détaillé pour la page single blog (sidebar droite)"""
    
    # Titre et contenu
    titre = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True, blank=True)
    contenu_principal = models.TextField(help_text="Contenu principal de l'article")
    citation = models.TextField(blank=True, help_text="Citation mise en évidence (blockquote)")
    
    # Images
    image_principale = ResizedImageField(
        size=[800, 450],
        quality=85,
        upload_to='articles/detail/',
        help_text="Image principale (800x450px)"
    )
    image_secondaire = ResizedImageField(
        size=[600, 400],
        quality=85,
        upload_to='articles/detail/',
        blank=True,
        null=True,
        help_text="Image secondaire (600x400px)"
    )
    
    # Auteur
    nom_auteur = models.CharField(max_length=100, default="John Doe")
    photo_auteur = ResizedImageField(
        size=[100, 100],
        quality=85,
        upload_to='auteurs/detail/',
        blank=True,
        null=True,
        help_text="Photo de l'auteur (100x100px)"
    )
    
    # Métadonnées
    date_publication = models.DateTimeField(default=timezone.now)
    est_actif = models.BooleanField(default=True)
    
    # Social sharing
    lien_facebook = models.CharField(max_length=200, blank=True)
    lien_twitter = models.CharField(max_length=200, blank=True)
    lien_linkedin = models.CharField(max_length=200, blank=True)
    
    # Tags
    tag_1 = models.CharField(max_length=50, blank=True, default="UI/UX")
    tag_2 = models.CharField(max_length=50, blank=True, default="Technology")
    tag_3 = models.CharField(max_length=50, blank=True, default="Graphics")
    
    # Liste à puces (optionnel)
    element_liste_1 = models.CharField(max_length=200, blank=True)
    element_liste_2 = models.CharField(max_length=200, blank=True)
    element_liste_3 = models.CharField(max_length=200, blank=True)
    element_liste_4 = models.CharField(max_length=200, blank=True)
    element_liste_5 = models.CharField(max_length=200, blank=True)
    
    class Meta:
        ordering = ['-date_publication']
        verbose_name = "Article Détaillé"
        verbose_name_plural = "Articles Détaillés"
    
    def __str__(self):
        return self.titre
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.titre)
        super().save(*args, **kwargs)
    
    def get_tags_list(self):
        """Retourne une liste des tags non vides"""
        tags = []
        for i in range(1, 4):
            tag = getattr(self, f'tag_{i}', '')
            if tag:
                tags.append(tag)
        return tags
    
    def get_elements_liste(self):
        """Retourne une liste des éléments non vides"""
        elements = []
        for i in range(1, 6):
            element = getattr(self, f'element_liste_{i}', '')
            if element:
                elements.append(element)
        return elements

class CategorieSidebar(models.Model):  # Pour les catégories dans la sidebar
    """Catégories pour la sidebar"""
    nom = models.CharField(max_length=100)
    description = models.CharField(max_length=200, blank=True)
    nombre_articles = models.IntegerField(default=0)
    ordre = models.IntegerField(default=0)
    
    class Meta:
        ordering = ['ordre']
        verbose_name = "Catégorie Sidebar"
        verbose_name_plural = "Catégories Sidebar"
    
    def __str__(self):
        return self.nom

class ArticleSidebar(models.Model):  # Pour les articles dans les tabs
    """Articles pour les tabs Popular/Recent dans la sidebar"""
    
    TYPE_CHOIX = [
        ('populaire', 'Populaire'),
        ('recent', 'Récent'),
    ]
    
    type_article = models.CharField(max_length=20, choices=TYPE_CHOIX)
    titre = models.CharField(max_length=200)
    image = ResizedImageField(
        size=[72, 72],
        quality=85,
        upload_to='sidebar/articles/'
    )
    date_publication = models.DateField(default=timezone.now)
    ordre = models.IntegerField(default=0)
    
    class Meta:
        ordering = ['ordre']
        verbose_name = "Article Sidebar"
        verbose_name_plural = "Articles Sidebar"
    
    def __str__(self):
        return f"{self.get_type_article_display()}: {self.titre}"

class PhotoGalerie(models.Model):  # Pour la galerie photo sidebar
    """Photos pour la galerie sidebar"""
    titre = models.CharField(max_length=100, blank=True)
    image = ResizedImageField(
        size=[100, 100],
        quality=85,
        upload_to='sidebar/galerie/'
    )
    ordre = models.IntegerField(default=0)
    
    class Meta:
        ordering = ['ordre']
        verbose_name = "Photo Galerie"
        verbose_name_plural = "Photos Galerie"
    
    def __str__(self):
        return self.titre if self.titre else f"Photo {self.id}"

class CommentaireDetail(models.Model):  # Pour les commentaires
    """Commentaires pour l'article détaillé"""
    article = models.ForeignKey(ArticleDetail, on_delete=models.CASCADE, related_name='commentaires')
    nom = models.CharField(max_length=100)
    photo = ResizedImageField(
        size=[50, 50],
        quality=85,
        upload_to='commentaires/',
        blank=True,
        null=True
    )
    contenu = models.TextField()
    date_creation = models.DateTimeField(auto_now_add=True)
    est_approuve = models.BooleanField(default=True)
    
    # Pour les réponses
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='reponses')
    
    class Meta:
        ordering = ['-date_creation']
    
    def __str__(self):
        return f"Commentaire de {self.nom}"
    

class ArticleCentre(models.Model):  # Nouveau nom pour éviter conflits
    """Article pour la page single blog sans sidebar (centré)"""
    
    # Titre et contenu
    titre = models.CharField(max_length=200)
    description_courte = models.TextField(max_length=300, help_text="Description courte sous le titre")
    contenu_principal = models.TextField(help_text="Contenu principal")
    citation = models.TextField(blank=True, help_text="Citation (blockquote)")
    sous_titre = models.CharField(max_length=200, blank=True, help_text="Sous-titre après les images")
    texte_sous_titre = models.TextField(blank=True, help_text="Texte sous le sous-titre")
    
    # Images
    image_principale = models.ImageField(upload_to='articles/centre/', help_text="Image principale en haut")
    image_gauche = models.ImageField(upload_to='articles/centre/', blank=True, null=True, help_text="Image à gauche")
    
    # Auteur
    nom_auteur = models.CharField(max_length=100, default="Admin")
    photo_auteur = models.ImageField(upload_to='auteurs/centre/', blank=True, null=True, help_text="Photo de l'auteur")
    bio_auteur = models.TextField(blank=True, help_text="Biographie de l'auteur")
    
    # Tags (3 tags max)
    tag_1 = models.CharField(max_length=50, blank=True, default="UI/UX")
    tag_2 = models.CharField(max_length=50, blank=True, default="Technology")
    tag_3 = models.CharField(max_length=50, blank=True, default="Graphics")
    
    # Liens sociaux
    facebook_auteur = models.URLField(blank=True)
    twitter_auteur = models.URLField(blank=True)
    linkedin_auteur = models.URLField(blank=True)
    
    # Dates
    date_creation = models.DateTimeField(auto_now_add=True)
    date_publication = models.DateField(default=timezone.now)
    
    # Statut
    est_actif = models.BooleanField(default=True)
    
    class Meta:
        verbose_name = "Article Centre"
        verbose_name_plural = "Articles Centre"
        ordering = ['-date_publication']
    
    def __str__(self):
        return self.titre
    
    def tags_list(self):
        """Retourne la liste des tags non vides"""
        tags = []
        if self.tag_1: tags.append(self.tag_1)
        if self.tag_2: tags.append(self.tag_2)
        if self.tag_3: tags.append(self.tag_3)
        return tags
    
    def has_social_links(self):
        """Vérifie si l'auteur a des liens sociaux"""
        return any([self.facebook_auteur, self.twitter_auteur, self.linkedin_auteur])

class CommentaireCentre(models.Model):
    """Commentaires pour les articles centrés"""
    article = models.ForeignKey(ArticleCentre, on_delete=models.CASCADE, related_name='commentaires')
    nom = models.CharField(max_length=100)
    email = models.EmailField(blank=True)
    site_web = models.URLField(blank=True)
    message = models.TextField()
    date_creation = models.DateTimeField(auto_now_add=True)
    approuve = models.BooleanField(default=True)
    
    # Pour les réponses imbriquées
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='reponses')
    
    class Meta:
        ordering = ['-date_creation']
        verbose_name = "Commentaire Centre"
        verbose_name_plural = "Commentaires Centre"
    
    def __str__(self):
        return f"{self.nom} - {self.article.titre[:50]}"
    
    def has_replies(self):
        """Vérifie si le commentaire a des réponses"""
        return self.reponses.exists()


from django.db import models

class FooterInfo(models.Model):
    """Informations générales du footer"""
    
    # Section principale
    nom_entreprise = models.CharField(max_length=100, default="BIJOUX & CRÉATIONS")
    description = models.TextField(default="Artisans joailliers passionnés créant des bijoux uniques et intemporels depuis 2010.")
    
    # Liens sociaux
    instagram = models.URLField(blank=True, help_text="Lien Instagram")
    facebook = models.URLField(blank=True, help_text="Lien Facebook")
    pinterest = models.URLField(blank=True, help_text="Lien Pinterest")
    tiktok = models.URLField(blank=True, help_text="Lien TikTok")
    
    # Contact
    adresse = models.TextField(default="12 Rue de la Joaillerie\n75001 Paris, France")
    email = models.EmailField(default="contact@bijoux-creations.fr")
    telephone = models.CharField(max_length=20, default="+33 1 23 45 67 89")
    
    # Copyright
    copyright_texte = models.CharField(max_length=200, default="BIJOUX & CRÉATIONS ©2025. Tous droits réservés")
    
    # Options
    est_actif = models.BooleanField(default=True)
    
    class Meta:
        verbose_name = "Configuration Footer"
        verbose_name_plural = "Configuration Footer"
    
    def __str__(self):
        return "Configuration du Footer"
    
    def save(self, *args, **kwargs):
        # Garantir qu'il n'y a qu'une seule instance
        self.id = 1
        super().save(*args, **kwargs)
    
    @classmethod
    def load(cls):
        """Charge la configuration unique"""
        obj, created = cls.objects.get_or_create(id=1)
        return obj

class LienFooter(models.Model):
    """Liens de navigation du footer"""
    
    TYPE_CHOICES = [
        ('boutique', 'Boutique'),
        ('collections', 'Collections'),
    ]
    
    # AJOUTE cette ForeignKey pour pouvoir utiliser Inline
    footer = models.ForeignKey(FooterInfo, on_delete=models.CASCADE, related_name='liens', null=True, blank=True)
    
    type_lien = models.CharField(max_length=20, choices=TYPE_CHOICES)
    texte = models.CharField(max_length=100)
    url = models.CharField(max_length=200, default="#")
    ordre = models.IntegerField(default=0)
    
    class Meta:
        ordering = ['type_lien', 'ordre']
        verbose_name = "Lien Footer"
        verbose_name_plural = "Liens Footer"
    
    def __str__(self):
        return f"{self.get_type_lien_display()}: {self.texte}"