from django.contrib import admin
from .models import Etudiant;
from .models import Livre;
from .models import Exemplaire;
from .models import Tag
from .models import Emprunt
from django.utils.html import format_html
from django.urls import reverse


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
    list_display = ['exemplaire', 'etudiant', 'date_emprunt', 'confirmer_button', 'date_retour', 'confirm_return_button']
    list_editable = ['date_retour']

    def confirm_return_button(self, obj):
        if obj.confirmer_retour:
            return format_html('<a class="button" disabled>Returned</a>')
        elif obj.confirmer:
            return format_html('<a class="button" href="{}">Confirm Return</a>', reverse('confirm_return_emprunt', args=[obj.pk]))
    confirm_return_button.short_description = "Confirm Return"

    def confirmer_button(self, obj):
        if obj.confirmer:
            return format_html('<a class="button" disabled>Confirmed</a>')
        else:
            return format_html('<a class="button" href="{}">Confirm</a>', reverse('confirm', args=[obj.pk]))
    confirmer_button.short_description = "Confirm"


    


# Register your models here.
admin.site.register(Etudiant,EtudiantAdmin)
admin.site.register(Livre,livreAdmine)
admin.site.register(Exemplaire,ExemplaireAdmin)
admin.site.register(Tag)
admin.site.register(Emprunt,EmpruntAdmin)

admin.site.site_header="Library administration"
admin.site.site_title="Library"

