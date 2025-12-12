# tp3/website/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q
from .models import *

def index(request):
    about_instance = About.objects.first()
    collection = Collection.objects.first()
    cta = CTA.objects.filter(is_active=True).first()
    services = Service.objects.filter(is_active=True).order_by('order')[:3]
    testimonials = Testimonial.objects.all().order_by('order')[:3]
    testimonial1s = Testimonial1.objects.all()[:3]
    tests = Test.objects.all()[:3]
    slides = Slider.objects.filter(is_active=True).order_by('display_order')
    settings = SiteSettings.objects.first()   
    expertise = ExpertiseSection.objects.filter(is_active=True).order_by('display_order').first()
    team_section = TeamSection.objects.filter(is_active=True).order_by('display_order').first()
    pricing_plans = PricingPlan.objects.filter(is_active=True).order_by('order')
    
    # CORRECTION : Utilisez 'published' au lieu de 'is_published' et 'created_at' au lieu de 'published_date'
    blog_posts = Post.objects.filter(published=True).order_by('-created_at')[:3]
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
        
    testimonials = Testimonial.objects.all().order_by('order')[:3]
    testimonial1s = Testimonial1.objects.all()[:3]


    context = {
        'title': 'TP WEB L3 Info',
        'about': about_instance,
        'collection': collection,
        'cta': cta,
        'services': services,
        'testimonials': testimonials,
        'testimonial1s': testimonial1s,
        'tests':tests,
        'slides': slides,
        'settings': settings,
        'expertise': expertise,
        'team_section': team_section,
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
    about_instance = About.objects.first()

    if not collection:
        collection = Collection.objects.create(
            section_title="NOS COLLECTIONS EXCLUSIVES",
            main_title="Découvrez nos gammes de bijoux raffinés",
            description="Des créations uniques pour chaque occasion, de l'élégance discrète à la pièce statement"
        )
    
    context = {
        'banners': banners,
        'about': about_instance,
        'collection': collection,
        'cta': cta,
    }
    return render(request, 'website/pages/about.html', context)

def contact(request):
    banners = Banner.objects.filter(page="Contact")
    contact_info = ContactInfo.objects.filter(is_active=True).first()
    
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
    if request.method == 'POST':
        name = request.POST.get('name', '').strip()
        email = request.POST.get('email', '').strip()
        website = request.POST.get('website', '').strip()
        message_text = request.POST.get('message', '').strip()
        
        if not name or not email or not message_text:
            messages.error(request, "Veuillez remplir tous les champs obligatoires.")
            return redirect('contact')
        
        contact_message = ContactMessage.objects.create(
            name=name,
            email=email,
            website=website if website else None,
            message=message_text,
            ip_address=get_client_ip(request),
            user_agent=request.META.get('HTTP_USER_AGENT', '')
        )
        
        messages.success(request, "Votre message a été envoyé avec succès. Nous vous répondrons bientôt.")
        return redirect('contact')
    
    return redirect('contact')

def get_client_ip(request):
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
    clients = Client.objects.filter(is_active=True).order_by('order')
    testimonials = Testimonial.objects.all().order_by('order')[:3]
    testimonial1s = Testimonial1.objects.all()[:3]
    tests = Test.objects.all()[:3]
    all_services = Service.objects.filter(is_active=True).order_by('order')
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
        'expertise': expertise,
        'clients': clients,
        'collection': collection,
        'testimonials': testimonials,
        'testimonial1s': testimonial1s,
        'tests':tests,
    }

    return render(request,'website/pages/our-services.html',context)

def services_detail(request):
    banners = Banner.objects.filter(page='Service_Detail')
    connect_section = ConnectSection.objects.filter(is_active=True).first()
    current_collection = JewelryCollection.objects.filter(is_active=True).first()
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
    testimonials = Testimonial.objects.all().order_by('order')[:3]
    testimonial1s = Testimonial1.objects.all()[:3]
    tests = Test.objects.all()[:3]
    portfolio = PortfolioSection.objects.filter(is_active=True).first()
    photos_galerie = PhotoGalerie.objects.all().order_by('ordre')[:9]

    if not portfolio:
        portfolio = PortfolioSection.objects.create(
            section_title="Our Gallery",
            main_title="Seamless logistics, faster deliveries",
            description="Whatever item needs to be delivered or shipped, we're capable to do that!"
        )
    
    categories = PortfolioCategory.objects.filter(is_active=True).order_by('display_order')
    portfolio_items = PortfolioItem.objects.filter(is_active=True).order_by('display_order', '-created_at')

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
        'testimonial1s': testimonial1s,
        'tests':tests,
        'portfolio_items': portfolio_items,
        'photos_galerie': photos_galerie,
    }
    return render(request, 'website/pages/gallery.html',context)
    
def team(request):
    banners = Banner.objects.filter(page='Team')
    team_section = TeamSection.objects.filter(is_active=True).order_by('display_order').first()
    testimonials = Testimonial.objects.filter(is_active=True).order_by('order')[:3]
    clients = Client.objects.filter(is_active=True).order_by('order')

    context = {
        'title': 'Our Team',
        'banners': banners,
        'team_section': team_section,
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
        'pricing_plans': pricing_plans,
        'testimonials': testimonials,
    }
    return render(request, 'website/pages/pricing.html',context)

# VUES BLOG CORRIGÉES
def blog_list(request):
    banners = Banner.objects.filter(page='About')
    posts_list = Post.objects.filter(published=True).order_by('-created_at')
    paginator = Paginator(posts_list, 12)
    page_number = request.GET.get('page')
    posts = paginator.get_page(page_number)
    
    categories = BlogCategory.objects.all()
    sidebar_content = SidebarContent.objects.filter(is_active=True)
    gallery_images = GalleryImage.objects.all()[:9]
    
    # CORRECTION : Supprimez 'is_popular=True' car le champ n'existe pas
    popular_posts = Post.objects.filter(published=True).order_by('-views')[:4]  # Utilisez views pour la popularité
    recent_posts = Post.objects.filter(published=True).order_by('-created_at')[:4]
    
    context = {
        'posts': posts,
        'categories': categories,
        'sidebar_content': sidebar_content,
        'banners': banners,
        'gallery_images': gallery_images,
        'popular_posts': popular_posts,
        'recent_posts': recent_posts,
    }
    return render(request, 'website/pages/blog.html', context)

def single_post(request, slug):
    post = get_object_or_404(Post, slug=slug, published=True)
    post.increment_views()
    
    similar_posts = Post.objects.filter(
        category=post.category, 
        published=True
    ).exclude(id=post.id)[:2]
    
    categories = BlogCategory.objects.all()
    sidebar_content = SidebarContent.objects.filter(is_active=True)
    gallery_images = GalleryImage.objects.all()[:9]
    popular_posts = Post.objects.filter(published=True).order_by('-views')[:4]  # CORRECTION
    recent_posts = Post.objects.filter(published=True).order_by('-created_at')[:4]
    
    context = {
        'post': post,
        'similar_posts': similar_posts,
        'categories': categories,
        'sidebar_content': sidebar_content,
        'gallery_images': gallery_images,
        'popular_posts': popular_posts,
        'recent_posts': recent_posts,
    }
    
    return render(request, f'website/pages/blog.html', context)

def single_post_left_sidebar(request, slug):

    return single_post(request, slug, 'single_left.html')

def single_post_right_sidebar(request, slug):

     return single_post(request, slug, 'single_right.html')



def single_post_no_sidebar(request, slug):
   return single_post(request, slug, 'single_no_sidebar.html')

def search_posts(request):
    query = request.GET.get('q', '')
    results = []
    
    if query:
        results = Post.objects.filter(
            Q(title__icontains=query) | 
            Q(content__icontains=query) |
            Q(excerpt__icontains=query)
        ).filter(published=True).order_by('-created_at')
    
    context = {
        'query': query,
        'results': results,
        'results_count': results.count(),
    }
    return render(request, 'website/pages/blog.html', context)

def posts_by_category(request, slug):
    category = get_object_or_404(BlogCategory, slug=slug)
    posts = Post.objects.filter(category=category, published=True).order_by('-created_at')
    
    context = {
        'category': category,
        'posts': posts,
    }
    return render(request, 'website/pages/blog.html', context)

def posts_by_tag(request, slug):
    tag = get_object_or_404(Tag, slug=slug)
    posts = Post.objects.filter(tags=tag, published=True).order_by('-created_at')
    
    context = {
        'tag': tag,
        'posts': posts,
    }
    return render(request, 'website/pages/blog.html', context)
    
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

# Ajoutez à la fin de website/views.py

# AJOUTEZ CES FONCTIONS À LA FIN DE website/views.py

def single_blog_left(request, slug=None):
    """Alias pour single_post_left_sidebar - pour compatibilité avec urls.py"""
    if slug:
        return single_post_left_sidebar(request, slug)
    # Si pas de slug, affiche le premier article
    first_post = Post.objects.filter(published=True).first()
    if first_post:
        return single_post_left_sidebar(request, first_post.slug)
    return blog_list(request)

def single_blog_right(request, slug=None):
    """Alias pour single_post_right_sidebar - pour compatibilité avec urls.py"""
    if slug:
        return single_post_right_sidebar(request, slug)
    first_post = Post.objects.filter(published=True).first()
    if first_post:
        return single_post_right_sidebar(request, first_post.slug)
    return blog_list(request)

def single_blog_no_sidebar(request, slug=None):
    """Alias pour single_post_no_sidebar - pour compatibilité avec urls.py"""
    if slug:
        return single_post_no_sidebar(request, slug)
    first_post = Post.objects.filter(published=True).first()
    if first_post:
        return single_post_no_sidebar(request, first_post.slug)
    return blog_list(request)

# Fonctions wrapper pour les URLs sans slug
def single_post_left_sidebar_wrapper(request):
    """Pour l'URL single-blog-post-left-sidebar.html (sans slug)"""
    return single_blog_left(request)

def single_post_right_sidebar_wrapper(request):
    """Pour l'URL single-blog-post-right-sidebar.html (sans slug)"""
    return single_blog_right(request)

def single_post_no_sidebar_wrapper(request):
    """Pour l'URL single-blog-post-without-sidebar.html (sans slug)"""
    return single_blog_no_sidebar(request)

def single_blog_left(request):
    blog_banners=BlogBanner.objects.filter(page='single_blog_left')
    context = {

         'blog_banners': blog_banners,
 }

    return render(request, 'website/single-blog-post-left-sidebar.html')


def single_blog_right(request):


    blog_banners=BlogBanner.objects.filter(page='single_blog_right')

    context = {

         'blog_banners': blog_banners,
        }

    return render(request,  'website/single-blog-post-right-sidebar.html')


def single_blog_no_sidebar(request):

    blog_banners=BlogBanner.objects.filter(page='single_blog_no_sidebar')
    context = {

         'blog_banners': blog_banners,
        }


    return render(request,  'website/single-blog-post-without-sidebar.html')


