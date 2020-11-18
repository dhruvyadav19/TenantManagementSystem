
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path,include
from users.views import register_view, profile_view, delete_user
from django.contrib.auth import views as auth_views
from houses.views import house_view,add_house_view,house_info,update_house, delete_house
from rentals.views import rent_house, view_rented_house, vacate_house, tenant_report, pay_rent, contact_owner, complaints, view_complaints

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',include('pages.urls')),
    path('register/',register_view, name='register-view'),
    path('delete/',delete_user, name = 'delete-view'),
    path('login/',auth_views.LoginView.as_view(template_name='users/login.html'),name='login-view'),
    path('logout/',auth_views.LogoutView.as_view(template_name='users/logout.html'),name='logout-view'),
    path('profile/',profile_view, name = 'profile-view'),
    path('view-house/',house_view,name = 'house-view'),
    path('add-house/',add_house_view, name = 'add-house-view'),
    path('view-house/<single_slug>/', house_info, name = 'house-info'),
    path('search/<single_slug>/', house_info),
    path('view-house/<single_slug>/update_house/', update_house, name='update-house'),
    path('search/<single_slug>/update_house/', update_house),
    path('search/<single_slug>/rent_house/', rent_house, name='rent-house'),
    path('view-house/<single_slug>/delete_house/',delete_house,name = 'delete-house-view'),
    path('view-rented-house/',view_rented_house, name='rented-house-view'),
    path('view-rented-house/<single_slug>/', house_info, name = 'house-info'),
    path('view-rented-house/<single_slug>/vacate-house/',vacate_house,name = 'vacate-house-view'),
    path('tenant-report/',tenant_report, name = 'tenant-report-view'),
    path('search/<single_slug>/pay-rent/',pay_rent,name = 'pay-rent-view'),
    path('view-rented-house/<single_slug>/pay-rent/',pay_rent,name = 'pay-rent-view'),
    path('search/<single_slug>/contact_owner/',contact_owner,name = 'contact-owner-view'),
    path('search/<single_slug>/register_complaints/',complaints,name = 'register-complaints'),
    path('view-rented-house/<single_slug>/register_complaints/',complaints,name = 'register-complaints'),
    path('tenant-report/view-complaint/<single_slug>/',view_complaints, name = 'view-complaints')

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
