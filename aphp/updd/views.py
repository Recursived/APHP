from django.contrib.auth.models import User
from django.urls import reverse_lazy
from django.views.generic.edit import FormView

from .models import DossierMedical, Personnel, Patient, Notification, Document, Operation, Soin, Ordonnance, Diagnostic, \
    Message, Medecin
from django.views.generic import TemplateView, ListView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from .mixins import GroupRequiredMixin
from .forms import DocumentForm, OrdonnanceForm, DiagnosticForm, MessagerieForm, PatientForm, SoinForm, ProfilEditForm
from .base import MultiModelFormView
from django.contrib import messages
from django.utils.translation import gettext_lazy as _
from django.db.models import Q
from django.shortcuts import redirect


# Create your views here.
class AccueilView(LoginRequiredMixin, TemplateView):
    login_url = 'login'
    permission_denied_message = _("Il faut se connecter avant d'utiliser l'application")
    template_name = "updd/accueil_template.html"


class AgendaView(GroupRequiredMixin, TemplateView):
    group_required = ['medecin', 'secretaire']
    template_name = "updd/agenda_view.html"


class ListeDossierPatient(GroupRequiredMixin, ListView):
    group_required = ['medecin', 'secretaire', 'infirmier']
    template_name = 'updd/liste_dossier_patient.html'
    model = DossierMedical
    context_object_name = "listedossier"
    paginate_by = 10
    

    def get_queryset(self):
        p = Personnel.objects.get(pk=self.request.user.pk).dossiermedical.values_list('patient_id', flat=True)
        return Patient.objects.filter(pk__in=p)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['total_dossier'] = Personnel.objects.get(pk=self.request.user).dossiermedical.count()
        return context


class DossierPatientView(GroupRequiredMixin, DetailView):
    group_required = ["medecin", "secretaire", "infirmier"]
    template_name = "updd/dossier_patient.html"
    model = Patient
    context_object_name = "patient"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        pk_patient = self.kwargs.get("pk")
        patient = Patient.objects.get(pk=pk_patient)
        doss = DossierMedical.objects.get(patient=patient)
        docs = Document.objects.filter(dossier=doss)

        #On récupère tous les fichiers médicaux
        ordos = Ordonnance.objects.filter(document__in=docs)
        soins = Soin.objects.filter(document__in=docs)
        opes = Operation.objects.filter(document__in=docs)
        diags = Diagnostic.objects.filter(document__in=docs)

        # On rajoute les infos dans le contexte
        context["ordonnances"] = ordos
        context["operations"] = opes
        context["diagnostics"] = diags
        context["soins"] = soins

        return context


class ProfilView(GroupRequiredMixin, DetailView):
    group_required = ['medecin', 'secretaire', 'infirmier']
    template_name = 'updd/profil_view.html'
    model = Personnel
    context_object_name = "personne"

    def get_object(self, queryset=None):
        return Personnel.objects.get(pk=self.request.user.pk)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["nb_message"] =  Message.objects.filter(Q(author=self.request.user.pk) | Q(receiver=self.request.user.pk)).count()
        context["nb_notif"] = Notification.objects.filter(receiver=self.request.user.pk).count()
        return context


# Formulaire Nouvelle Ordonnance
class OrdonnanceFormView(GroupRequiredMixin, MultiModelFormView):
    group_required = ['secretaire']
    template_name = 'updd/new_ordonnance.html'
    success_url = reverse_lazy("accueil")
    form_classes = {'ordoform' : OrdonnanceForm, 'docform' : DocumentForm}

    def forms_valid(self, forms):
        docform = forms["docform"].save(commit=False)
        docform.author = Personnel.objects.get(pk=self.request.user)
        docform.save()
        ordoform = forms["ordoform"].save(commit=False)
        ordoform.document = docform
        ordoform.save()
        messages.info(self.request, _("L'ordonnance a été enregistrée et une notification a été envoyé au commanditaire"))
        Notification.objects.create(raison=_("Création d'une ordonnance"),
                                    content=_("L'ordonnance du patient %s %s a été complétée, je vous prie de bien vouloir la valider ou me notifier les éléments inccorects.") % (docform.dossier.patient.prenom, docform.dossier.patient.nom ),
                                    receiver=User.objects.get(pk = ordoform.commanditaire.pk))
        return super(MultiModelFormView, self).forms_valid(forms)


class DiagnsoticFormView(GroupRequiredMixin, MultiModelFormView):
    group_required = ['secretaire']
    template_name = 'updd/new_diagnostic.html'
    success_url = reverse_lazy("accueil")
    form_classes = {'diagform' : DiagnosticForm, 'docform' : DocumentForm}

    def forms_valid(self, forms):
        docform = forms["docform"].save(commit=False)
        docform.author = Personnel.objects.get(pk=self.request.user)
        docform.save()
        diagform = forms["diagform"].save(commit=False)
        diagform.document = docform
        diagform.save()
        messages.info(self.request, _("Le diagnostic a été enregistré "))
        return super(MultiModelFormView, self).forms_valid(forms)


class SoinFormView(GroupRequiredMixin, MultiModelFormView):
    group_required = ['infirmier']
    template_name = 'updd/new_soin.html'
    success_url = reverse_lazy("accueil")
    form_classes = {'soinform' : SoinForm, 'docform' : DocumentForm}

    def forms_valid(self, forms):
        docform = forms["docform"].save(commit=False)
        docform.author = Personnel.objects.get(pk=self.request.user)
        docform.save()
        soinform = forms["soinform"].save(commit=False)
        soinform.document = docform
        soinform.save()
        messages.info(self.request, _("La fiche de soin a été enregistré "))
        return super(MultiModelFormView, self).forms_valid(forms)


class MessagerieView(GroupRequiredMixin, ListView, FormView):
    group_required = ['medecin', 'secretaire', 'infirmier']
    template_name = 'updd/messagerie_view.html'
    context_object_name = "listeMessage"
    paginate_by = 8
    form_class = MessagerieForm

    def post(self, request, *args, **kwargs):
        form = MessagerieForm(self.request.POST)
        if form.is_valid():
            mess = form.save(commit=False)
            mess.author = self.request.user
            mess.save()
        return redirect("messagerie", self.kwargs['page'])

    def get_queryset(self):
        return Message.objects.filter(Q(author=self.request.user.pk) | Q(receiver=self.request.user.pk)).order_by('-date_message')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(MessagerieView, self).get_context_data(**kwargs)
        if self.request.method == "GET":
            form = MessagerieForm()
            context["form"] = form
        return context



class NotificationView(GroupRequiredMixin, ListView):
    group_required = ['medecin', 'secretaire', 'infirmier']
    template_name = 'updd/notification_view.html'
    context_object_name = "listenotif"
    paginate_by = 8

    def get_queryset(self):
        return Notification.objects.filter(receiver=self.request.user.pk)


class DMPFormView(GroupRequiredMixin, FormView):
    group_required = ['secretaire']
    template_name = "updd/new_dmp.html"
    success_url = reverse_lazy("accueil")
    form_class = PatientForm

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            p = form.save()
            d = DossierMedical.objects.create(patient = p)
            for a in Personnel.objects.all():
                a.dossiermedical.add(d)
            messages.info(self.request, _('Le dossier du patient %s %s a été créé.') % (p.prenom, p.nom))
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

class ProfilEditView(GroupRequiredMixin, FormView):
    group_required = ['secretaire', 'medecin', 'infirmier']
    template_name = "updd/update_profil.html"
    success_url = reverse_lazy("profil")
    form_class = ProfilEditForm

    def get_initial(self):
        p = Personnel.objects.get(user=self.request.user)
        self.initial = {
            'nom' : self.request.user.last_name,
            'prenom' : self.request.user.first_name,
            'telephone' : p.telephone,
            'adresse' : p.adresse,
        }
        return self.initial.copy()

    def post(self, request, *args, **kwargs):
        form = ProfilEditForm(self.request.POST)
        if form.is_valid():
            admin = User.objects.filter(is_superuser=True).first()
            Notification.objects.create(
                raison=_("Changement de profil"),
                content=_("Bonjour,\n Je suis l'agent %s %s (%s) et je souhaite modifier mon profil.") % (
                self.request.user.first_name,
                self.request.user.last_name,
                self.request.user.pk),
                receiver=admin
            )
            print(dir(form.fields["adresse"]))
            print(type(form.cleaned_data["adresse"]))
            Message.objects.create(
                objet=_("Changement de profil - %s %s (%s) ") % (self.request.user.first_name,
                                                                  self.request.user.last_name,
                                                                  self.request.user.pk),
                author=self.request.user,
                receiver=admin,
                content=_("Bonjour, voici les nouvelles informations concernant mon profil :\n"
                          " Nom : %s;\n"
                          " Prénom : %s;\n"
                          " Téléphone : %s;\n"
                          " Adresse : %s;\n"
                          " Reaffectation : %s") % (form.cleaned_data["nom"],
                                       form.cleaned_data["prenom"],
                                       form.cleaned_data["telephone"],
                                       form.cleaned_data["adresse"],
                                       form.cleaned_data["reaffectation"] if form.cleaned_data["reaffectation"] != None else _("Aucune reaffectation")
                                       )
            )
            return self.form_valid(form)
        else:
            return self.form_invalid(form)


class ListeOrdoValidation(GroupRequiredMixin, ListView):
    group_required = ['medecin']
    template_name = 'updd/liste_ordo.html'
    model = Ordonnance
    context_object_name = "listeordo"
    paginate_by = 8

    def get_queryset(self):
        dnc = Document.objects.filter(complet=False)
        return Ordonnance.objects.filter(document__in=dnc).filter(commanditaire=Medecin.objects.get(user=Personnel.objects.get(user=self.request.user)))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['total_ordo'] = self.get_queryset().count()
        return context


class ValidationOrdoView(OrdonnanceFormView):
    group_required = ['medecin']
    template_name = 'updd/validate_ordonnance.html'
    success_url = reverse_lazy("accueil")
    form_classes = {'ordoform': OrdonnanceForm, 'docform': DocumentForm}

    def get_context_data(self, **kwargs):
        context = super(ValidationOrdoView, self).get_context_data()
        context["obj_key"] = self.kwargs.get("pk")
        return context

    def get_forms(self):
        forms = {}
        form_kwargs = self.get_form_kwargs()
        o = Ordonnance.objects.get(pk=self.kwargs.get("pk"))
        forms["ordoform"] = self.form_classes["ordoform"](instance=o, **form_kwargs["ordoform"])
        forms["docform"] = self.form_classes["docform"](instance=o.document, **form_kwargs["docform"])
        return forms

    def forms_valid(self, forms):
        messages.info(self.request, _("L'ordonnance a bien été modifiée et enregistrée."))
        forms["docform"].save()
        forms["ordoform"].save()
        return super(MultiModelFormView, self).forms_valid(forms)
