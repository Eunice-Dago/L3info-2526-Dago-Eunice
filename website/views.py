# tp3/website/views.py
from django.shortcuts import render
from .models import *
from django.shortcuts import redirect

def index(request):
    about_instance = About.objects.first()
    collection = Collection.objects.first()
    cta = CTA.objects.filter(is_active=True).first()
    services = Service.objects.filter(is_active=True).order_by('order')[:3]
    testimonials = Testimonial.objects.filter(is_active=True).order_by('order')[:3]
    slides = Slider.objects.filter(is_active=True).order_by('display_order')
    settings = SliderSettings.get_settings()
    expertise = ExpertiseSection.objects.filter(is_active=True).order_by('display_order').first()
    team_section = TeamSection.objects.filter(is_active=True).order_by('display_order').first()
    pricing_plans = PricingPlan.objects.filter(is_active=True).order_by('order')
    blog_posts = BlogPost.objects.filter(is_published=True).order_by('-published_date')[:3]
    clients = Client.objects.filter(is_active=True).order_by('order')
    video_section = VideoSection.objects.filter(is_active=True).first()
    photos_galerie = PhotoGalerie.objects.all().order_by('ordre')[:9]
    portfolio = PortfolioSection.objects.filter(is_active=True).first()


 

    if not portfolio:
        portfolio = PortfolioSection.objects.create(
            section_title="Our Gallery",
            main_title="Seamless logistics, faster deliveries",
            description="Whatever item needs to be delivered or shipped, we're capable to do that!"
        )
    
    # Catégories actives
    categories = PortfolioCategory.objects.filter(is_active=True).order_by('display_order')
    
    # Éléments du portfolio
    portfolio_items = PortfolioItem.objects.filter(is_active=True).order_by('display_order', '-created_at')



 # Si elle n'existe pas, créez-la via l'admin
    if not collection:
        collection = Collection.objects.create(
            section_title="NOS COLLECTIONS EXCLUSIVES",
            main_title="Découvrez nos gammes de bijoux raffinés",
            description="Des créations uniques pour chaque occasion, de l'élégance discrète à la pièce statement"
        )


    if not cta:
        cta = CTA.objects.create(
            section_title="Pourquoi Nous Choisir",
            main_title="Des bijoux qui racontent votre histoire !",
            description="Chaque pièce est une œuvre d'art unique, créée avec passion et expertise. De la conception à la réalisation, nous nous engageons pour l'excellence et l'authenticité.",
            phone_label="CONSEIL PERSONNALISÉ",
            phone_number="+33 1 23 45 67 89",
            phone_display="+33 1 23 45 67 89"
        )


    if not services.exists():
        default_services = [
            {
                'title': '100% Satisfaction',
                'description': 'Lorem Ipsum',
                'icon_filename': '1.svg',
                'order': 1
            },
            {
                'title': 'Fast Delivery',
                'description': 'Lorem Ipsum',
                'icon_filename': '3.svg',
                'order': 2
            },
            {
                'title': '24x7 Service',
                'description': 'Lorem Ipsum',
                'icon_filename': '2.svg',
                'order': 3
            }
        ]


        for service_data in default_services:
            Service.objects.create(**service_data)
        
        services = Service.objects.filter(is_active=True).order_by('order')[:3]


        if not testimonials.exists():
         default_testimonials = [
            {
                'name': 'Alexandra Grant',
                'location': 'Los Angeles, USA',
                'content': 'We are full-cycle software development and digital solutions company with rich expertise and focus on the latest technologies',
                'photo_filename': '1.jpg',
                'order': 1
            },
            {
                'name': 'John Smith',
                'location': 'New York, USA',
                'content': 'Excellent service and professionalism. The team delivered exactly what we needed on time and within budget.',
                'photo_filename': '2.jpg',
                'order': 2
            },
            {


                'name': 'Marie Dubois',
                'location': 'Paris, France',
                'content': 'Très satisfaite du travail accompli. Une équipe réactive et compétente qui a su comprendre nos besoins.',
                'photo_filename': '3.jpg',
                'order': 3
            }
        ]
        
        for testimonial_data in default_testimonials:
            Testimonial.objects.create(**testimonial_data)
        
        testimonials = Testimonial.objects.filter(is_active=True).order_by('order')[:3]


    context = {
        'title': 'TP WEB L3 Info',
        'about': about_instance,
        'collection': collection,
        'cta': cta,
        'services': services,
        'testimonials': testimonials,
        'slides': slides,
        'settings': settings,
        'expertise': expertise,  # Ajoute la section savoir-faire
        'team_section': team_section,  # Ajoute la section équipe
        'pricing_plans': pricing_plans,
        'blog_posts': blog_posts,
        'clients': clients,
        'video_section': video_section,
        'photos_galerie': photos_galerie,
        'portfolio': portfolio,
        'portfolio_items': portfolio_items,
        'categories': categories,



        }
    return render(request, 'website/pages/index.html', context)

def about(request):
    banners = Banner.objects.filter(page='About')
    collection = Collection.objects.first()
    cta = CTA.objects.filter(is_active=True).first()

    # Récupère le premier enregistrement About (ou celui que vous voulez)
    about_instance = About.objects.first()

     # Si elle n'existe pas, créez-la via l'admin
    if not collection:
        collection = Collection.objects.create(
            section_title="NOS COLLECTIONS EXCLUSIVES",
            main_title="Découvrez nos gammes de bijoux raffinés",
            description="Des créations uniques pour chaque occasion, de l'élégance discrète à la pièce statement"
        )
    
    context = {
        'banners': banners,
        'about': about_instance,  # Maintenant c'est l'instance About
        'collection': collection,
        'cta': cta,
    }
    return render(request, 'website/pages/about.html', context)

def contact(request):
    """Page de contact"""
    banners = Banner.objects.filter(page="Contact")
    contact_info = ContactInfo.objects.filter(is_active=True).first()
    
    # Si aucune info de contact n'existe, créez-en une par défaut
    if not contact_info:
        contact_info = ContactInfo.objects.create(
            section_title="Get In Touch",
            main_title="Talk or Meet with Us",
            address_title="Get Us Here",
            address_line1="1355 Market St, Suite 900",
            address_line2="San Francisco, CA 94",
            phone_title="Call Us",
            phone_number="+1 123 456 7890",
            email_title="Write Us",
            email_address="info@thisone.com",
            form_title="Estimate Project",
            form_heading="Let Us Know Here",
            submit_button_text="SEND MESSAGE"
        )
    
    context = {
        'banners': banners,
        'contact': contact_info,
    }
    return render(request, 'website/pages/contact.html', context)

def contact_submit(request):
    """Traitement du formulaire de contact"""
    if request.method == 'POST':
        name = request.POST.get('name', '').strip()
        email = request.POST.get('email', '').strip()
        website = request.POST.get('website', '').strip()
        message_text = request.POST.get('message', '').strip()
        
        # Validation simple
        if not name or not email or not message_text:
          messages.error(request, "Veuillez remplir tous les champs obligatoires.")
          return redirect('contact')
        
        # Créer le message
        contact_message = ContactMessage.objects.create(
            name=name,
            email=email,
            website=website if website else None,
            message=message_text,
            ip_address=get_client_ip(request),
            user_agent=request.META.get('HTTP_USER_AGENT', '')
        )
        
        # Optionnel : Envoyer un email de notification
        # send_contact_notification(contact_message)
        
        messages.success(request, "Votre message a été envoyé avec succès. Nous vous répondrons bientôt.")
        return redirect('contact')
    
    return redirect('contact')

def get_client_ip(request):
    """Récupère l'adresse IP du client"""
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip
    


def our_services(request):
    banners = Banner.objects.filter(page='Service')
    collection = Collection.objects.first()
    expertise = ExpertiseSection.objects.filter(is_active=True).order_by('display_order').first()
    testimonials = Testimonial.objects.filter(is_active=True).order_by('order')[:3]
    clients = Client.objects.filter(is_active=True).order_by('order')
    
    # Récupérer tous les services
    all_services = Service.objects.filter(is_active=True).order_by('order')
    
    # Services pour la section principale
    services = Service.objects.filter(is_active=True).order_by('order')[:3]

    if not services.exists():
        default_services = [
            {
                'title': '100% Satisfaction',
                'description': 'Lorem Ipsum',
                'icon_filename': '1.svg',
                'order': 1
            },
            {
                'title': 'Fast Delivery',
                'description': 'Lorem Ipsum',
                'icon_filename': '3.svg',
                'order': 2
            },
            {
                'title': '24x7 Service',
                'description': 'Lorem Ipsum',
                'icon_filename': '2.svg',
                'order': 3
            }
        ]


        for service_data in default_services:
            Service.objects.create(**service_data)

        services = Service.objects.filter(is_active=True).order_by('order')[:3]

    context = {
        'title': 'Our Services',
        'banners': banners,
        'services': services,
        'all_services': all_services,
        'testimonials': testimonials,
        'expertise': expertise,
        'clients': clients,
        'collection': collection,
    }

    return render(request,'website/pages/our-services.html',context)


def services_detail(request):
    """Render service details page."""
    
    banners = Banner.objects.filter(page='Service_Detail')
    connect_section = ConnectSection.objects.filter(is_active=True).first()
    
    # Prend la première collection active
    current_collection = JewelryCollection.objects.filter(is_active=True).first()
    
    if not current_collection:
        # Si aucune collection n'existe, crée-en une de test ou passe None
        current_collection = None
    
    all_collections = JewelryCollection.objects.filter(is_active=True).order_by('order')
    
    context = {
        'title': 'Service Details',
        'banners': banners,
        'connect_section': connect_section,
        'current_collection': current_collection,
        'all_collections': all_collections,
    }
    return render(request, 'website/pages/services-detail.html', context)


def gallery(request):
    banners = Banner.objects.filter(page='Gallery')
    services = Service.objects.filter(is_active=True).order_by('order')[:3]
    testimonials = Testimonial.objects.filter(is_active=True).order_by('order')[:3]
    portfolio = PortfolioSection.objects.filter(is_active=True).first()
    photos_galerie = PhotoGalerie.objects.all().order_by('ordre')[:9]

    if not portfolio:
        portfolio = PortfolioSection.objects.create(
            section_title="Our Gallery",
            main_title="Seamless logistics, faster deliveries",
            description="Whatever item needs to be delivered or shipped, we're capable to do that!"
        )
    
    # Catégories actives
    categories = PortfolioCategory.objects.filter(is_active=True).order_by('display_order')
    
    # Éléments du portfolio
    portfolio_items = PortfolioItem.objects.filter(is_active=True).order_by('display_order', '-created_at')

    #gallery= Gallery.objects.all()

    if not services.exists():
        default_services = [
            {
                'title': '100% Satisfaction',
                'description': 'Lorem Ipsum',
                'icon_filename': '1.svg',
                'order': 1
            },
            {
                'title': 'Fast Delivery',
                'description': 'Lorem Ipsum',
                'icon_filename': '3.svg',
                'order': 2
            },
            {
                'title': '24x7 Service',
                'description': 'Lorem Ipsum',
                'icon_filename': '2.svg',
                'order': 3
            }
        ]


        for service_data in default_services:
            Service.objects.create(**service_data)
        
        services = Service.objects.filter(is_active=True).order_by('order')[:3]



    context = {
        'title': 'Gallery',
        'banners': banners,
        'services': services,
        'portfolio': portfolio,
        'categories': categories,
        'testimonials': testimonials,
        'portfolio_items': portfolio_items,
        'photos_galerie': photos_galerie,


    }
    return render(request, 'website/pages/gallery.html',context)
    
def team(request):
    banners = Banner.objects.filter(page='Team')
    team_section = TeamSection.objects.filter(is_active=True).order_by('display_order').first()
    testimonials = Testimonial.objects.filter(is_active=True).order_by('order')[:3]
    clients = Client.objects.filter(is_active=True).order_by('order')



    #team_members = TeamMember.objects.all()
    context = {
        'title': 'Our Team',
        'banners': banners,
        #'team_members': team_members,
        'team_section': team_section,  # Ajoute la section équipe
        'testimonials': testimonials,
        'clients': clients,



    }
    return render(request, 'website/pages/team.html',context)


def pricing(request):
    banners = Banner.objects.filter(page='Pricing')
    pricing_plans = PricingPlan.objects.filter(is_active=True).order_by('order')
    testimonials = Testimonial.objects.filter(is_active=True).order_by('order')[:3]

    context = {
        'title': 'Pricing',
        'banners': banners,
        'pricing_plans': pricing_plans,  # Nom correct de la variable
        'testimonials': testimonials,

    }
    return render(request, 'website/pages/pricing.html',context)



def blog(request):
    banners = Banner.objects.filter(page='Blog')
            # Essayer de récupérer les éléments de la sidebar
        # Si le modèle n'existe pas, laisser à None
    
    blog_banner = BlogBanner.objects.filter(is_active=True).first()
    blog_posts = BlogPost.objects.filter(is_published=True).order_by('-published_date')[:3]
    categories_sidebar = CategorieSidebar.objects.all().order_by('ordre')
    articles_populaires = ArticleSidebar.objects.filter(type_article='populaire').order_by('ordre')[:4]
    articles_recents = ArticleSidebar.objects.filter(type_article='recent').order_by('ordre')[:4]
    photos_galerie = PhotoGalerie.objects.all().order_by('ordre')[:9]
    

    """Render the blog listing page."""
    context = {

        'banners': banners,
        #'blogs': blogs,
        'title': 'Blog',
        'blog_banner': blog_banner,
        'blog_posts': blog_posts,
        'articles_recents': articles_recents,
        'categories_sidebar': categories_sidebar,
        'articles_populaires': articles_populaires,
        'articles_recents': articles_recents,
        'photos_galerie': photos_galerie,
        'blog_banner': blog_banner, 


    }
    return render(request, 'website/pages/blog.html', context)

from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from django.db.models import Q


def blog_list(request):
    """Liste des articles"""
    # CORRECTION : Utiliser le bon champ de statut
    posts_list = BlogPost.objects.filter(is_published=True).order_by('-published_date')
    
    # Pagination
    paginator = Paginator(posts_list, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    # Données pour la sidebar
    categories = BlogCategory.objects.all()
    popular_posts = BlogPost.objects.filter(is_published=True).order_by('-view_count')[:4]
    recent_posts = BlogPost.objects.filter(is_published=True).order_by('-published_date')[:4]
    tags = Tag.objects.all()
    

    
    # Contenu sidebar
    sidebar_content = {}
    try:
        for content in SidebarContent.objects.filter(is_active=True):
            sidebar_content[content.content_type] = content
    except (NameError, AttributeError):
        pass
    
    context = {
        'posts': page_obj,
        'page_obj': page_obj,
        'is_paginated': paginator.num_pages > 1,
        'categories': categories,
        'popular_posts': popular_posts,
        'recent_posts': recent_posts,
        'tags': tags,
        'sidebar_content': sidebar_content,
    }
    
    return render(request, 'website/blog.html', context)


def blog_detail(request, slug):
    """Détail d'un article"""
    post = get_object_or_404(BlogPost, slug=slug, is_published=True)
    
    # Incrémenter le compteur de vues
    post.view_count += 1
    post.save(update_fields=['view_count'])
    
    # Articles similaires (même catégorie)
    related_posts = BlogPost.objects.filter(
        category=post.category, 
        is_published=True
    ).exclude(id=post.id)[:3]
    
    context = {
        'post': post,
        'related_posts': related_posts,
    }
    
    return render(request, 'website/blog_detail.html', context)


def blog_category(request, slug):
    """Articles par catégorie"""
    category = get_object_or_404(BlogCategory, slug=slug)
    posts = BlogPost.objects.filter(category=category, status='published').order_by('-publication_date')
    
    context = {
        'category': category,
        'posts': posts,
    }
    
    return render(request, 'website/blog_category.html', context)

def blog_tag(request, slug):
    """Articles par tag"""
    tag = get_object_or_404(Tag, slug=slug)
    posts = BlogPost.objects.filter(tags=tag, status='published').order_by('-publication_date')
    
    context = {
        'tag': tag,
        'posts': posts,
    }
    
    return render(request, 'website/blog_tag.html', context)

def blog_search(request):
    """Recherche d'articles"""
    query = request.GET.get('q', '')
    if query:
        posts = BlogPost.objects.filter(
            Q(title__icontains=query) | 
            Q(content__icontains=query) |
            Q(excerpt__icontains=query),
            status='published'
        ).order_by('-publication_date')
    else:
        posts = BlogPost.objects.none()
    
    context = {
        'posts': posts,
        'query': query,
    }
    
    return render(request, 'website/blog_search.html', context) 




from django.shortcuts import render, get_object_or_404
from .models import ArticleDetail, CategorieSidebar, ArticleSidebar, PhotoGalerie

def single_blog_right(request, slug=None):
    blog_banner = BlogBanner.objects.filter(is_active=True).first()

    """Page single blog avec sidebar à droite"""
    
    # CORRECTION : Vérifier si ArticleDetail existe
    article = None
    try:
        if slug:
            article = get_object_or_404(ArticleDetail, slug=slug, est_actif=True)
        else:
            article = ArticleDetail.objects.filter(est_actif=True).first()
    except (NameError, AttributeError):
        # Si ArticleDetail n'existe pas, essayer avec BlogPost
        try:
            if slug:
                article = get_object_or_404(BlogPost, slug=slug, is_published=True)
            else:
                article = BlogPost.objects.filter(is_published=True).first()
        except (NameError, AttributeError):
            pass

    categories_sidebar = CategorieSidebar.objects.all().order_by('ordre')
    articles_populaires = ArticleSidebar.objects.filter(type_article='populaire').order_by('ordre')[:4]
    articles_recents = ArticleSidebar.objects.filter(type_article='recent').order_by('ordre')[:4]
    photos_galerie = PhotoGalerie.objects.all().order_by('ordre')[:9]
    
    context = {
        'article': article,
        'categories_sidebar': categories_sidebar,
        'articles_populaires': articles_populaires,
        'articles_recents': articles_recents,
        'photos_galerie': photos_galerie,
        'blog_banner': blog_banner,
    }
    
    return render(request, 'website/pages/single-blog-post-right-sidebar.html', context)
    

def single_blog_left(request):
    """Render single blog post with left sidebar."""
    
    # Prend le premier article publié (ou un article spécifique)
    article = ArticleBlog.objects.filter(est_publie=True).first()
    blog_banner = BlogBanner.objects.filter(is_active=True).first()

    if not article:
        # Si aucun article n'existe, crée un contexte vide ou un message d'erreur
        context = {
            'error': 'Aucun article disponible pour le moment.',
            'categories': CategorieArticle.objects.all().order_by('ordre'),
            'mots_cles': MotCleArticle.objects.all(),
        }
        return render(request, 'website/pages/single-blog-post-left-sidebar.html', context)
    
    # Incrémente les vues
    article.nombre_vues += 1
    article.save(update_fields=['nombre_vues'])
    
    # Données sidebar
    categories = CategorieArticle.objects.all().order_by('ordre')
    mots_cles = MotCleArticle.objects.all()
    articles_populaires = ArticlePopulaire.objects.select_related('article').order_by('-clics')[:4]
    
    # Sections sidebar
    section_a_propos = SidebarBlog.objects.filter(type_section='a_propos', est_actif=True).first()
    section_galerie = SidebarBlog.objects.filter(type_section='galerie', est_actif=True).first()
    images_galerie = ImageGalerieSidebar.objects.filter(section_sidebar=section_galerie).order_by('ordre')[:9] if section_galerie else []
    
    # Articles récents
    articles_recents = ArticleBlog.objects.filter(est_publie=True).order_by('-date_publication')[:4]
    
    # Commentaires
    commentaires = article.commentaires.filter(est_approuve=True, parent__isnull=True)
    
    context = {
        'article': article,
        'categories': categories,
        'mots_cles': mots_cles,
        'articles_populaires': articles_populaires,
        'articles_recents': articles_recents,
        'section_a_propos': section_a_propos,
        'images_galerie': images_galerie,
        'commentaires': commentaires,
        'blog_banner': blog_banner,

    }
    
    return render(request, 'website/pages/single-blog-post-left-sidebar.html', context)



from django.shortcuts import render
from .models import ArticleCentre

def single_blog_no_sidebar(request):
    """Page single blog sans sidebar (centré)"""
    blog_banner = BlogBanner.objects.filter(is_active=True).first()

    
    # Prend le premier article actif
    article = ArticleCentre.objects.filter(est_actif=True).first()
    
    # Si aucun article n'existe
    if not article:
        article = None
    
    # Récupère les commentaires approuvés (sans les réponses parentes)
    commentaires = []
    if article:
        commentaires = article.commentaires.filter(approuve=True, parent__isnull=True)
    
    context = {
        'article': article,
        'commentaires': commentaires,
        'blog_banner': blog_banner,


    }
    
    return render(request, 'website/pages/single-blog-post-without-sidebar.html', context)
    """Render single blog post without sidebar."""

    
def banner(request):
    banners = Banner.objects.all()
    context = {
        'banners': banners,
        
    }
    return render(request, 'website/pages/banner.html', context)


def home(request):
    about_instance = About.objects.first()
    collection = Collection.objects.first()
    cta = CTA.objects.filter(is_active=True).first()

     # Si elle n'existe pas, créez-la via l'admin
    if not collection:
        collection = Collection.objects.create(
            section_title="NOS COLLECTIONS EXCLUSIVES",
            main_title="Découvrez nos gammes de bijoux raffinés",
            description="Des créations uniques pour chaque occasion, de l'élégance discrète à la pièce statement"
        )


    if not cta:
        cta = CTA.objects.create(
            section_title="Pourquoi Nous Choisir",
            main_title="Des bijoux qui racontent votre histoire !",
            description="Chaque pièce est une œuvre d'art unique, créée avec passion et expertise. De la conception à la réalisation, nous nous engageons pour l'excellence et l'authenticité.",
            phone_label="CONSEIL PERSONNALISÉ",
            phone_number="+33 1 23 45 67 89",
            phone_display="+33 1 23 45 67 89"
        )


    context = {
        'title': 'TP WEB L3 Info',
        'about': about_instance,
        'collection': collection,
        'cta': cta,
    }
    return render(request, 'website/pages/index.html', context)
