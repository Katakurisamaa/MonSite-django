from multiprocessing import context
from django.shortcuts import render, redirect, get_object_or_404

from commandes.models import Order, OrderProduct
from .models import Account, UserProfile
from .forms import RegistrationForm, UserForm, UserProfileForm
from django.contrib import messages, auth
from django.contrib.auth.decorators import login_required 
from django.http import HttpResponse
# Verification email
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage


from cart import models, views
import requests

def register_view(request):
    if request.method == "POST":
        form = RegistrationForm(request.POST)
        if form.is_valid():
            first_name   = form.cleaned_data['first_name'] # prénom
            last_name    = form.cleaned_data['last_name'] # nom
            phone_number = form.cleaned_data['phone_number']
            email        = form.cleaned_data['email']
            password     = form.cleaned_data['password']
            username     = email.split("@")[0]
            user         = Account.objects.create_user(first_name=first_name, last_name=last_name, email=email, username=username, password=password)
            user.phone_number = phone_number
            user.save()

            # Création automatique du profil d'utilisateur
            profile = UserProfile()
            profile.user_id = user.id
            profile.profile_picture = 'default/default-user.png'
            profile.save()

            current_site = get_current_site(request)
            mail_subject = "Veuillez activer votre compte s'il vous plaît"
            message = render_to_string('comptes/compte_verification_email.html', {
                'user': user,
                'domain': current_site,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': default_token_generator.make_token(user),
            })
            to_email = email
            send_email = EmailMessage(mail_subject, message, to=[to_email])
            send_email.send()

            # messages.success(request, 'Merci pour votre inscription chez nous. Nous avons envoyé une email de vérification à votre adresse email. Veuillez vérifier.')
            
            return redirect('/comptes/login/?command=verification&email='+email)
    else:
        form = RegistrationForm()
    context = {
        'form':form,
    }
    return render(request,'comptes/register.html', context)

def login_view(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']

        user = auth.authenticate(email=email, password=password)

        if user is not None:
            try:
                cart = models.Cart.objects.get(cart_id=views._cart_id(request) )
                is_cart_item_exists = models.CartItem.objects.filter(cart=cart).exists()
                if is_cart_item_exists:
                    cart_item = models.CartItem.objects.filter(cart=cart)
                    product_variation = []

                    # Getting the product variation by cart id
                    for item in cart_item:
                        variation = item.variations.all()
                        product_variation.append(list(variation))

                    # Get the cart item from the user to access his product variation
                    cart_item = models.CartItem.objects.filter(user=user)
                    ex_var_list = []  # empty existing variation list
                    id = []           # empty id
                    for item in cart_item:
                        existing_variation = item.variations.all()
                        ex_var_list.append(list(existing_variation))
                        id.append(item.id)
                    
                    for pr in product_variation:
                        if pr in ex_var_list:
                            index = ex_var_list.index(pr)
                            item_id = id[index]
                            item = models.CartItem.objects.get(id=item_id)
                            item.quantity += 1
                            item.user = user
                            item.save()
                        else:
                            cart_item = models.CartItem.objects.filter(cart=cart)
                            for item in cart_item:
                                item.user = user
                                item.save()
            except:
                pass
            auth.login(request, user)
            # messages.success(request, "Vous êtes connecté.")
            url = request.META.get('HTTP_REFERER')
            try:
                query = requests.utils.urlparse(url).query
                params = dict(x.split('=') for x in query.split('&'))
                if 'next' in params:
                    nextPage = params['next']
                    return redirect(nextPage)
            except:
                return redirect('accueil')
        else:
            messages.error(request, 'informations d’identification de connexion non valides')
            return redirect('login')
    return render(request, 'comptes/login.html')

@login_required(login_url='login')
def logout_view(request):
    auth.logout(request)
    messages.success(request, "Vous êtes déconnecté")
    return redirect('login')

def activate_view(request,uidb64,token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = Account._default_manager.get(pk=uid)
    except(TypeError, ValueError, OverflowError, Account.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(request, 'Félicitation! Votre compte est activé.')
        return redirect('login')
    else:
        messages.error(request, "lien d'activation invalide")
        return redirect('register')

@login_required(login_url='login')
def dashboard_view(request):
    orders = Order.objects.order_by('-created_at').filter(user_id=request.user.id, is_ordered=True)
    orders_count = orders.count()
    userprofile = UserProfile.objects.get(user_id=request.user.id)
    context={
        'orders_count': orders_count,
        'orders': orders,
        'userprofile':userprofile,
    }
    return render(request, 'comptes/dashboard.html', context)

def forgotPassword_view(request):
    if request.method == 'POST':
        email = request.POST['email']
        if Account.objects.filter(email=email).exists():
            user = Account.objects.get(email__exact=email)

            # Reset password email
            current_site = get_current_site(request)
            mail_subject = 'Réinitialiser votre mot de passe.'
            message = render_to_string('comptes/reset_password_email.html', {
                'user': user,
                'domain': current_site,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': default_token_generator.make_token(user),
            })
            to_email = email
            send_email = EmailMessage(mail_subject, message, to=[to_email])
            send_email.send()

            messages.success(request, 'Une e-mail de réinitialisation de votre passe vous a été envoyé à votre adresse e-mail.')
            return redirect('login')
        else:
            messages.error(request, 'Ce compte n’existe pas!')
            return redirect('forgotPassword')
    return render(request, 'comptes/forgotPassword.html')

def resetpassword_validate_view(request,uidb64,token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = Account._default_manager.get(pk=uid)
    except(TypeError, ValueError, OverflowError, Account.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        request.session['uid'] = uid
        messages.success(request, 'Veuillez réinitialiser votre mot de passe')
        return redirect('resetPassword')
    else:
        messages.error(request, 'Ce lien a expiré !')
        return redirect('login')

def resetPassword_view(request):
    if request.method == 'POST':
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        if password == confirm_password:
            uid = request.session.get('uid')
            user = Account.objects.get(pk=uid)
            user.set_password(password)
            user.save()
            messages.success(request, 'Mot de passe réinitialisé avec succès!')
            return redirect('login')
        else:
            messages.error(request, 'Le mot de passe ne correspond pas.')
            return redirect('resetPassword')
    else:
        return render(request, 'comptes/resetPassword.html')


def my_orders_view(request):
    orders = Order.objects.order_by('-created_at').filter(user_id=request.user.id, is_ordered=True)
    context={
        'orders': orders,
    }
    return render(request, 'comptes/my_orders.html', context)

def edit_profile_view(request):
    userprofile = get_object_or_404(UserProfile, user=request.user)
    if request.method == 'POST':
        user_form = UserForm(request.POST, instance=request.user)
        profile_form = UserProfileForm(request.POST, request.FILES, instance=userprofile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Votre photo a été téléchargé.')
            return redirect('edit_profile')
    else:
        user_form = UserForm(instance=request.user)
        profile_form = UserProfileForm(instance=userprofile)
    context = {
        'user_form': user_form,
        'profile_form': profile_form,
        'userprofile': userprofile,
    }
    return render(request, 'comptes/edit_profile.html', context)


@login_required(login_url='login')
def change_password_view(request):
    if request.method == 'POST':
        current_password = request.POST['current_password']
        new_password = request.POST['new_password']
        confirm_password = request.POST['confirm_password']

        user = Account.objects.get(username__exact=request.user.username)

        if new_password == confirm_password:
            success = user.check_password(current_password)
            if success:
                user.set_password(new_password)
                user.save()
                # auth.logout(request)
                messages.success(request, 'Mot de passe mis à jour avec succès :).')
                return redirect('change_password')
            else:
                messages.error(request, 'Veuillez bien encoder votre mot de passe actuel :/')
                return redirect('change_password')
        else:
            messages.error(request, 'Le mot de passe ne correspond pas :/!')
            return redirect('change_password')
    return render(request, 'comptes/change_password.html')

def order_detail_view(request, order_id):
    order_detail = OrderProduct.objects.filter(order__order_number=order_id)
    order = Order.objects.get(order_number=order_id)
    subtotal = 0
    for i in order_detail:
        subtotal += i.product_price * i.quantity

    context = {
        'order_detail': order_detail,
        'order': order,
        'subtotal': subtotal,
    }
    return render(request, 'comptes/order_detail.html', context)