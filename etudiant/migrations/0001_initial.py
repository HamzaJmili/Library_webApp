# Generated by Django 5.0.4 on 2024-04-30 16:22

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Etudiant',
            fields=[
                ('cne', models.CharField(max_length=50, primary_key=True, serialize=False)),
                ('prenom', models.CharField(max_length=100)),
                ('nom', models.CharField(max_length=100)),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('mot_de_passe', models.CharField(max_length=100)),
            ],
            options={
                'db_table': 'Etudiant',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='Exemplaire',
            fields=[
                ('id_exmp', models.AutoField(primary_key=True, serialize=False)),
                ('etat', models.CharField(max_length=50)),
            ],
            options={
                'db_table': 'Exemplaire',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='Livre',
            fields=[
                ('titre', models.CharField(max_length=255)),
                ('id_livre', models.AutoField(primary_key=True, serialize=False)),
                ('auteur', models.CharField(max_length=100)),
                ('description', models.TextField()),
                ('nb_pages', models.IntegerField()),
                ('nb_exemplaires', models.IntegerField()),
                ('nb_vues', models.IntegerField(default=0)),
                ('image', models.ImageField(upload_to='photos/')),
            ],
            options={
                'db_table': 'livre',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id_tag', models.AutoField(primary_key=True, serialize=False)),
                ('nom_tag', models.CharField(max_length=50)),
            ],
            options={
                'db_table': 'Tag',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='Emprunt',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_emprunt', models.DateField()),
                ('confirmer', models.BooleanField(default=False)),
                ('date_retour', models.DateField(blank=True, null=True)),
                ('etudiant', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='etudiant.etudiant')),
                ('exemplaire', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='etudiant.exemplaire')),
            ],
            options={
                'db_table': 'Emprunt',
                'managed': True,
            },
        ),
        migrations.AddField(
            model_name='exemplaire',
            name='livre',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='etudiant.livre'),
        ),
        migrations.AddField(
            model_name='livre',
            name='tags',
            field=models.ManyToManyField(null=True, to='etudiant.tag'),
        ),
    ]
