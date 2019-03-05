# Generated by Django 2.1.5 on 2019-02-12 16:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('updd', '0004_personnel_affectation'),
    ]

    operations = [
        migrations.AddField(
            model_name='patient',
            name='sexe',
            field=models.CharField(choices=[('Femme', 'Femme'), ('Homme', 'Homme')], default='Homme', max_length=10),
        ),
        migrations.AddField(
            model_name='personnel',
            name='sexe',
            field=models.CharField(choices=[('Femme', 'Femme'), ('Homme', 'Homme')], default='Homme', max_length=10),
        ),
    ]
