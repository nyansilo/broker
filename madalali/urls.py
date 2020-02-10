
from django.contrib import admin
from django.urls import path, re_path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from accounts import views as user_views

urlpatterns = [
    path('admin/', admin.site.urls),
    #path('tinymce/', include('tinymce.urls')),
    re_path(r'^tinymce/', include('tinymce.urls')),

    path('', include('front.urls', namespace='front')),
    path('', include('property.urls', namespace='property')),
    path('', include('blog.urls', namespace='blog')),

    path('user-profile/', user_views.user_profile, name='user_profile'),
    path('user-register/', user_views.user_register, name='user_register'),
    path('user-login/', auth_views.LoginView.as_view(
        template_name='accounts/user-login.html'), name='user_login'),
    path('logout', user_views.logout, name='logout'),
    #path('logout/', auth_views.LogoutView.as_view(template_name='accounts/logout.html'), name='logout'),

    path('password-reset/',
         auth_views.PasswordResetView.as_view(
             template_name='accounts/password_reset.html'
         ),
         name='password_reset'),
    path('password-reset/done/',
         auth_views.PasswordResetDoneView.as_view(
             template_name='accounts/password_reset_done.html'
         ),
         name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(
             template_name='accounts/password_reset_confirm.html'
         ),
         name='password_reset_confirm'),
    path('password-reset-complete/',
         auth_views.PasswordResetCompleteView.as_view(
             template_name='accounts/password_reset_complete.html'
         ),
         name='password_reset_complete'),

    # REST FRAMEWORK URLS
    path('api/blog/', include('blog.api.urls', namespace='blog_api')),
]


if settings.DEBUG:
    urlpatterns += static(
        settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(
        settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
#urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
#urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
