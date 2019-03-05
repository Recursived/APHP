"""aphp URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from . import views
from django.urls import path, re_path
from django.contrib.auth.views import (
    LoginView,
    PasswordResetView,
    PasswordResetDoneView,
    PasswordResetCompleteView,
    PasswordResetConfirmView,
    LogoutView
)

urlpatterns = [
    path('', views.AccueilView.as_view(), name="accueil"),
    path('accounts/login/', LoginView.as_view(), name="login"),
    path('resetpwd/', PasswordResetView.as_view(), name='password_reset'),
    path('resetpwd/done/', PasswordResetDoneView.as_view(), name='password_reset_done'),
    re_path(r'^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>.+)/$', PasswordResetConfirmView.as_view(), name="password_reset_confirm"),
    path('reset/done/',PasswordResetCompleteView.as_view(), name="password_reset_complete"),
    path('profil/', views.ProfilView.as_view(), name="profil"),
    path('logout/', LogoutView.as_view(next_page="login"), name='logout'),
    path('user/agenda/', views.AgendaView.as_view(), name="agenda"),
    path('listedossier/<int:page>/', views.ListeDossierPatient.as_view(), name="liste_dossier_patient"),
    path('new/ordonnance/', views.OrdonnanceFormView.as_view(), name='new_ordonnance'),
    path('patient/<int:pk>/dossier', views.DossierPatientView.as_view(), name="dossier_patient"),
    path('updd/messagerie/<int:page>', views.MessagerieView.as_view(), name="messagerie"),
    path('updd/notification/<int:page>', views.NotificationView.as_view(),name="notification"),
    path('new/dmp/', views.DMPFormView.as_view(), name="new_dmp"),
    path('new/diagnostic/', views.DiagnsoticFormView.as_view(), name="new_diagnostic"),
    path('new/fichesoin/', views.SoinFormView.as_view(), name="new_soin"),
    path('profil/edit/', views.ProfilEditView.as_view(), name="profil_update"),
    path('listeordo/<int:page>/', views.ListeOrdoValidation.as_view(), name="liste_ordo"),
    path('ordo/review/<int:pk>', views.ValidationOrdoView.as_view(), name="validation_ordo")
]
