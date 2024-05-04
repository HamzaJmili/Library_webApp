from django.shortcuts import render,redirect
from django.contrib import messages
from .models import Livre
from .models import Tag
from .models import Etudiant
from .models import Exemplaire
from .models import Emprunt
from django.utils import timezone

from django.contrib.auth import login as auth_login 
# Create your views here.
def home (request):
    if 'etudiant_cne' in request.session :
        all_books = Livre.objects.all()
        populaire=Livre.objects.all().order_by('-nb_vues')[:4]
        print(request.session['etudiant_cne'])
        all_tags = Tag.objects.all()
        return render(request, 'etudiant/home.html',{'books':all_books,'tags':all_tags,'populaire':populaire})
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


