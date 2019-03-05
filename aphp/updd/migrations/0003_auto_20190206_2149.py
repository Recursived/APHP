# Generated by Django 2.1.5 on 2019-02-06 20:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('updd', '0002_auto_20190205_2330'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='medecin',
            name='dossiermedical',
        ),
        migrations.AddField(
            model_name='personnel',
            name='dossiermedical',
            field=models.ManyToManyField(related_name='travaille_sur', to='updd.DossierMedical'),
        ),
        migrations.AlterField(
            model_name='operation',
            name='type',
            field=models.CharField(choices=[('Chirurgie', 'Chirurgie'), ('Anesthésie', 'Anesthésie'), ('Obstétrique', 'Obstétrique')], max_length=20, verbose_name="Type de l'opération"),
        ),
        migrations.AlterField(
            model_name='ordonnance',
            name='texte',
            field=models.TextField(verbose_name='Contenu ordonnance'),
        ),
        migrations.AlterField(
            model_name='patient',
            name='adresse',
            field=models.CharField(max_length=150, verbose_name='Adresse'),
        ),
        migrations.AlterField(
            model_name='patient',
            name='date_naissance',
            field=models.DateField(verbose_name='Date de naissance'),
        ),
        migrations.AlterField(
            model_name='patient',
            name='nom',
            field=models.CharField(max_length=100, verbose_name='Nom'),
        ),
        migrations.AlterField(
            model_name='patient',
            name='numsecu',
            field=models.CharField(max_length=15, verbose_name='Numéro sécurite sociale'),
        ),
        migrations.AlterField(
            model_name='patient',
            name='prenom',
            field=models.CharField(max_length=100, verbose_name='Prenom'),
        ),
        migrations.AlterField(
            model_name='patient',
            name='telephone',
            field=models.CharField(max_length=15, verbose_name='Téléphone'),
        ),
        migrations.AlterField(
            model_name='personnel',
            name='adresse',
            field=models.CharField(max_length=150, verbose_name='Adresse'),
        ),
        migrations.AlterField(
            model_name='personnel',
            name='telephone',
            field=models.CharField(max_length=15, verbose_name='Téléphone'),
        ),
        migrations.AlterField(
            model_name='structure',
            name='nom',
            field=models.CharField(max_length=100, verbose_name='Nom'),
        ),
    ]
