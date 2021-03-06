# Generated by Django 3.2 on 2021-05-08 18:04

import covidtest.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('covidtest', '0004_alter_pojistenec_cislo_pojistence'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='test',
            options={'ordering': ['-vyhodnoceni']},
        ),
        migrations.AlterField(
            model_name='osoba',
            name='rodne_cislo',
            field=models.CharField(help_text='Zadejte rodné číslo bez lomítka.', max_length=10, unique=True, validators=[covidtest.models.is_number], verbose_name='Rodné číslo'),
        ),
        migrations.AlterField(
            model_name='pojistenec',
            name='cislo_pojistence',
            field=models.CharField(max_length=10, unique=True, validators=[covidtest.models.is_number], verbose_name='Číslo pojištěnce'),
        ),
    ]
