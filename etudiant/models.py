from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone

from django.urls import path
class Tag(models.Model):
    id_tag = models.AutoField(primary_key=True)
    nom_tag = models.CharField(max_length=50)
    class Meta:
        managed = True
        db_table = 'Tag'
    def __str__(self):
        return self.nom_tag
    


class Livre(models.Model):
    titre = models.CharField(max_length=255)
    id_livre = models.AutoField(primary_key=True)
    auteur = models.CharField(max_length=100)
    description = models.TextField()
    nb_pages = models.IntegerField()
    pret = models.BooleanField(default=True)
    nb_exemplaires = models.IntegerField()

    
    nb_vues=models.IntegerField(default=0)
    image=models.ImageField(upload_to='photos/')
    tags=models.ManyToManyField(Tag,null=True)

    def __str__(self):
        return self.titre
    
    class Meta:
        managed = True
        db_table = 'livre'


        

class Exemplaire(models.Model):
    etats=[
        ('Disponible','Disponible'),
        ('emprunte','emprunte'),
        ('a enlever','a enlever')
    ]

    id_exmp = models.AutoField(primary_key=True)
    etat = models.CharField(max_length=50,null=True,blank=True , choices=etats)
    livre = models.ForeignKey(Livre, on_delete=models.CASCADE)

    class Meta:
        managed = True
        db_table = 'Exemplaire'
    def __str__(self):
        return ("id: "+str(self.id_exmp)+" --- book: "+self.livre.titre[:30])
    
@receiver(post_save, sender=Livre)
def create_exemplaires(sender, instance, created, **kwargs):
    if created:
        for _ in range(instance.nb_exemplaires):
            Exemplaire.objects.create(livre=instance, etat="Disponible")
       


        



       

class Etudiant(models.Model):
    cne = models.CharField(max_length=50, primary_key=True)
    prenom = models.CharField(max_length=100)
    nom = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    mot_de_passe = models.CharField(max_length=100)
    class Meta:
        managed = True
        db_table = 'Etudiant'
    def __str__(self):
        return (self.cne)
    

class Emprunt(models.Model):
    date_emprunt = models.DateField()
    confirmer = models.BooleanField(default=False)
    date_retour = models.DateField(null=True, blank=True)
    etudiant = models.ForeignKey(Etudiant, on_delete=models.CASCADE)
    exemplaire = models.ForeignKey(Exemplaire, on_delete=models.CASCADE)
    confirmer_retour =models.BooleanField(default=False)
    class Meta:
        managed = True
        db_table = 'Emprunt'
    

    
    



