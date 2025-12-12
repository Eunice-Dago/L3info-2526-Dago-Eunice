# website/admin.py
from django.contrib import admin
from django import forms
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _

# Importation de tous vos modèles
from .models import* 

# ============================================
# MODÈLES PRINCIPAUX
# ============================================

@admin.register(Banner)
class BannerAdmin(admin.ModelAdmin):
    list_display = ['page', 'title']
    list_filter = ['page']
    search_fields = ['title']


# Admin pour la page About
class ServiceAboutInline(admin.TabularInline):
    model = ServiceAbout
    extra = 3


@admin.register(About)
class AboutAdmin(admin.ModelAdmin):
    inlines = [ServiceAboutInline]
    list_display = ['about_title', 'section_title']


# Admin pour les collections
class CollectionItemInline(admin.TabularInline):
    model = CollectionItem
    extra = 6
    ordering = ['display_order']


@admin.register(Collection)
class CollectionAdmin(admin.ModelAdmin):
    inlines = [CollectionItemInline]
    list_display = ['main_title', 'section_title']
    
    def has_add_permission(self, request):
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
        return not CTA.objects.exists()


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ['title', 'order', 'is_active']
    list_editable = ['order', 'is_active']
    list_filter = ['is_active']
    search_fields = ['title', 'description']
    ordering = ['order']
    
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


@admin.register(PricingPlan)
class PricingPlanAdmin(admin.ModelAdmin):
    list_display = ('title', 'plan_type', 'price', 'period', 'order', 'is_active')
    list_editable = ('order', 'is_active')
    list_filter = ('plan_type', 'is_active')
    search_fields = ('title', 'description')
    
    fieldsets = (
        ('Informations de base', {
            'fields': ('plan_type', 'title', 'price', 'period', 'description', 'order', 'is_active')
        }),
        ('Caractéristiques', {
            'fields': ('feature1', 'feature2', 'feature3', 'feature4', 'feature5', 'feature6')
        }),
        ('Bouton', {
            'fields': ('button_text', 'button_url')
        }),
    )


# ============================================
# MODÈLES BLOG
# ============================================

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'category', 'created_at', 'published', 'views']
    list_filter = ['published', 'category', 'created_at']
    search_fields = ['title', 'content']
    prepopulated_fields = {'slug': ('title',)}


@admin.register(BlogCategory)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'post_count']
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['author_name', 'post', 'created_at', 'approved']
    list_filter = ['approved', 'created_at']
    list_editable = ['approved']
    search_fields = ['author_name', 'content']


@admin.register(SidebarContent)
class SidebarContentAdmin(admin.ModelAdmin):
    list_display = ['title', 'content_type', 'display_order', 'is_active']
    list_editable = ['display_order', 'is_active']
    list_filter = ['content_type', 'is_active']


@admin.register(GalleryImage)
class GalleryImageAdmin(admin.ModelAdmin):
    list_display = ['title', 'uploaded_at']
    search_fields = ['title']


# ============================================
# MODÈLES CONTACT
# ============================================

@admin.register(ContactInfo)
class ContactInfoAdmin(admin.ModelAdmin):
    list_display = ['main_title', 'phone_number', 'email_address', 'is_active']
    list_editable = ['is_active']
    
    def has_add_permission(self, request):
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
            return not SiteSetting.objects.exists()
        except:
            return True


# ============================================
# MODÈLES MENU
# ============================================

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


# ============================================
# MODÈLES PORTFOLIO
# ============================================

@admin.register(PortfolioSection)
class PortfolioSectionAdmin(admin.ModelAdmin):
    list_display = ['section_title', 'main_title', 'is_active']
    list_editable = ['is_active']
    
    def has_add_permission(self, request):
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


# ============================================
# MODÈLES TÉMOIGNAGES
# ============================================

admin.site.register(Testimonial)


admin.site.register(Testimonial1)

admin.site.register(Test)





# ============================================
# MODÈLES SLIDER
# ============================================

class CallToActionInline(admin.TabularInline):
    model = CallToAction
    extra = 1
    fields = ('text', 'link', 'button_color', 'vertical_offset', 'animation_delay', 'is_active')


@admin.register(Slider)
class SliderAdmin(admin.ModelAdmin):
    list_display = ('title', 'display_order', 'is_active', 'transition', 'published_date_display')
    list_editable = ('display_order', 'is_active')
    list_filter = ('is_active', 'transition', 'published_date')
    search_fields = ('title', 'subtitle', 'description')
    list_per_page = 20
    
    fieldsets = (
        ('Contenu', {
            'fields': ('title', 'subtitle', 'description')
        }),
        ('Médias', {
            'fields': ('image', 'preview_image', 'thumbnail', 'video')
        }),
        ('Configuration', {
            'fields': ('transition', 'display_duration', 'display_order', 'is_active')
        }),
        ('Bouton principal', {
            'fields': ('button_text', 'button_link')
        }),
    )
    
    readonly_fields = ('preview_image', 'created_at', 'updated_at', 'published_date_display')
    inlines = [CallToActionInline]
    
    def preview_image(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" style="max-height: 60px;" />',
                obj.image.url
            )
        return format_html('<span style="color: #999;">Aucune image</span>')
    preview_image.short_description = 'Aperçu'
    
    def published_date_display(self, obj):
        if obj.published_date:
            return obj.published_date.strftime('%d/%m/%Y %H:%M')
        return "-"
    published_date_display.short_description = 'Publié le'
    
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
            'fields': ('lazy_load', 'preload_images')
        }),
    )


# ============================================
# MODÈLES EXPERTISE
# ============================================

class ExpertiseItemInline(admin.TabularInline):
    model = ExpertiseItem
    extra = 1
    fields = ('title', 'content', 'accordion_id', 'is_expanded', 'display_order', 'is_active')
    ordering = ('display_order',)


@admin.register(ExpertiseSection)
class ExpertiseSectionAdmin(admin.ModelAdmin):
    list_display = ('get_section_title_display', 'main_title_preview', 'is_active', 'display_order', 'item_count')
    list_editable = ('is_active', 'display_order')
    list_filter = ('is_active', 'section_title')
    search_fields = ('main_title', 'description')
    
    fieldsets = (
        ('Contenu', {
            'fields': ('section_title', 'main_title', 'description', 'image')
        }),
        ('Configuration', {
            'fields': ('is_active', 'display_order')
        }),
    )
    
    readonly_fields = ('created_at', 'updated_at')
    inlines = [ExpertiseItemInline]
    
    def main_title_preview(self, obj):
        return obj.main_title.replace('<br>', ' ')
    main_title_preview.short_description = 'Titre principal'
    
    def item_count(self, obj):
        return obj.items.count()
    item_count.short_description = 'Nombre d\'éléments'


@admin.register(ExpertiseItem)
class ExpertiseItemAdmin(admin.ModelAdmin):
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


# ============================================
# MODÈLES ÉQUIPE
# ============================================

class TeamMemberAdminForm(forms.ModelForm):
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
            'fields': ('social_media',)
        }),
        ('Configuration', {
            'fields': ('is_active', 'display_order')
        }),
    )
    
    readonly_fields = ('created_at', 'updated_at')
    
    def social_count(self, obj):
        if obj.social_media:
            return len([v for v in obj.social_media.values() if v])
        return 0
    social_count.short_description = 'Réseaux'


@admin.register(TeamSection)
class TeamSectionAdmin(admin.ModelAdmin):
    list_display = ('main_title', 'section_title', 'is_active', 'display_order', 'member_count')
    list_editable = ('is_active', 'display_order')
    list_filter = ('is_active',)
    search_fields = ('main_title', 'section_title', 'description')
    
    fieldsets = (
        ('Contenu', {
            'fields': ('section_title', 'main_title', 'description')
        }),
        ('Membres', {
            'fields': ('members',)
        }),
        ('Apparence', {
            'fields': ('background_color',)
        }),
        ('Configuration', {
            'fields': ('is_active', 'display_order')
        }),
    )
    
    filter_horizontal = ('members',)
    readonly_fields = ('created_at', 'updated_at')
    
    def member_count(self, obj):
        return obj.members.count()
    member_count.short_description = 'Membres'


# ============================================
# AUTRES MODÈLES
# ============================================

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


@admin.register(VideoSection)
class VideoSectionAdmin(admin.ModelAdmin):
    list_display = ('video_url', 'is_active', 'order')
    list_editable = ('is_active', 'order')
    
    fieldsets = (
        ('Configuration Vidéo', {
            'fields': ('video_url', 'play_icon', 'button_text')
        }),
        ('Arrière-plan', {
            'fields': ('background_image', 'background_color')
        }),
        ('Paramètres', {
            'fields': ('is_active', 'order')
        }),
    )
    
    def has_add_permission(self, request):
        if VideoSection.objects.count() >= 1:
            return False
        return super().has_add_permission(request)


@admin.register(ConnectSection)
class ConnectSectionAdmin(admin.ModelAdmin):
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
            'fields': ('background_color',)
        }),
        ('Paramètres', {
            'fields': ('is_active', 'display_order')
        }),
    )


# ============================================
# MODÈLES COLLECTION JOAILLERIE
# ============================================

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


# ============================================
# MODÈLES BLOG FRANÇAIS
# ============================================

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
            'fields': ('url_facebook', 'url_twitter', 'url_linkedin')
        }),
        ('Statistiques', {
            'fields': ('est_publie', 'est_en_vedette', 'nombre_vues')
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


# ============================================
# MODÈLES DÉTAILS ARTICLES
# ============================================

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
            'fields': ('tag_1', 'tag_2', 'tag_3')
        }),
        ('Liste à puces', {
            'fields': ('element_liste_1', 'element_liste_2', 'element_liste_3', 
                      'element_liste_4', 'element_liste_5')
        }),
        ('Réseaux sociaux', {
            'fields': ('lien_facebook', 'lien_twitter', 'lien_linkedin')
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


# ============================================
# MODÈLES ARTICLES CENTRE
# ============================================

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
            'fields': ('facebook_auteur', 'twitter_auteur', 'linkedin_auteur')
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


# ============================================
# MODÈLES FOOTER
# ============================================

class LienFooterInline(admin.TabularInline):
    model = LienFooter
    extra = 1
    fields = ('type_lien', 'texte', 'url', 'ordre')


@admin.register(FooterInfo)
class FooterInfoAdmin(admin.ModelAdmin):
    list_display = ('nom_entreprise', 'email', 'telephone', 'est_actif')
    list_editable = ('est_actif',)
    
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


@admin.register(LienFooter)
class LienFooterAdmin(admin.ModelAdmin):
    list_display = ('texte', 'type_lien', 'url', 'ordre', 'footer')
    list_editable = ('ordre', 'url', 'type_lien')
    list_filter = ('type_lien',)
    
    def save_model(self, request, obj, form, change):
        if not obj.footer:
            footer_principal = FooterInfo.load()
            obj.footer = footer_principal
        super().save_model(request, obj, form, change)


# ============================================
# CONFIGURATION GLOBALE ADMIN
# ============================================

# Enregistrement des modèles simples qui n'ont pas besoin de configuration spéciale
simple_models = [
    ServiceAbout, GalleryCategory, GalleryItem,
    BlogBanner  # Ajout de BlogBanner
]

for model in simple_models:
    admin.site.register(model)

# Configuration de l'interface admin
admin.site.site_header = 'Administration du Site'
admin.site.site_title = 'Admin'
admin.site.index_title = 'Tableau de bord'