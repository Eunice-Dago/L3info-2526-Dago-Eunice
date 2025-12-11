from django.contrib import admin
from django import forms  # <-- AJOUTE CETTE LIGNE
from .models import *
from .models import Banner, About, Service, ServiceAbout, PricingPlan, GalleryCategory, GalleryItem, ContactInfo,ContactMessage , SiteSetting, Collection, CollectionItem,CTA,NavigationItem, SiteSettings,BlogCategory, Tag, BlogPost, Comment, SidebarContent



@admin.register(Banner)
class BannerAdmin(admin.ModelAdmin):
    list_display = ['page', 'title']
    list_filter = ['page']
    search_fields = ['title']

#admin de la class de la page about
class ServiceAboutInline(admin.TabularInline):
    model = ServiceAbout
    extra = 3

@admin.register(About)
class AboutAdmin(admin.ModelAdmin):
    inlines = [ServiceAboutInline]
    list_display = ['about_title', 'section_title']


class CollectionItemInline(admin.TabularInline):
    model = CollectionItem
    extra = 6
    ordering = ['display_order']

@admin.register(Collection)
class CollectionAdmin(admin.ModelAdmin):
    inlines = [CollectionItemInline]
    list_display = ['main_title', 'section_title']
    
    def has_add_permission(self, request):
        # Empêche d'ajouter plusieurs sections Collections
        return not Collection.objects.exists()

@admin.register(CollectionItem)
class CollectionItemAdmin(admin.ModelAdmin):
    list_display = ['title', 'collection', 'display_order']
    list_editable = ['display_order']
    
@admin.register(CTA)
class CTAAdmin(admin.ModelAdmin):
    list_display = ['section_title', 'main_title', 'is_active']
    list_editable = ['is_active']
    
    fieldsets = (
        ('Contenu principal', {
            'fields': ('section_title', 'main_title', 'description')
        }),
        ('Contact téléphone', {
            'fields': ('phone_label', 'phone_number', 'phone_display')
        }),
        ('Image de fond', {
            'fields': ('background_image',)
        }),
        ('Options', {
            'fields': ('is_active',)
        }),
    )
    
    def has_add_permission(self, request):
        """Limite à une seule section CTA"""
        return not CTA.objects.exists()

@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ['title', 'order', 'is_active']
    list_editable = ['order', 'is_active']
    list_filter = ['is_active']
    search_fields = ['title', 'description']
    ordering = ['order']
    ICON_SIZE_CHOICES = [
        ('small', 'Petit (40x40)'),
        ('medium', 'Moyen (60x60)'),
        ('large', 'Grand (80x80)'),
        ('xlarge', 'Très grand (100x100)'),
    ]
    
    icon_size = models.CharField(
        max_length=10,
        choices=ICON_SIZE_CHOICES,
        default='medium',
        verbose_name="Taille de l'icône"
    )
    
    fieldsets = (
        ('Contenu', {
            'fields': ('title', 'description')
        }),
        ('Icône', {
            'fields': ('icon_image', 'icon_filename')
        }),
        ('Options', {
            'fields': ('order', 'is_active')
        }),
    )
    
    # ... méthodes existantes ...
    
    def get_icon_css_class(self):
        """Retourne la classe CSS selon la taille choisie"""
        size_map = {
            'small': 'icon-small',
            'medium': 'icon-medium',
            'large': 'icon-large',
            'xlarge': 'icon-xlarge',
        }
        return size_map.get(self.icon_size, 'icon-medium')
    

@admin.register(PricingPlan)
class PricingPlanAdmin(admin.ModelAdmin):
    # Ce qui s'affiche dans la liste
    list_display = ('title', 'plan_type', 'price', 'period', 'order', 'is_active')
    
    # Ce qui est éditable directement dans la liste
    list_editable = ('order', 'is_active')
    
    # Filtres sur le côté
    list_filter = ('plan_type', 'is_active')
    
    # Barre de recherche
    search_fields = ('title', 'description')
    
    # Groupement des champs dans le formulaire d'édition
    fieldsets = (
        ('Informations de base', {
            'fields': ('plan_type', 'title', 'price', 'period', 'description', 'order', 'is_active')
        }),
        ('Caractéristiques', {
            'fields': ('feature1', 'feature2', 'feature3', 'feature4', 'feature5', 'feature6'),
            'description': 'Entrez les caractéristiques du plan (une par ligne)'
        }),
        ('Bouton', {
            'fields': ('button_text', 'button_url'),
            'description': 'Configuration du bouton "Choisir le plan"'
        }),
    )

#-----blog----------
@admin.register(BlogCategory)
class BlogCategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'order', 'post_count']
    list_editable = ['order']
    prepopulated_fields = {'slug': ('name',)}
    
    def post_count(self, obj):
        return obj.posts.count()
    post_count.short_description = "Nombre d'articles"

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}

class CommentInline(admin.TabularInline):
    model = Comment
    extra = 0
    readonly_fields = ['author_name', 'author_email', 'content', 'created_at']


from django.contrib import admin
from django.utils.html import format_html
from .models import BlogPost

@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
    # Affichage dans la liste
    list_display = ('title', 'category', 'author', 'published_date', 'view_count','order' ,'is_published', 'is_featured')
    list_filter = ('category', 'is_published', 'is_featured', 'published_date')
    search_fields = ('title', 'content', 'author', 'excerpt')
    list_editable = ('is_published', 'is_featured', 'order')
    ordering = ('-published_date',)
    
    # Prévisualisation de l'image
    readonly_fields = ('image_preview', 'created_at', 'updated_at')
    
    # Organisation des champs dans le formulaire
    fieldsets = (
        ('Contenu', {
            'fields': ('title', 'slug', 'category', 'excerpt', 'content', 'image', 'image_preview')
        }),
        ('Informations', {
            'fields': ('author', 'published_date', 'meta_description')
        }),
        ('Statistiques', {
            'fields': ('view_count', 'comment_count'),
            'classes': ('collapse',)
        }),
        ('Paramètres', {
            'fields': ('is_featured', 'is_published', 'order')
        }),
        ('Dates', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    # Pré-remplissage automatique
    prepopulated_fields = {'slug': ('title',)}
    
    # Méthode pour afficher l'image
    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="max-width: 300px; max-height: 200px;" />', obj.image.url)
        return "Aucune image"
    image_preview.short_description = "Aperçu"


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['author_name', 'post', 'created_at', 'is_approved']
    list_filter = ['is_approved', 'created_at']
    list_editable = ['is_approved']
    search_fields = ['author_name', 'author_email', 'content']
    actions = ['approve_comments']
    
    def approve_comments(self, request, queryset):
        queryset.update(is_approved=True)
        self.message_user(request, f"{queryset.count()} commentaires approuvés.")
    approve_comments.short_description = "Approuver les commentaires sélectionnés"

@admin.register(SidebarContent)
class SidebarContentAdmin(admin.ModelAdmin):
    list_display = ['title', 'content_type', 'is_active', 'order']
    list_filter = ['content_type', 'is_active']
    list_editable = ['is_active', 'order']
    ordering = ['order']

@admin.register(GalleryCategory)
class GalleryCategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'is_active']
    list_editable = ['is_active']
    prepopulated_fields = {'slug': ('name',)}

@admin.register(GalleryItem)
class GalleryItemAdmin(admin.ModelAdmin):
    list_display = ['title', 'category', 'media_type', 'order', 'is_active']
    list_filter = ['category', 'media_type', 'is_active']
    list_editable = ['order', 'is_active']
    search_fields = ['title']

@admin.register(ContactInfo)
class ContactInfoAdmin(admin.ModelAdmin):
    list_display = ['main_title', 'phone_number', 'email_address', 'is_active']
    list_editable = ['is_active']
    
    def has_add_permission(self, request):
        # Une seule instance d'informations de contact
        return not ContactInfo.objects.exists()

@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'status', 'created_at', 'ip_address']
    list_filter = ['status', 'created_at']
    list_editable = ['status']
    search_fields = ['name', 'email', 'message']
    readonly_fields = ['ip_address', 'user_agent', 'created_at', 'updated_at']
    
    fieldsets = (
        ('Message', {
            'fields': ('name', 'email', 'website', 'message')
        }),
        ('Métadonnées', {
            'fields': ('ip_address', 'user_agent')
        }),
        ('Statut', {
            'fields': ('status',)
        }),
        ('Dates', {
            'fields': ('created_at', 'updated_at')
        }),
    )


@admin.register(SiteSetting)
class SiteSettingAdmin(admin.ModelAdmin):
    list_display = ['site_name', 'contact_email', 'contact_phone']
    
    def has_add_permission(self, request):
        try:
            count = self.model.objects.count()
        except:
            return True
        return count == 0
    


#-------menu----------

@admin.register(NavigationItem)
class NavigationItemAdmin(admin.ModelAdmin):
    list_display = ['title', 'url', 'order', 'is_active', 'has_dropdown']
    list_editable = ['order', 'is_active']
    list_filter = ['is_active', 'has_dropdown']
    search_fields = ['title', 'url']
    
    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        form.base_fields['parent'].queryset = NavigationItem.objects.filter(has_dropdown=False)
        return form


@admin.register(SiteSettings)
class SiteSettingsAdmin(admin.ModelAdmin):
    def has_add_permission(self, request):
        return not SiteSettings.objects.exists()
    

from django.contrib import admin
from .models import PortfolioSection, PortfolioCategory, PortfolioItem

@admin.register(PortfolioSection)
class PortfolioSectionAdmin(admin.ModelAdmin):
    list_display = ['section_title', 'main_title', 'is_active']
    list_editable = ['is_active']
    
    def has_add_permission(self, request):
        # Une seule section portfolio
        return not PortfolioSection.objects.exists()

@admin.register(PortfolioCategory)
class PortfolioCategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'css_class', 'display_order', 'is_active', 'item_count']
    list_editable = ['display_order', 'is_active']
    prepopulated_fields = {'slug': ('name',)}
    
    def item_count(self, obj):
        return obj.items.count()
    item_count.short_description = "Nombre d'éléments"

@admin.register(PortfolioItem)
class PortfolioItemAdmin(admin.ModelAdmin):
    list_display = ['title', 'category', 'item_type', 'display_order', 'is_featured', 'is_active']
    list_filter = ['item_type', 'category', 'is_active', 'is_featured']
    list_editable = ['display_order', 'is_featured', 'is_active']
    search_fields = ['title']
    ordering = ['display_order', '-created_at']
    
    fieldsets = (
        ('Contenu', {
            'fields': ('title', 'category', 'item_type')
        }),
        ('Médias', {
            'fields': ('thumbnail', 'full_image', 'video_url', 'video_id')
        }),
        ('Options', {
            'fields': ('display_order', 'is_featured', 'is_active')
        }),
    )
from .models import Testimonial

@admin.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
    list_display = ['name', 'location', 'order', 'is_active']
    list_editable = ['order', 'is_active']
    list_filter = ['is_active']
    search_fields = ['name', 'location', 'content']
    ordering = ['order']
    
    fieldsets = (
        ('Client', {
            'fields': ('name', 'location')
        }),
        ('Témoignage', {
            'fields': ('content',)
        }),
        ('Photo', {
            'fields': ('photo', 'photo_filename')
        }),
        ('Options', {
            'fields': ('order', 'is_active')
        }),
    )


# website/admin.py
from django.contrib import admin
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _
from .models import Slider, SliderSettings, CallToAction

class CallToActionInline(admin.TabularInline):
    model = CallToAction
    extra = 1
    fields = ('text', 'link', 'button_color', 'vertical_offset', 'animation_delay', 'is_active')
    classes = ('collapse',)  # Optionnel : réduit par défaut

@admin.register(Slider)
class SliderAdmin(admin.ModelAdmin):
    # Liste principale
    list_display = ('title', 'display_order', 'is_active', 'transition', 'published_date_display')
    list_editable = ('display_order', 'is_active')
    list_filter = ('is_active', 'transition', 'published_date')
    search_fields = ('title', 'subtitle', 'description')
    list_per_page = 20
    
    # Formulaires - CHAMPS ÉDITABLES UNIQUEMENT
    fieldsets = (
        ('Contenu', {
            'fields': ('title', 'subtitle', 'description')
        }),
        ('Médias', {
            'fields': ('image', 'preview_image', 'thumbnail', 'video'),
            'classes': ('wide',),
        }),
        ('Configuration', {
            'fields': ('transition', 'display_duration', 'display_order', 'is_active'),
            'classes': ('collapse',),
        }),
        ('Bouton principal', {
            'fields': ('button_text', 'button_link'),
            'classes': ('collapse',),
        }),
    )
    
    # Champs en lecture seule
    readonly_fields = ('preview_image', 'created_at', 'updated_at', 'published_date_display')
    
    # CTAs intégrés
    inlines = [CallToActionInline]
    
    # Prévisualisation image
    def preview_image(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" style="max-height: 60px; border: 1px solid #ddd; border-radius: 4px;" />',
                obj.image.url
            )
        return format_html('<span style="color: #999;">Aucune image</span>')
    preview_image.short_description = 'Aperçu'
    
    # Date formatée
    def published_date_display(self, obj):
        if obj.published_date:
            return obj.published_date.strftime('%d/%m/%Y %H:%M')
        return "-"
    published_date_display.short_description = 'Publié le'
    
    # Ordonner par défaut
    ordering = ('-published_date', 'display_order')

@admin.register(CallToAction)
class CallToActionAdmin(admin.ModelAdmin):
    list_display = ('text', 'slide', 'button_color', 'is_active')
    list_filter = ('is_active',)
    search_fields = ('text', 'link')
    autocomplete_fields = ['slide']

@admin.register(SliderSettings)
class SliderSettingsAdmin(admin.ModelAdmin):
    def has_add_permission(self, request):
        return not SliderSettings.objects.exists()
    
    def has_delete_permission(self, request, obj=None):
        return False
    
    fieldsets = (
        ('Animation', {
            'fields': ('animation_speed', 'autoplay', 'autoplay_delay', 'loop')
        }),
        ('Interface', {
            'fields': ('show_navigation', 'show_bullets', 'show_timer', 'timer_color')
        }),
        ('Apparence', {
            'fields': ('mobile_breakpoint', 'overlay_opacity')
        }),
        ('Performance', {
            'fields': ('lazy_load', 'preload_images'),
            'classes': ('collapse',),
        }),
    )

# Titres admin
admin.site.site_header = 'Administration du Site'
admin.site.site_title = 'Admin'
admin.site.index_title = 'Tableau de bord'


# website/admin.py (ajoute à la fin)

from .models import ExpertiseSection, ExpertiseItem

class ExpertiseItemInline(admin.TabularInline):
    """Éléments d'accordéon dans la section savoir-faire"""
    model = ExpertiseItem
    extra = 1
    fields = ('title', 'content', 'accordion_id', 'is_expanded', 'display_order', 'is_active')
    ordering = ('display_order',)
    
    def formfield_for_dbfield(self, db_field, **kwargs):
        """Aide à la saisie pour l'ID accordéon"""
        if db_field.name == 'accordion_id':
            kwargs['help_text'] = 'Ex: collapseOne, collapseTwo, collapseThree'
        return super().formfield_for_dbfield(db_field, **kwargs)

@admin.register(ExpertiseSection)
class ExpertiseSectionAdmin(admin.ModelAdmin):
    """Admin pour la section Savoir-faire"""
    
    list_display = ('get_section_title_display', 'main_title_preview', 'is_active', 'display_order', 'item_count')
    list_editable = ('is_active', 'display_order')
    list_filter = ('is_active', 'section_title')
    search_fields = ('main_title', 'description')
    
    fieldsets = (
        ('Contenu', {
            'fields': ('section_title', 'main_title', 'description', 'image')
        }),
        ('Configuration', {
            'fields': ('is_active', 'display_order'),
            'classes': ('collapse',)
        }),
    )
    
    readonly_fields = ('created_at', 'updated_at')
    inlines = [ExpertiseItemInline]
    
    def main_title_preview(self, obj):
        """Aperçu du titre principal sans HTML"""
        return obj.main_title.replace('<br>', ' ')
    main_title_preview.short_description = 'Titre principal'
    
    def item_count(self, obj):
        return obj.items.count()
    item_count.short_description = 'Nombre d\'éléments'

@admin.register(ExpertiseItem)
class ExpertiseItemAdmin(admin.ModelAdmin):
    """Admin séparé pour les éléments d'accordéon"""
    
    list_display = ('title', 'expertise_section', 'accordion_id', 'is_expanded', 'is_active')
    list_filter = ('is_active', 'is_expanded', 'expertise_section')
    list_editable = ('is_active', 'is_expanded')
    search_fields = ('title', 'content')
    autocomplete_fields = ['expertise_section']
    
    fieldsets = (
        ('Contenu', {
            'fields': ('expertise_section', 'title', 'content')
        }),
        ('Configuration accordéon', {
            'fields': ('accordion_id', 'is_expanded', 'display_order')
        }),
        ('Activation', {
            'fields': ('is_active',)
        }),
    )

from .models import TeamMember, TeamSection
class TeamMemberAdminForm(forms.ModelForm):
    """Formulaire personnalisé pour les réseaux sociaux"""
    class Meta:
        model = TeamMember
        fields = '__all__'
        widgets = {
            'social_media': forms.Textarea(attrs={
                'rows': 3,
                'placeholder': '{"twitter": "https://twitter.com/username",\n"linkedin": "https://linkedin.com/in/username",\n"facebook": "https://facebook.com/username"}'
            }),
        }

@admin.register(TeamMember)
class TeamMemberAdmin(admin.ModelAdmin):
    """Admin pour les membres d'équipe"""
    
    form = TeamMemberAdminForm
    
    list_display = ('name', 'position', 'is_active', 'display_order', 'social_count')
    list_editable = ('display_order', 'is_active')
    list_filter = ('is_active', 'position')
    search_fields = ('name', 'position', 'bio')
    
    fieldsets = (
        ('Informations personnelles', {
            'fields': ('name', 'position', 'image', 'bio')
        }),
        ('Réseaux sociaux', {
            'fields': ('social_media',),
            'description': 'Format JSON: {"plateforme": "url"}'
        }),
        ('Configuration', {
            'fields': ('is_active', 'display_order')
        }),
    )
    
    readonly_fields = ('created_at', 'updated_at')
    
    def social_count(self, obj):
        return len([v for v in obj.social_media.values() if v])
    social_count.short_description = 'Réseaux'

@admin.register(TeamSection)
class TeamSectionAdmin(admin.ModelAdmin):
    """Admin pour la section Équipe"""
    
    list_display = ('main_title', 'section_title', 'is_active', 'display_order', 'member_count')
    list_editable = ('is_active', 'display_order')
    list_filter = ('is_active',)
    search_fields = ('main_title', 'section_title', 'description')
    
    fieldsets = (
        ('Contenu', {
            'fields': ('section_title', 'main_title', 'description')
        }),
        ('Membres', {
            'fields': ('members',),
            'description': 'Sélectionnez les membres à afficher dans cette section'
        }),
        ('Apparence', {
            'fields': ('background_color',)
        }),
        ('Configuration', {
            'fields': ('is_active', 'display_order')
        }),
    )
    
    filter_horizontal = ('members',)  # Interface plus pratique pour sélection multiple
    readonly_fields = ('created_at', 'updated_at')
    
    def member_count(self, obj):
        return obj.members.count()
    member_count.short_description = 'Membres'


from django.utils.html import format_html
from .models import Client

@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ('name', 'type', 'logo_preview', 'order', 'is_active', 'year')
    list_editable = ('order', 'is_active')
    list_filter = ('type', 'is_active')
    search_fields = ('name', 'description')
    
    fieldsets = (
        ('Informations', {
            'fields': ('name', 'type', 'year', 'description', 'url')
        }),
        ('Image', {
            'fields': ('logo', 'logo_preview')
        }),
        ('Paramètres', {
            'fields': ('order', 'is_active')
        }),
    )
    
    readonly_fields = ('logo_preview',)
    
    def logo_preview(self, obj):
        if obj.logo:
            return format_html('<img src="{}" style="max-width: 100px; max-height: 50px;" />', obj.logo.url)
        return "Aucun logo"
    logo_preview.short_description = "Aperçu"

from django.utils.html import format_html
from .models import VideoSection

@admin.register(VideoSection)
class VideoSectionAdmin(admin.ModelAdmin):
    list_display = ('video_url', 'is_active', 'order')
    list_editable = ('is_active', 'order')
    
    fieldsets = (
        ('Configuration Vidéo', {
            'fields': ('video_url', 'play_icon', 'button_text')
        }),
        ('Arrière-plan', {
            'fields': ('background_image', 'background_color'),
            'description': 'Choisissez une image ou une couleur de fond'
        }),
        ('Paramètres', {
            'fields': ('is_active', 'order')
        }),
    )
    
    def has_add_permission(self, request):
        """Limite à une seule instance"""
        if VideoSection.objects.count() >= 1:
            return False
        return super().has_add_permission(request)
    
from django.contrib import admin
from .models import ConnectSection

@admin.register(ConnectSection)
class ConnectSectionAdmin(admin.ModelAdmin):  # Nom différent
    list_display = ('main_title', 'section_title', 'button_text', 'is_active', 'display_order')
    list_editable = ('is_active', 'display_order')
    list_filter = ('is_active',)
    search_fields = ('main_title', 'section_title', 'subtitle')
    
    fieldsets = (
        ('Contenu', {
            'fields': ('section_title', 'main_title', 'subtitle')
        }),
        ('Bouton', {
            'fields': ('button_text', 'button_url')
        }),
        ('Style', {
            'fields': ('background_color',),
            'classes': ('collapse',)
        }),
        ('Paramètres', {
            'fields': ('is_active', 'display_order')
        }),
    )


from django.utils.html import format_html
from .models import JewelryCollection, CollectionFeature, CollectionFAQ

class CollectionFeatureInline(admin.TabularInline):
    model = CollectionFeature
    extra = 1

class CollectionFAQInline(admin.TabularInline):
    model = CollectionFAQ
    extra = 1

@admin.register(JewelryCollection)
class JewelryCollectionAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'material', 'is_active', 'is_featured', 'order', 'image_preview')
    list_editable = ('order', 'is_active', 'is_featured')
    list_filter = ('category', 'is_active', 'is_featured')
    search_fields = ('name', 'short_description', 'long_description')
    prepopulated_fields = {'slug': ('name',)}
    
    inlines = [CollectionFeatureInline, CollectionFAQInline]
    
    fieldsets = (
        ('Informations de base', {
            'fields': ('name', 'slug', 'category', 'is_active', 'is_featured', 'order')
        }),
        ('Description', {
            'fields': ('short_description', 'long_description', 'fabrication_process')
        }),
        ('Images', {
            'fields': ('main_image', 'featured_image', 'image_preview')
        }),
        ('Caractéristiques techniques', {
            'fields': ('material', 'purity', 'delivery_time', 'custom_order_time')
        }),
    )
    
    readonly_fields = ('image_preview',)
    
    def image_preview(self, obj):
        if obj.featured_image:
            return format_html('<img src="{}" style="max-width: 100px; max-height: 75px;" />', obj.featured_image.url)
        return "Aucune image"
    image_preview.short_description = "Aperçu"

from django.contrib import admin
from django.utils.html import format_html
from django.utils.safestring import mark_safe
from .models import BlogBanner

@admin.register(BlogBanner)
class BlogBannerAdmin(admin.ModelAdmin):
    """Configuration de l'admin pour BlogBanner"""
    
    # Configuration de la liste
    list_display = ('title_preview', 'category', 'author', 'page', 'published_date', 
                    'is_active', 'display_order', 'image_thumbnail')
    list_display_links = ('title_preview',)
    list_editable = ('is_active', 'display_order', 'category')
    list_filter = ('category', 'is_active', 'page', 'published_date')
    search_fields = ('title', 'category', 'author', 'page')
    ordering = ('display_order', '-published_date')
    actions = ['activate_selected', 'deactivate_selected']
    
    # Pagination
    list_per_page = 20
    
    # Méthodes d'affichage
    def title_preview(self, obj):
        """Aperçu du titre (limité à 60 caractères)"""
        return obj.short_title() if hasattr(obj, 'short_title') else (obj.title[:60] + '...' if len(obj.title) > 60 else obj.title)
    title_preview.short_description = "Titre"
    title_preview.admin_order_field = 'title'
    
    def image_thumbnail(self, obj):
        """Miniature de l'image dans la liste"""
        if obj.background_image:
            return format_html(
                '<img src="{}" style="width: 80px; height: 40px; object-fit: cover; border-radius: 4px;" />',
                obj.background_image.url
            )
        return format_html(
            '<div style="width: 80px; height: 40px; background-color: {}; border-radius: 4px;"></div>',
            obj.background_color
        )
    image_thumbnail.short_description = "Image"
    
    def background_preview(self, obj):
        """Grande prévisualisation dans le formulaire d'édition"""
        if obj.background_image:
            return format_html(
                '''
                <div style="margin: 10px 0; padding: 10px; background: #f8f9fa; border-radius: 8px;">
                    <h4>Aperçu actuel:</h4>
                    <img src="{}" style="max-width: 100%; height: auto; max-height: 300px; border-radius: 4px; border: 1px solid #ddd;" />
                    <p style="margin-top: 10px; color: #666; font-size: 12px;">
                        Taille: {} × {} px<br>
                        Format: {}
                    </p>
                </div>
                ''',
                obj.background_image.url,
                obj.background_image.width if hasattr(obj.background_image, 'width') else '?',
                obj.background_image.height if hasattr(obj.background_image, 'height') else '?',
                obj.background_image.name.split('.')[-1].upper() if obj.background_image.name else '?'
            )
        return format_html(
            '''
            <div style="margin: 10px 0; padding: 10px; background: #f8f9fa; border-radius: 8px;">
                <h4>Couleur de fond actuelle:</h4>
                <div style="width: 100%; height: 100px; background-color: {}; border-radius: 4px; border: 1px solid #ddd;"></div>
                <p style="margin-top: 10px; color: #666;">Code: {}</p>
            </div>
            ''',
            obj.background_color,
            obj.background_color
        )
    background_preview.short_description = "Aperçu du fond"
    
    # Configuration des champs du formulaire
    fieldsets = (
        ('Identification', {
            'fields': ('page', 'category', 'display_order', 'is_active'),
            'classes': ('collapse', 'wide'),
            'description': 'Configuration de base de la bannière'
        }),
        ('Contenu', {
            'fields': ('title', 'article_url', 'author'),
            'description': 'Contenu textuel de la bannière'
        }),
        ('Statistiques', {
            'fields': ('published_date', 'comment_count', 'view_count'),
            'classes': ('collapse',),
            'description': 'Informations de publication et statistiques'
        }),
        ('Apparence', {
            'fields': ('background_image', 'background_color', 'background_preview'),
            'description': 'Configuration de l\'apparence de la bannière'
        }),
    )
    
    readonly_fields = ('background_preview', 'created_at', 'updated_at')
    
    # Configuration pour le formulaire d'ajout
    add_fieldsets = (
        (None, {
            'fields': ('page', 'category', 'title', 'is_active')
        }),
        ('Contenu', {
            'fields': ('author', 'article_url'),
            'classes': ('collapse',)
        }),
        ('Apparence', {
            'fields': ('background_image', 'background_color'),
            'classes': ('collapse',)
        }),
    )
    
    # Personnalisation du formulaire selon le mode
    def get_fieldsets(self, request, obj=None):
        if not obj:  # Mode ajout
            return self.add_fieldsets
        return super().get_fieldsets(request, obj)
    
    # Champs en lecture seule pour l'édition
    def get_readonly_fields(self, request, obj=None):
        readonly_fields = list(super().get_readonly_fields(request, obj))
        if obj:  # En mode édition
            readonly_fields.extend(['created_at', 'updated_at'])
        return readonly_fields
    
    # Pré-remplissage pour l'ajout
    def get_changeform_initial_data(self, request):
        initial = super().get_changeform_initial_data(request)
        initial['author'] = 'John'
        initial['comment_count'] = 0
        initial['view_count'] = 0
        initial['background_color'] = '#1a1a1a'
        return initial
    
    # Actions personnalisées
    def activate_selected(self, request, queryset):
        """Activer les bannières sélectionnées"""
        updated = queryset.update(is_active=True)
        self.message_user(request, f"{updated} bannière(s) activée(s).")
    activate_selected.short_description = "Activer la sélection"
    
    def deactivate_selected(self, request, queryset):
        """Désactiver les bannières sélectionnées"""
        updated = queryset.update(is_active=False)
        self.message_user(request, f"{updated} bannière(s) désactivée(s).")
    deactivate_selected.short_description = "Désactiver la sélection"
    
    # Configuration avancée
    save_on_top = True  # Boutons en haut aussi
    save_as = True  # Permet de sauvegarder comme nouvelle copie
    save_as_continue = True  # Continue l'édition après "sauvegarder comme"
    
    # Filtres horizontaux/verticaux
    filter_horizontal = ()
    filter_vertical = ()
    
    # Champs pour la recherche rapide
    autocomplete_fields = []
    
    # Configuration des onglets (si vous avez beaucoup de champs)
    def get_fieldsets_with_tabs(self, request, obj=None):
        """Version alternative avec onglets"""
        return [
            ('Général', {
                'fields': ['page', 'category', 'title', 'is_active']
            }),
            ('Contenu', {
                'fields': ['author', 'article_url', 'published_date']
            }),
            ('Statistiques', {
                'fields': ['comment_count', 'view_count']
            }),
            ('Apparence', {
                'fields': ['background_image', 'background_color', 'background_preview']
            }),
        ]
    
    # Personnalisation des messages
    def message_user(self, request, message, level='INFO', extra_tags='', fail_silently=False):
        """Personnaliser les messages à l'utilisateur"""
        from django.contrib import messages
        if level == 'INFO':
            messages.success(request, message)
        elif level == 'WARNING':
            messages.warning(request, message)
        elif level == 'ERROR':
            messages.error(request, message)
        else:
            messages.info(request, message)

# Optionnel : Inscription d'actions globales
@admin.action(description="Réinitialiser les vues à zéro")
def reset_views(modeladmin, request, queryset):
    """Réinitialise le compteur de vues"""
    queryset.update(view_count=0)
    modeladmin.message_user(request, f"Vues réinitialisées pour {queryset.count()} bannière(s).")

# Ajout de l'action au modèle
BlogBannerAdmin.actions.append(reset_views)

from .models import (
    ArticleBlog, AuteurArticle, CategorieArticle, MotCleArticle,
    CommentaireArticle, SidebarBlog, ImageGalerieSidebar,
    ArticlePopulaire, RechercheBlog
)

class ImageGalerieSidebarInline(admin.TabularInline):
    model = ImageGalerieSidebar
    extra = 1

@admin.register(SidebarBlog)
class SidebarBlogAdmin(admin.ModelAdmin):
    list_display = ('titre', 'type_section', 'est_actif', 'ordre')
    list_editable = ('ordre', 'est_actif')
    list_filter = ('type_section', 'est_actif')
    inlines = [ImageGalerieSidebarInline]
    
    fieldsets = (
        ('Configuration', {
            'fields': ('type_section', 'titre', 'contenu', 'est_actif', 'ordre')
        }),
    )

class CommentaireArticleInline(admin.TabularInline):
    model = CommentaireArticle
    extra = 0
    readonly_fields = ('nom', 'email', 'contenu', 'date_creation')
    can_delete = False

@admin.register(ArticleBlog)
class ArticleBlogAdmin(admin.ModelAdmin):
    list_display = ('titre', 'categorie', 'auteur', 'date_publication', 'est_publie', 'nombre_vues')
    list_editable = ('est_publie',)
    list_filter = ('categorie', 'est_publie', 'date_publication')
    search_fields = ('titre', 'contenu', 'resume')
    prepopulated_fields = {'slug': ('titre',)}
    filter_horizontal = ('mots_cles',)
    
    fieldsets = (
        ('Contenu', {
            'fields': ('titre', 'slug', 'resume', 'contenu', 'citation')
        }),
        ('Images', {
            'fields': ('image_principale', 'image_galerie_1', 'image_galerie_2')
        }),
        ('Métadonnées', {
            'fields': ('auteur', 'categorie', 'mots_cles', 'date_publication')
        }),
        ('Réseaux sociaux', {
            'fields': ('url_facebook', 'url_twitter', 'url_linkedin'),
            'classes': ('collapse',)
        }),
        ('Statistiques', {
            'fields': ('est_publie', 'est_en_vedette', 'nombre_vues'),
            'classes': ('collapse',)
        }),
    )
    
    inlines = [CommentaireArticleInline]

@admin.register(AuteurArticle)
class AuteurArticleAdmin(admin.ModelAdmin):
    list_display = ('nom',)

@admin.register(CategorieArticle)
class CategorieArticleAdmin(admin.ModelAdmin):
    list_display = ('nom', 'ordre', 'nombre_articles')
    list_editable = ('ordre',)
    prepopulated_fields = {'slug': ('nom',)}

@admin.register(MotCleArticle)
class MotCleArticleAdmin(admin.ModelAdmin):
    list_display = ('nom',)
    prepopulated_fields = {'slug': ('nom',)}

@admin.register(CommentaireArticle)
class CommentaireArticleAdmin(admin.ModelAdmin):
    list_display = ('nom', 'article', 'date_creation', 'est_approuve')
    list_filter = ('est_approuve', 'date_creation')
    search_fields = ('nom', 'email', 'contenu')
    list_editable = ('est_approuve',)

@admin.register(ArticlePopulaire)
class ArticlePopulaireAdmin(admin.ModelAdmin):
    list_display = ('article', 'clics')
    readonly_fields = ('clics',)

@admin.register(RechercheBlog)
class RechercheBlogAdmin(admin.ModelAdmin):
    list_display = ('requete', 'adresse_ip', 'date_creation')
    readonly_fields = ('date_creation',)
    list_filter = ('date_creation',)

from .models import ArticleDetail, CategorieSidebar, ArticleSidebar, PhotoGalerie, CommentaireDetail

class CommentaireDetailInline(admin.TabularInline):
    model = CommentaireDetail
    extra = 0
    readonly_fields = ('nom', 'contenu', 'date_creation')
    can_delete = False

@admin.register(ArticleDetail)
class ArticleDetailAdmin(admin.ModelAdmin):
    list_display = ('titre', 'nom_auteur', 'date_publication', 'est_actif')
    list_editable = ('est_actif',)
    search_fields = ('titre', 'contenu_principal')
    prepopulated_fields = {'slug': ('titre',)}
    
    fieldsets = (
        ('Contenu principal', {
            'fields': ('titre', 'slug', 'contenu_principal', 'citation')
        }),
        ('Images', {
            'fields': ('image_principale', 'image_secondaire')
        }),
        ('Auteur', {
            'fields': ('nom_auteur', 'photo_auteur')
        }),
        ('Tags', {
            'fields': ('tag_1', 'tag_2', 'tag_3'),
            'classes': ('collapse',)
        }),
        ('Liste à puces', {
            'fields': ('element_liste_1', 'element_liste_2', 'element_liste_3', 
                      'element_liste_4', 'element_liste_5'),
            'classes': ('collapse',)
        }),
        ('Réseaux sociaux', {
            'fields': ('lien_facebook', 'lien_twitter', 'lien_linkedin'),
            'classes': ('collapse',)
        }),
        ('Paramètres', {
            'fields': ('date_publication', 'est_actif')
        }),
    )
    
    inlines = [CommentaireDetailInline]

@admin.register(CategorieSidebar)
class CategorieSidebarAdmin(admin.ModelAdmin):
    list_display = ('nom', 'nombre_articles', 'ordre')
    list_editable = ('ordre', 'nombre_articles')

@admin.register(ArticleSidebar)
class ArticleSidebarAdmin(admin.ModelAdmin):
    list_display = ('titre', 'type_article', 'date_publication', 'ordre')
    list_editable = ('ordre', 'type_article')
    list_filter = ('type_article',)

@admin.register(PhotoGalerie)
class PhotoGalerieAdmin(admin.ModelAdmin):
    list_display = ('titre', 'ordre', 'image_preview')
    list_editable = ('ordre',)
    
    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="max-width: 50px; max-height: 50px;" />', obj.image.url)
        return "Aucune image"
    image_preview.short_description = "Aperçu"

@admin.register(CommentaireDetail)
class CommentaireDetailAdmin(admin.ModelAdmin):
    list_display = ('nom', 'article', 'date_creation', 'est_approuve')
    list_editable = ('est_approuve',)
    list_filter = ('est_approuve', 'date_creation')


from .models import ArticleCentre, CommentaireCentre

class CommentaireCentreInline(admin.TabularInline):
    model = CommentaireCentre
    extra = 0
    fields = ('nom', 'email', 'message', 'date_creation', 'approuve')
    readonly_fields = ('date_creation',)

@admin.register(ArticleCentre)
class ArticleCentreAdmin(admin.ModelAdmin):
    list_display = ('titre', 'nom_auteur', 'date_publication', 'est_actif', 'image_miniature')
    list_editable = ('est_actif',)
    list_filter = ('est_actif', 'date_publication')
    search_fields = ('titre', 'contenu_principal', 'nom_auteur')
    
    fieldsets = (
        ('Informations de base', {
            'fields': ('titre', 'est_actif')
        }),
        ('Contenu', {
            'fields': ('description_courte', 'contenu_principal', 'citation', 'sous_titre', 'texte_sous_titre')
        }),
        ('Images', {
            'fields': ('image_principale', 'image_gauche')
        }),
        ('Auteur', {
            'fields': ('nom_auteur', 'photo_auteur', 'bio_auteur')
        }),
        ('Tags', {
            'fields': ('tag_1', 'tag_2', 'tag_3')
        }),
        ('Réseaux sociaux', {
            'fields': ('facebook_auteur', 'twitter_auteur', 'linkedin_auteur'),
            'classes': ('collapse',)
        }),
        ('Dates', {
            'fields': ('date_publication',)
        }),
    )
    
    inlines = [CommentaireCentreInline]
    
    def image_miniature(self, obj):
        if obj.image_principale:
            return format_html('<img src="{}" width="50" height="30" />', obj.image_principale.url)
        return "Pas d'image"
    image_miniature.short_description = "Image"

@admin.register(CommentaireCentre)
class CommentaireCentreAdmin(admin.ModelAdmin):
    list_display = ('nom', 'article', 'date_creation', 'approuve')
    list_editable = ('approuve',)
    list_filter = ('approuve', 'date_creation')
    search_fields = ('nom', 'email', 'message')

from .models import FooterInfo, LienFooter

class LienFooterInline(admin.TabularInline):
    model = LienFooter
    extra = 1
    fields = ('type_lien', 'texte', 'url', 'ordre')

@admin.register(FooterInfo)
class FooterInfoAdmin(admin.ModelAdmin):
    list_display = ('nom_entreprise', 'email', 'telephone', 'est_actif')
    list_editable = ('est_actif',)
    
    # Empêcher d'ajouter plusieurs instances
    def has_add_permission(self, request):
        return not FooterInfo.objects.exists()
    
    inlines = [LienFooterInline]
    
    fieldsets = (
        ('Informations générales', {
            'fields': ('nom_entreprise', 'description', 'est_actif')
        }),
        ('Réseaux sociaux', {
            'fields': ('instagram', 'facebook', 'pinterest', 'tiktok')
        }),
        ('Contact', {
            'fields': ('adresse', 'email', 'telephone')
        }),
        ('Copyright', {
            'fields': ('copyright_texte',)
        }),
    )

# Enregistre LienFooter séparément
@admin.register(LienFooter)
class LienFooterAdmin(admin.ModelAdmin):
    list_display = ('texte', 'type_lien', 'url', 'ordre', 'footer')
    list_editable = ('ordre', 'url', 'type_lien')
    list_filter = ('type_lien',)
    
    def save_model(self, request, obj, form, change):
        # Si pas de footer associé, associe au footer principal
        if not obj.footer:
            footer_principal = FooterInfo.load()
            obj.footer = footer_principal
        super().save_model(request, obj, form, change)