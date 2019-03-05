from django.db import models
from django.contrib.auth.models import User
from django.core.validators import RegexValidator
from django.utils.translation import gettext_lazy as _


class Structure(models.Model):
    nom = models.CharField(max_length=100, verbose_name=_("Nom"))

    def __str__(self):
        return self.nom


class Hopital(models.Model):
    structure = models.OneToOneField("Structure", on_delete=models.CASCADE, primary_key=True)
    logo = models.ImageField(upload_to='updd/static/media')

    def __str__(self):
        return "Hopital --> " + self.structure.__str__()


class Pole(models.Model):
    structure = models.OneToOneField("Structure", on_delete=models.CASCADE, primary_key=True)
    hopital = models.ForeignKey("Hopital", on_delete=models.CASCADE)

    def __str__(self):
        return "Pole --> " + self.structure.__str__()+ " --> " + self.hopital.__str__()




class Service(models.Model):
    structure = models.OneToOneField("Structure", on_delete=models.CASCADE, primary_key=True)
    pole = models.ForeignKey("Pole", on_delete=models.CASCADE)

    def __str__(self):
        return "Service --> " + self.structure.__str__() + " --> " + self.pole.__str__()


class UH(models.Model):
    structure = models.OneToOneField("Structure", on_delete=models.CASCADE, primary_key=True)
    service = models.ForeignKey("Service", on_delete=models.CASCADE)

    def __str__(self):
        return "UH --> " + self.structure.__str__() + " --> "+ self.service.__str__()


class US(models.Model):
    structure = models.OneToOneField("Structure", on_delete=models.CASCADE, primary_key=True)
    uh = models.ForeignKey("UH", on_delete=models.CASCADE)

    def __str__(self):
        return "US --> " + self.structure.__str__() + " --> "+ self.uh.__str__()


class Personnel(models.Model):
    f = _("Femme")
    h = _("Homme")
    CHOICES = (
        (f, f),
        (h, h),
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    adresse = models.CharField(max_length=150, verbose_name=_("Adresse"), validators=[RegexValidator(regex="^[a-zA-Z0-9 ,]+$",)])
    telephone = models.CharField(max_length=15, verbose_name=_("Téléphone"), validators=[RegexValidator(regex="^[0-9]{10}$",)])
    dossiermedical = models.ManyToManyField("DossierMedical",  related_name=_("travaille_sur"))
    affectation =  models.ForeignKey('Service', on_delete=models.CASCADE, null=True)
    sexe = models.CharField(max_length=10, choices=CHOICES, default=h)

    def __str__(self):
        return f"{self.pk} - {self.user.last_name} {self.user.first_name} ({self.telephone})"


class Medecin(models.Model):
    user = models.OneToOneField("Personnel", primary_key=True, on_delete=models.CASCADE)
    dirigep = models.OneToOneField("Pole", related_name=_("dirige_pole"), on_delete=models.CASCADE)
    diriges = models.OneToOneField("Service", related_name=_("dirige_service"), on_delete=models.CASCADE)

    def __str__(self):
        return f"Medecin: {self.pk} {self.user}"


class Infirmier(models.Model):
    user = models.OneToOneField("Personnel", on_delete=models.CASCADE, primary_key=True)

    def __str__(self):
        return f"Infirmier : {self.pk} {self.user}"


class Secretaire(models.Model):
    user = models.OneToOneField("Personnel", on_delete=models.CASCADE, primary_key=True)

    def __str__(self):
        return f"Secretaire : {self.pk} {self.user}"


class Patient(models.Model):
    f = _("Femme")
    h = _("Homme")
    CHOICES = (
        (f, f),
        (h, h),
    )
    nom = models.CharField(max_length=100, verbose_name=_("Nom"))
    prenom = models.CharField(max_length=100, verbose_name=_("Prenom"))
    date_naissance = models.DateField(auto_now=False, verbose_name=_("Date de naissance"))
    telephone = models.CharField(max_length=15, verbose_name=_("Téléphone"), validators=[RegexValidator(regex="^[0-9]{10}$")])
    adresse = models.CharField(max_length=150, verbose_name=_("Adresse"), validators=[RegexValidator(regex="^[a-zA-Z0-9 ,]+$",)])
    numsecu = models.CharField(max_length=15, verbose_name=_("Numéro sécurite sociale"), validators=[RegexValidator(regex="^[0-9]{15}$")])
    hospitalisation = models.ForeignKey("US", on_delete=models.CASCADE)
    sexe = models.CharField(max_length=10, choices=CHOICES, default=h)

    def __str__(self):
        return f"Patient: {self.pk} {self.prenom} {self.nom} {self.numsecu} ({self.telephone})"


class DossierMedical(models.Model):
    patient = models.OneToOneField("Patient", on_delete=models.CASCADE)

    def __str__(self):
        return f"Doss Medical: {self.patient}"


class Document(models.Model):
    author = models.ForeignKey("Personnel", on_delete=models.CASCADE, verbose_name=_("Auteur"))
    dossier = models.ForeignKey("DossierMedical", on_delete=models.CASCADE)
    complet = models.BooleanField(default=False, verbose_name=_("Terminé"))
    date_creation = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Doc : {self.dossier} {self.author} {self.date_creation}"

class Diagnostic(models.Model):
    document = models.OneToOneField("Document", on_delete=models.CASCADE, primary_key=True)
    fichier = models.FileField()
    observation = models.TextField()

    def __str__(self):
        return f"Diag : {self.document}"


class Ordonnance(models.Model):
    document = models.OneToOneField("Document", on_delete=models.CASCADE, primary_key=True)
    texte = models.TextField(verbose_name=_("Contenu ordonnance"))
    complet = models.BooleanField(default=False, verbose_name=_("Terminé"))
    commanditaire = models.ForeignKey("Medecin", on_delete=models.CASCADE, verbose_name=_("Commanditaire"), null=True)

    def __str__(self):
        return f"Ordo: {self.document}"


class Operation(models.Model):
    chir = _("Chirurgie")
    anest = _("Anesthésie")
    obst = _("Obstétrique")
    CHOICES = (
        (chir, chir),
        (anest, anest),
        (obst, obst),
    )
    document = models.OneToOneField("Document", on_delete=models.CASCADE, primary_key=True)
    type = models.CharField(max_length=20, verbose_name=_("Type de l'opération"), choices=CHOICES)
    libelle = models.CharField(max_length=100, verbose_name=_("Libelle de l'opération"))

    def __str__(self):
        return f"Operation: {self.document}"

class Soin(models.Model):
    document = models.OneToOneField("Document", on_delete=models.CASCADE, primary_key=True)
    texte = models.TextField(verbose_name=_("Contenu fiche de soin"))

    def __str__(self):
        return f"Soin: {self.document}"


class Notification(models.Model):
    raison = models.CharField(max_length=200)
    content = models.TextField()
    receiver = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"Notif: {self.pk}"


class Message(models.Model):
    objet = models.CharField(max_length=200, verbose_name=_("Objet du message"))
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name=_("a_envoye"))
    date_message = models.DateTimeField(auto_now_add=True, verbose_name=_("Date d'envoi du message"))
    content = models.TextField(verbose_name=_("Contenu du message"))
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name=_("a_recu"), verbose_name=_("Destinataire"))

    def __str__(self):
        return f"Message: {self.pk}"
