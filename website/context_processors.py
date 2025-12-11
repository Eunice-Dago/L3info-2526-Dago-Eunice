# Dans website/context_processors.py
from .models import FooterInfo, LienFooter

def footer_context(request):
    """Ajoute les données du footer à tous les templates"""
    try:
        footer_config = FooterInfo.load()
        liens_boutique = LienFooter.objects.filter(type_lien='boutique').order_by('ordre')
        liens_collections = LienFooter.objects.filter(type_lien='collections').order_by('ordre')
    except:
        # Si les modèles n'existent pas encore
        footer_config = None
        liens_boutique = []
        liens_collections = []
    
    return {
        'footer_config': footer_config,
        'liens_boutique': liens_boutique,
        'liens_collections': liens_collections,
    }

# website/context_processors.py
from .models import BlogBanner

def global_blog_banner(request):
    """Ajoute la bannière de blog active à tous les templates."""
    blog_banner = BlogBanner.objects.filter(is_active=True).first()
    return {
        'global_blog_banner': blog_banner
    }