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
    ,path('blog.html', views.blog_list, name='blog_list')
    ,path('single-blog-post-right-sidebar.html', views.single_blog_right, name='single_blog_right')
    ,path('single-blog-post-left-sidebar.html', views.single_blog_left, name='single_blog_left')
    ,path('single-blog-post-without-sidebar.html', views.single_blog_no_sidebar, name='single_blog_no_sidebar')
    ,path('admin/', admin.site.urls)
    ,path('blog/<slug:slug>/left-sidebar/', views.single_post_left_sidebar, name='post_left_sidebar')
    ,path('blog/<slug:slug>/right-sidebar/', views.single_post_right_sidebar, name='post_right_sidebar')
    ,path('blog/<slug:slug>/no-sidebar/', views.single_post_no_sidebar, name='post_no_sidebar')
    ,path('blog/search/', views.search_posts, name='search_posts')
    ,path('blog/category/<slug:slug>/', views.posts_by_category, name='posts_by_category')
    ,path('blog/category/<slug:slug>/', views.posts_by_category, name='blog_category') # Alias
    ,path('blog/tag/<slug:slug>/', views.posts_by_tag, name='posts_by_tag')

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
