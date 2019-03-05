from django import forms
from django.contrib import messages
from django.utils.translation import gettext_lazy as _
from .models import Ordonnance, Document, Diagnostic, Message, Patient, Soin, Service


class DocumentForm(forms.ModelForm):

    class Meta:
        model = Document
        fields = ['dossier', 'complet']

class OrdonnanceForm(forms.ModelForm):

    class Meta:
        model = Ordonnance
        fields = ["texte", "commanditaire"]


class DiagnosticForm(forms.ModelForm):

    class Meta:
        model = Diagnostic
        fields = ["fichier", "observation"]


class SoinForm(forms.ModelForm):

    class Meta:
        model = Soin
        fields = ['texte']


class MessagerieForm(forms.ModelForm):

    class Meta:
        model = Message
        fields = ["receiver","objet","content"]


class PatientForm(forms.ModelForm):

    class Meta:
        model = Patient
        fields = ['nom', 'prenom', 'date_naissance', 'telephone', 'adresse' , "numsecu", "hospitalisation", "sexe" ]
        widgets = {
            'telephone' : forms.TextInput(attrs={"placeholder":"0102030405"}),
            'nom' : forms.TextInput(attrs={"placeholder":"Nom du patient"}),
            'prenom': forms.TextInput(attrs={"placeholder": "Prénom du patient"}),
            'date_naissance' : forms.TextInput(attrs={"placeholder":"__/__/____"}),
            'adresse': forms.TextInput(attrs={"placeholder": "Adresse du patient"}),
            'numsecu': forms.TextInput(attrs={"placeholder": "288127511510792 "})

        }



class ProfilEditForm(forms.Form):
    nom = forms.CharField(max_length=50, required=False, label=_("Changer mon nom"))
    prenom = forms.CharField(max_length=50, required=False, label=_("Changer mon prénom"))
    telephone = forms.CharField(max_length=10, required=False, label=_("Changer mon numéro de téléphone"))
    adresse = forms.CharField(max_length=150, required=False, label=_("Changer mon adresse"))
    demande = forms.BooleanField(required=False, label=_("Effectuer une demande de réaffectation"))
    reaffectation = forms.ModelChoiceField(queryset=Service.objects.all(),
                                           required=False,
                                           empty_label=_("Quelle est votre réaffectation"),
                                           label=_("Réaffecation"))