from django.urls import path
from . import views
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static



app_name = 'website'
urlpatterns = [
    
     path('', views.index, name='home')
    ,path('index.html', views.index, name='index')
    ,path('about-us.html', views.about, name='about')
    ,path('contact.html', views.contact, name='contact')
    ,path('contact/submit/', views.contact_submit, name='contact_submit')
    ,path('our-services.html', views.our_services,name='services')
    ,path('services-detail.html', views.services_detail, name='services_detail')
    ,path('gallery.html', views.gallery, name='gallery')
    ,path('team.html', views.team, name='team')
    ,path('pricing.html', views.pricing, name='pricing')
    ,path('blog.html', views.blog, name='blog')
    ,path('single-blog-post-right-sidebar.html', views.single_blog_right, name='single_blog_right')
    ,path('single-blog-post-left-sidebar.html', views.single_blog_left, name='single_blog_left')
    ,path('single-blog-post-without-sidebar.html', views.single_blog_no_sidebar, name='single_blog_no_sidebar')
    ,path('admin/', admin.site.urls)
    ,path('blog/search/', views.blog_search, name='blog_search')
    ,path('blog/category/<slug:slug>/', views.blog_category, name='blog_category')
    ,path('blog/tag/<slug:slug>/', views.blog_tag, name='blog_tag')
    ,path('blog/<slug:slug>/', views.blog_detail, name='blog_detail')


] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
