from django.contrib import admin
from .models import Etudiant;
from .models import Livre;
from .models import Exemplaire;
from .models import Tag
from .models import Emprunt

class EtudiantAdmin(admin.ModelAdmin):
    list_display =  ['cne','email',]
    search_fields = ['cne']
    

class livreAdmine(admin.ModelAdmin):
    list_display=['id_livre','titre','nb_exemplaires','pret']
    search_fields=['titre']
    list_editable=['pret']
    readonly_fields=['nb_vues']

class ExemplaireAdmin(admin.ModelAdmin):
    list_display=['id_exmp','livre','etat'] 
    list_editable=['etat']

class EmpruntAdmin(admin.ModelAdmin):
    list_display=['etudiant','exemplaire','date_emprunt','date_retour','confirmer']
    list_editable=['date_retour','confirmer']
    list_filter=['confirmer']
    


# Register your models here.
admin.site.register(Etudiant,EtudiantAdmin)
admin.site.register(Livre,livreAdmine)
admin.site.register(Exemplaire,ExemplaireAdmin)
admin.site.register(Tag)
admin.site.register(Emprunt,EmpruntAdmin)

admin.site.site_header="Library administration"
admin.site.site_title="Library"

