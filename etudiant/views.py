import datetime
from django.http import Http404
from django.shortcuts import render,redirect
from django.contrib import messages
from .models import Livre
from .models import Tag
from .models import Etudiant
from .models import Exemplaire
from .models import Emprunt
from django.utils import timezone
from django.shortcuts import get_object_or_404, redirect


from django.contrib.auth import login as auth_login 
# Create your views here.
def home (request): 
    if 'etudiant_cne' in request.session :
        all_books=[]
        is_search = False
        if 'Search' in request.GET :
            is_search=True

            query = request.GET.get('Search')
            all_books.extend(Livre.objects.filter(titre__icontains=query)) 
            
            try:
            
                tag_search = Tag.objects.get(nom_tag=query)
                all_books.extend(Livre.objects.filter(tags=tag_search))
            except Tag.DoesNotExist or Livre.DoesNotExist:
            
                pass

            print(query)
            
            
        else:
            print("no search")
            all_books = Livre.objects.all()
        populaire=Livre.objects.all().order_by('-nb_vues')[:4]
        print(request.session['etudiant_cne'])
        all_tags = Tag.objects.all()
        if 'Search' in request.GET :
            return render(request, 'etudiant/home.html',{'books':all_books,'tags':all_tags,'populaire':populaire,'is_search':is_search ,'search':query})
        else:

            return render(request, 'etudiant/home.html',{'books':all_books,'tags':all_tags,'populaire':populaire,'is_search':is_search})
    else :
        return redirect('login')


def book(request,id_book,borrowed):
    
    if 'etudiant_cne' in request.session :
        disponible=True
        book=Livre.objects.get(id_livre=id_book)
        nb_disp_exemplaire=Exemplaire.objects.filter(livre=book,etat="Disponible").count()
        book.nb_exemplaires=nb_disp_exemplaire
        book.nb_vues=book.nb_vues+1
        
        book.save()
        tags_in_book=book.tags.all()
       
        books_fav=[]
        for tag_in_book in tags_in_book:
            nw_book=Livre.objects.filter(tags=tag_in_book)
            print("Current book ID:", book.id_livre)
            print("Filtered books after exclusion:", nw_book.values_list('id_livre', flat=True))
            books_fav.extend(Livre.objects.filter(tags=tag_in_book).exclude(pk=book.id_livre))
            if(len(books_fav)>5):
                break
        print(books_fav)
        
        

       
        if(book.nb_exemplaires==0 or book.pret==False):
            disponible=False

        return render(request, 'etudiant/single_book.html',{'book':book,'disponible':disponible,'borrowed':borrowed,'books_fav':books_fav[:4]})
    else :
        return redirect('login')
def borrow_book (request,id_book):
    if 'etudiant_cne' in request.session :

        book=Livre.objects.get(id_livre=id_book)
        
        nb_disp_exemplaire=Exemplaire.objects.filter(livre=book,etat="Disponible").count()
        if(book.nb_exemplaires!=0 and book.pret==True):
            first_disp_exemplaire = Exemplaire.objects.filter(livre=book, etat="Disponible").first()
            etudiant_s=Etudiant.objects.get(cne=request.session['etudiant_cne'])
           
            emprunt=Emprunt(date_emprunt=timezone.now().date(),confirmer= False,etudiant=etudiant_s,exemplaire=first_disp_exemplaire)
            first_disp_exemplaire.etat='emprunte'
            book.nb_exemplaires=book.nb_exemplaires-1
            book.save()
            first_disp_exemplaire.save()
            emprunt.save()
            
            return redirect('single_book', id_book=book.id_livre,borrowed='true')





    else :
        return redirect('login')

def login(request):
    msg=False
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        try:
            etudiant = Etudiant.objects.get(email=email)
            if (password== etudiant.mot_de_passe):
                
               
                request.session['etudiant_cne'] = etudiant.cne
                request.session['etudiant_email'] = etudiant.email
                
                return redirect('home') 
            else:
                msg=True
                messages.error(request, 'Invalid email or password.')
                
        except Etudiant.DoesNotExist:
            msg=True
            messages.error(request, 'Invalid email or password.')
    return render(request, 'etudiant/login.html',{'msg':msg}) 

def logout (request):
    del request.session['etudiant_cne']
    del request.session['etudiant_email']
    return redirect('login')

def profile(request):
    if 'etudiant_cne' in request.session:
        etudiant = Etudiant.objects.get(cne=request.session['etudiant_cne'])
        emprunts = Emprunt.objects.filter(etudiant=etudiant).select_related('exemplaire__livre')

        today = timezone.now().date()

        has_overdue_books = any(emprunt.is_overdue() for emprunt in emprunts)

        return render(request, 'etudiant/profile.html', {'etudiant': etudiant, 'emprunts': emprunts, 'today': today, 'has_overdue_books': has_overdue_books})
    else:
        return redirect('login')




def confirm_return_emprunt(request, pk):
    emprunt = get_object_or_404(Emprunt, pk=pk)
    emprunt.confirmer_retour = True

    # Mettre à jour la date de retour et le statut de l'exemplaire
    emprunt.date_retour = timezone.now().date()
    emprunt.exemplaire.etat = 'Disponible'
    emprunt.exemplaire.save()
    emprunt.save()
    return redirect('admin:etudiant_emprunt_changelist')

def confirm(request, pk):
    emprunt = get_object_or_404(Emprunt, pk=pk)
    emprunt.confirmer = True

    # Récupérer la date de retour depuis le formulaire
    date_retour = request.POST.get('date_retour')
    if date_retour:
        emprunt.date_retour = date_retour
    #else:
        #Définir une date de retour par défaut si aucune n'est fournie
        #emprunt.date_retour = timezone.now().date() + datetime.timedelta(days=14)  # Par exemple, 14 jours après la date de confirmation

    emprunt.save()
    return redirect('admin:etudiant_emprunt_changelist')

def annuler_emprunt(request, emprunt_id):
    try:
        emprunt = Emprunt.objects.get(id=emprunt_id, etudiant__cne=request.session['etudiant_cne'], confirmer=False)
    except Emprunt.DoesNotExist:
        raise Http404("No Emprunt matches the given query.")
    
    emprunt.exemplaire.etat = 'Disponible'
    emprunt.exemplaire.save()
    emprunt.delete()

    emprunt.exemplaire.livre.nb_exemplaires += 1
    emprunt.exemplaire.livre.save()

    return redirect('profile')

