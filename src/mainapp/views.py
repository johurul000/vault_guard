import random
import string
from django.shortcuts import render
from django.http import JsonResponse
from django.shortcuts import render, redirect, HttpResponse, get_object_or_404
from django.contrib.auth.models import User
from mainapp.models import LoginDetails, QuickPin, SecureNote, BankDetails, PaymentCards, CustomUser
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.hashers import make_password, check_password
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import get_user_model
from .aesutil import encrypt, decrypt, computeMasterKey
User = get_user_model()

def SignUpPage(request):
    if request.method =='POST':
        uname = request.POST.get('username')
        email = request.POST.get('email')
        pass1 = request.POST.get('password1')
        pass2 = request.POST.get('password2')
        my_user = User.objects.create_user(username=uname, email=email, password=pass1)
        my_user.save()
        return redirect('login')

    return render(request, 'signup.html')


def LogInPage(request):
    if request.method =='POST':
        username = request.POST.get('username')
        pass1 = request.POST.get('pass')
        user = authenticate(request, username=username, password=pass1)
        if user is not None:
            login(request,user)
            user = request.user
            if user.first_login:
                user.first_login = False
                user.save()
                return redirect('quickpin')
            else:
                return redirect('home')
        else:
            messages.error(request, 'Invalid username or password.')
    return render(request, 'login.html')


def LogOutPage(request):
    logout(request)
    return redirect('login')


@login_required(login_url='login')
def HomePage(request):
    # Fetching all the passwords to display
    user = request.user
    cusername = user.username


    passwords = LoginDetails.objects.filter(user=user)
    notes = SecureNote.objects.filter(user=user)
    banks = BankDetails.objects.filter(user=user)
    cards = PaymentCards.objects.filter(user=user)
    context = {
        'cusername' : cusername,
        'passwords': passwords,
        'notes' : notes,
        'banks' : banks,
        'cards' : cards
    }
    return render(request, 'home.html', context)


def generateUserSecret(length=10):
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k = length))

@login_required(login_url='login')
def AddQuickPin(request):
    if request.method =='POST':
        user = request.user

        # Check if the user already has a QuickPin
        if QuickPin.objects.filter(user=user).exists():
            # Update the existing QuickPin instance
            # quick_pin_instance = QuickPin.objects.get(user=user)
            # digits = request.POST.get('digit1') + request.POST.get('digit2') + request.POST.get('digit3') + request.POST.get('digit4')
            # quick_pin_instance.quick_pin = make_password(digits)
            # quick_pin_instance.user_secret = generateUserSecret()
            # quick_pin_instance.save()
            messages.error(request, 'QuickPin Already exists')
        else:
             # Create a new QuickPin instance
            digits = request.POST.get('digit1') + request.POST.get('digit2') + request.POST.get('digit3') + request.POST.get('digit4')
            quick_pin = make_password(digits)
            user_secret = generateUserSecret()
            
            quick_pin_instance = QuickPin(user=user, quick_pin = quick_pin, user_secret = user_secret)
            quick_pin_instance.save()
        return redirect('home')
    
    
    return render(request, 'quickpin.html')


def CheckPin(request):
    if request.method == 'POST':
        quick_pin = request.POST.get('quick_pin')
        print("part 01")
        user = request.user
        quick_pin_instance = QuickPin.objects.get(user=user)
        print("part 02")
        if check_password(quick_pin, quick_pin_instance.quick_pin):
            print("part 03")
            return JsonResponse({'success': True})
        else:
            print("part04")
            response_data = {
                    'success': False,
                    'error_message': 'Invalid Quick PIN',
                }
            return JsonResponse(response_data)





# PASSWORD


def AddPass(request):
    user= request.user
    cusername = user.username
    if request.method =='POST':
        websiteName = request.POST.get('websiteName')
        websiteUrl = request.POST.get('websiteUrl')
        username = request.POST.get('username')
        password = request.POST.get('password')
        notes = request.POST.get('notes')
        digits = request.POST.get('digit1') + request.POST.get('digit2') + request.POST.get('digit3') + request.POST.get('digit4')
        
        

        quick_pin_instance = QuickPin.objects.get(user=user)

        if check_password(digits, quick_pin_instance.quick_pin):

            mk = computeMasterKey(digits, quick_pin_instance.user_secret)
            print(mk)
            encyptedPass = encrypt(key=mk, source=password, keyType="bytes")
            print(encrypt)
            login_details_instance = LoginDetails(website_name=websiteName, website_url=websiteUrl, username=username, notes=notes, password=encyptedPass, user=user)
            login_details_instance.save() 
            return redirect('home')   
        else:

            context = {
                'websiteName': websiteName,
                'websiteUrl': websiteUrl,
                'username': username,
                'password': password,
                'notes': notes,
            }
            messages.error(request, 'Wrong Pin! Try Again.')
            return render(request, 'passadd.html', context)
    
    return render(request, 'passadd.html', {'cusername':cusername})


def EditPass(request, password_id):
    quick_pin = request.GET.get('quickPin', '')
    password = LoginDetails.objects.get(pk=password_id)
    user= request.user
    cusername = user.username
    quick_pin_instance = QuickPin.objects.get(user=user)
    mk = computeMasterKey(quick_pin, quick_pin_instance.user_secret)

    if request.method == 'POST':
        website_name = request.POST['website_name']
        website_url = request.POST['website_url']
        username = request.POST['username']
        password_value = request.POST['password']
        notes = request.POST['notes']

        encyptedPass = encrypt(key=mk, source=password_value, keyType="bytes")


        password.website_name = website_name
        password.website_url = website_url
        password.username = username
        password.password = encyptedPass
        password.notes = notes

        password.save()
        return redirect('home')
        
    decryptedPass = decrypt(key=mk, source=password.password, keyType="bytes")
    
    context = {
        'cusername':cusername,
        'password': password,
        'decryptedPass' : decryptedPass.decode()
    }
    return render(request, 'passedit.html', context)


def ViewPass(request, password_id):
    quick_pin = request.GET.get('quickPin', '')
    print(quick_pin)
    password = LoginDetails.objects.get(pk=password_id)
    print(password.password)
    user = request.user
    cusername = user.username
    quick_pin_instance = QuickPin.objects.get(user=user)
    mk = computeMasterKey(quick_pin, quick_pin_instance.user_secret)
    decryptedPass = decrypt(key=mk, source=password.password, keyType="bytes")
    print(decryptedPass)
    context = {
        'cusername' : cusername,
        'password': password,
        'decryptedPass' : decryptedPass.decode()
    }
    return render(request, 'passview.html', context)


def DeletePass(request, password_id):
    password = get_object_or_404(LoginDetails, pk=password_id)
    print("Got the pass")
    password.delete()
    return redirect('home')







# NOTES

def AddNote(request):
    user= request.user
    cusername = user.username
    if request.method =='POST':
        noteTitle = request.POST.get('noteTitle')
        noteContent = request.POST.get('noteContent')
        digits = request.POST.get('digit1') + request.POST.get('digit2') + request.POST.get('digit3') + request.POST.get('digit4')
        
        quick_pin_instance = QuickPin.objects.get(user=user)

        if check_password(digits, quick_pin_instance.quick_pin):

            mk = computeMasterKey(digits, quick_pin_instance.user_secret)
            print(mk)
            encyptedNote = encrypt(key=mk, source=noteContent, keyType="bytes")
            print(encrypt)
            note_instance =  SecureNote(note_title=noteTitle, note_content=encyptedNote, user=user)
            note_instance.save()
            return redirect('home')   
        else:

            context = {
                'noteTitle': noteTitle,
                'noteContent': noteContent,
            }
            messages.error(request, 'Wrong Pin! Try Again.')
            return render(request, 'noteadd.html', context)
        
    return render(request, 'noteadd.html', {'cusername':cusername})

def EditNote(request, note_id):
    quick_pin = request.GET.get('quickPin', '')
    notes = SecureNote.objects.get(pk=note_id)
    user= request.user
    cusername = user.username
    quick_pin_instance = QuickPin.objects.get(user=user)
    mk = computeMasterKey(quick_pin, quick_pin_instance.user_secret)

    if request.method == 'POST':

        note_title = request.POST['note_title']
        note_content = request.POST['note_content']

        encyptedNote = encrypt(key=mk, source=note_content, keyType="bytes")

        notes.note_title = note_title
        notes.note_content = encyptedNote
        notes.save()
        return redirect('home')
        
    decryptedNote = decrypt(key=mk, source=notes.note_content, keyType="bytes")
    
    context = {
        'cusername' : cusername,
        'notes': notes,
        'decryptedNote' : decryptedNote.decode()
    }
    return render(request, 'noteedit.html', context)
    


def ViewNote(request, note_id):
    quick_pin = request.GET.get('quickPin', '')
    notes = SecureNote.objects.get(pk=note_id)
    user = request.user
    cusername = user.username
    quick_pin_instance = QuickPin.objects.get(user=user)
    mk = computeMasterKey(quick_pin, quick_pin_instance.user_secret)
    decryptedNote = decrypt(key=mk, source=notes.note_content, keyType="bytes")
    context = {
        'cusername' : cusername,
        'notes': notes,
        'decryptedNote' : decryptedNote.decode()
    }
    return render(request, 'noteview.html', context)


def DeleteNote(request, note_id):
    note = get_object_or_404(SecureNote, pk=note_id)
    note.delete()
    return redirect('home')


# BANK DETAILS



def AddBank(request):
    user= request.user
    cusername = user.username
    if request.method =='POST':

        bank_name = request.POST.get('bank_name')
        account_holder_name = request.POST.get('account_holder_name')
        account_number = request.POST.get('account_number')
        ifsc_code = request.POST.get('ifsc_code')
        branch_address = request.POST.get('branch_address')
        notes = request.POST.get('notes')

        if len(account_number) >= 4:
            last_four_digits = account_number[-4:]
        else:
            last_four_digits = ''

        digits = request.POST.get('digit1') + request.POST.get('digit2') + request.POST.get('digit3') + request.POST.get('digit4')

        quick_pin_instance = QuickPin.objects.get(user=user)

        if check_password(digits, quick_pin_instance.quick_pin):

            mk = computeMasterKey(digits, quick_pin_instance.user_secret)
            print(mk)
            # encyptedNote = encrypt(key=mk, source=noteContent, keyType="bytes")
            print(encrypt)
            bank_instance =  BankDetails(
                bank_name=bank_name, 
                account_holder_name=account_holder_name, 
                account_number=account_number, 
                ifsc_code=ifsc_code, 
                branch_address=branch_address, 
                notes=notes, 
                ac_no_last_four=last_four_digits, 
                user=user
            )
            bank_instance.save()
            return redirect('home')   
        else:

            context = {
                'bank_name': bank_name,
                'account_holder_name': account_holder_name,
                'account_number': account_number,
                'ifsc_code': ifsc_code,
                'branch_address': branch_address,
                'notes': notes,
            }
            messages.error(request, 'Wrong Pin! Try Again.')
            return render(request, 'bankadd.html', context)
        
    return render(request, 'bankadd.html', {'cusername': cusername})



def EditBank(request, bank_id):
    quick_pin = request.GET.get('quickPin', '')
    bank = BankDetails.objects.get(pk=bank_id)
    user= request.user
    cusername = user.username
    quick_pin_instance = QuickPin.objects.get(user=user)
    mk = computeMasterKey(quick_pin, quick_pin_instance.user_secret)

    if request.method == 'POST':

        bank_name = request.POST['bank_name']
        account_holder_name = request.POST['account_holder_name']
        account_number = request.POST['account_number']
        ifsc_code = request.POST['ifsc_code']
        branch_address = request.POST['branch_address']
        notes = request.POST['notes']

        if len(account_number) >= 4:
            last_four_digits = account_number[-4:]
        else:
            last_four_digits = 'Null'


        bank.bank_name = bank_name
        bank.account_holder_name = account_holder_name
        bank.account_number = account_number
        bank.ifsc_code = ifsc_code
        bank.branch_address = branch_address
        bank.notes = notes
        bank.ac_no_last_four =last_four_digits
        bank.save()
        return redirect('home')
        
    
    context = {
        'cusername' : cusername,
        'bank': bank,
    }
    return render(request, 'bankedit.html', context)




def ViewBank(request, bank_id):
    quick_pin = request.GET.get('quickPin', '')
    bank = BankDetails.objects.get(pk=bank_id)
    user = request.user
    cusername = user.username
    quick_pin_instance = QuickPin.objects.get(user=user)
    mk = computeMasterKey(quick_pin, quick_pin_instance.user_secret)
    context = {
        'cusername' : cusername,
        'bank': bank,
    }
    return render(request, 'bankview.html', context)

def DeleteBank(request, bank_id):
    bank = get_object_or_404(BankDetails, pk=bank_id)
    bank.delete()
    return redirect('home')



# PAYMENT CARDS
def AddCard(request):
    user= request.user
    cusername = user.username
    if request.method =='POST':

        card_holder_name = request.POST.get('card_holder_name')
        card_type = request.POST.get('card_type')
        card_number = request.POST.get('card_number')
        cvv = request.POST.get('cvv')
        expiration_month = request.POST.get('expiration_month')
        expiration_year = request.POST.get('expiration_year')
        notes = request.POST.get('notes')
        print(expiration_month)
        print(expiration_year)


        if len(card_number) >= 4:
            last_four_digits = card_number[-4:]
        else:
            last_four_digits = ''

        digits = request.POST.get('digit1') + request.POST.get('digit2') + request.POST.get('digit3') + request.POST.get('digit4')
        
        quick_pin_instance = QuickPin.objects.get(user=user)

        if check_password(digits, quick_pin_instance.quick_pin):

            mk = computeMasterKey(digits, quick_pin_instance.user_secret)
            print(mk)
            encyptedCardNumber = encrypt(key=mk, source=card_number, keyType="bytes")
            encyptedCvv = encrypt(key=mk, source=cvv, keyType="bytes")
            encyptedExpMonth = encrypt(key=mk, source=expiration_month, keyType="bytes")
            encyptedExpYr = encrypt(key=mk, source=expiration_year, keyType="bytes")
            card_instance =  PaymentCards(
                card_holder_name=card_holder_name,
                card_type=card_type,
                card_number=encyptedCardNumber,
                card_no_last_four= last_four_digits,
                cvv=encyptedCvv,
                expiration_month=encyptedExpMonth,
                expiration_year=encyptedExpYr,
                notes=notes,
                user=user
            )
            card_instance.save()
            return redirect('home')   
        else:

            context = {
                'card_holder_name': card_holder_name,
                'card_type': card_type,
                'card_number': card_number,
                'notes': notes,
            }
            messages.error(request, 'Wrong Pin! Try Again.')
            return render(request, 'cardadd.html', context)
        
    return render(request, 'cardadd.html', {'cusername':cusername})



def EditCard(request, card_id):
    quick_pin = request.GET.get('quickPin', '')
    cards = PaymentCards.objects.get(pk=card_id)
    user= request.user
    cusername = user.username
    quick_pin_instance = QuickPin.objects.get(user=user)
    mk = computeMasterKey(quick_pin, quick_pin_instance.user_secret)

    if request.method == 'POST':

        card_holder_name = request.POST['card_holder_name']
        card_type = request.POST['card_type']
        card_number = request.POST['card_number']
        cvv = request.POST['cvv']
        expiration_month = request.POST['expiration_month']
        expiration_year = request.POST['expiration_year']
        notes = request.POST['notes']

        if len(card_number) >= 4:
            last_four_digits = card_number[-4:]
        else:
            last_four_digits = ''

        encyptedCardNumber = encrypt(key=mk, source=card_number, keyType="bytes")
        encyptedCvv = encrypt(key=mk, source=cvv, keyType="bytes")
        encyptedExpMonth = encrypt(key=mk, source=expiration_month, keyType="bytes")
        encyptedExpYr = encrypt(key=mk, source=expiration_year, keyType="bytes")

        cards.card_holder_name = card_holder_name
        cards.card_type = card_type
        cards.card_number = encyptedCardNumber
        cards.card_no_last_four = last_four_digits
        cards.cvv = encyptedCvv
        cards.expiration_month = encyptedExpMonth
        cards.expiration_year = encyptedExpYr
        cards.notes = notes
        cards.save()
        return redirect('home')
        
    decryptedCardNumber = decrypt(key=mk, source=cards.card_number, keyType="bytes")
    decryptedCvv = decrypt(key=mk, source=cards.cvv, keyType="bytes")
    decryptedExpMonth = decrypt(key=mk, source=cards.expiration_month, keyType="bytes")
    decryptedExpYear = decrypt(key=mk, source=cards.expiration_year, keyType="bytes")
    
    context = {
        'cusername': cusername,
        'cards': cards,
        'decryptedCardNumber' : decryptedCardNumber.decode(),
        'decryptedCvv' : decryptedCvv.decode(),
        'decryptedExpMonth' : decryptedExpMonth.decode(),
        'decryptedExpYear' : decryptedExpYear.decode(),
    }
    return render(request, 'cardedit.html', context)




def ViewCard(request, card_id):
    quick_pin = request.GET.get('quickPin', '')
    cards = PaymentCards.objects.get(pk=card_id)
    user = request.user
    cusername = user.username
    quick_pin_instance = QuickPin.objects.get(user=user)
    mk = computeMasterKey(quick_pin, quick_pin_instance.user_secret)
    decryptedCardNumber = decrypt(key=mk, source=cards.card_number, keyType="bytes")
    decryptedCvv = decrypt(key=mk, source=cards.cvv, keyType="bytes")
    decryptedExpMonth = decrypt(key=mk, source=cards.expiration_month, keyType="bytes")
    decryptedExpYear = decrypt(key=mk, source=cards.expiration_year, keyType="bytes")
    
    context = {
        'cusername' : cusername,
        'cards': cards,
        'decryptedCardNumber' : decryptedCardNumber.decode(),
        'decryptedCvv' : decryptedCvv.decode(),
        'decryptedExpMonth' : decryptedExpMonth.decode(),
        'decryptedExpYear' : decryptedExpYear.decode(),
    }
    return render(request, 'cardview.html', context)



def DeleteCard(request, card_id):
    card = get_object_or_404(PaymentCards, pk=card_id)
    card.delete()
    return redirect('home')







@login_required(login_url='login')
def ListPass(request):
    user = request.user
    cusername = user.username
    passwords = LoginDetails.objects.filter(user=user)
    context = {
        'cusername' : cusername,
        'passwords': passwords,
    }
    return render(request, 'listpass.html', context)

def ListNote(request):
    user = request.user
    cusername = user.username
    notes = SecureNote.objects.filter(user=user)
    context = {
        'cusername' : cusername,
        'notes' : notes,
    }
    return render(request, 'listnote.html', context)


def ListBank(request):
    user = request.user
    cusername = user.username
    banks = BankDetails.objects.filter(user=user)
    context = {
        'cusername' : cusername,
        'banks' : banks,
    }
    return render(request, 'listbank.html', context)

def ListCard(request):
    user = request.user
    cusername = user.username
    cards = PaymentCards.objects.filter(user=user)
    context = {
        'cusername' : cusername,
        'cards' : cards
    }
    return render(request, 'listcard.html', context)





def UpdateProfile(request):
    user = request.user
    cusername = user.username
    user_instance = CustomUser.objects.get(id=user.id)
    if request.method == 'POST':

        username = request.POST['username']
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST['email']

        print("part01")
        user_instance.username = username
        user_instance.first_name = first_name
        user_instance.last_name = last_name
        user_instance.email = email
        print("part02")
        user_instance.save()
        return redirect('home')
        
    print(user_instance.username)
    context = {
        'user_instance' : user_instance,
        'cusername' : cusername
    }
    return render(request, 'updateprofile.html', context)

def ViewProfile(request):
    user = request.user 
    cusername = user.username
    user_instance = CustomUser.objects.get(id=user.id)
    context = {
        'user_instance' : user_instance,
        'cusername' : cusername
    }
    return render(request, 'viewprofile.html', context)


def UpdatePassword(request):
    user = request.user
    cusername = user.username

    if request.method =='POST':
        username = user.username
        password = request.POST.get('password')
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')
        user_instance = authenticate(request, username=username, password=password)
        if user_instance is not None:
            if new_password == confirm_password:
                user_instance.set_password(new_password)
                user_instance.save()
                return redirect('home')
            else:
                messages.error(request, 'New Passwords Does not match With Confirm password!')

        else:
            messages.error(request, 'Invalid Password!')
    return render(request, 'updatepassword.html', {'cusername': cusername})

def UpdateQuickpin(request):
    if request.method =='POST':
        old_pin = request.POST.get('digit1') + request.POST.get('digit2') + request.POST.get('digit3') + request.POST.get('digit4')
        new_pin = request.POST.get('digit5') + request.POST.get('digit6') + request.POST.get('digit7') + request.POST.get('digit8')
        confirm_pin = request.POST.get('digit9') + request.POST.get('digit10') + request.POST.get('digit11') + request.POST.get('digit12')

        user = request.user

        quick_pin_instance = QuickPin.objects.get(user=user)
        if check_password(old_pin, quick_pin_instance.quick_pin):
            if new_pin == confirm_pin:

                new_user_secret = generateUserSecret()
                new_quick_pin = make_password(new_pin)

                ReEncryptPass(user=user, old_pin=old_pin, old_user_secret=quick_pin_instance.user_secret, new_pin=new_pin, new_user_secret=new_user_secret)
                ReEncryptNote(user=user, old_pin=old_pin, old_user_secret=quick_pin_instance.user_secret, new_pin=new_pin, new_user_secret=new_user_secret)
                ReEncryptCard(user=user, old_pin=old_pin, old_user_secret=quick_pin_instance.user_secret, new_pin=new_pin, new_user_secret=new_user_secret)
                

                quick_pin_instance.quick_pin = new_quick_pin
                quick_pin_instance.user_secret = new_user_secret
                quick_pin_instance.save()
                return redirect('home')
            else:
                messages.error(request, 'New Pin And Confirm Pin Does not Match!!')
        else:
            messages.error(request, 'Wrong Pin! Try Again')
    
    return render(request, 'updatequickpin.html')


def ReEncryptPass(user, old_pin, old_user_secret, new_pin, new_user_secret):
 
    old_mk = computeMasterKey(old_pin, old_user_secret)
    new_mk = computeMasterKey(new_pin, new_user_secret)
    passwords = LoginDetails.objects.filter(user=user)
    if passwords.exists():
        for pas in passwords:

            decryptedPass = decrypt(key=old_mk, source=pas.password, keyType="bytes").decode()

            encryptedPass = encrypt(key=new_mk, source=decryptedPass, keyType="bytes")

            pas.password = encryptedPass
            pas.save()



def ReEncryptNote(user, old_pin, old_user_secret, new_pin, new_user_secret):
    old_mk = computeMasterKey(old_pin, old_user_secret)
    new_mk = computeMasterKey(new_pin, new_user_secret)
    notes = SecureNote.objects.filter(user=user)
    if notes.exists():
        for note in notes:

            decryptedNote = decrypt(key=old_mk, source=note.note_content, keyType="bytes").decode()

            encryptedNote = encrypt(key=new_mk, source=decryptedNote, keyType="bytes")

            note.note_content = encryptedNote
            note.save()



def ReEncryptCard(user, old_pin, old_user_secret, new_pin, new_user_secret):
    old_mk = computeMasterKey(old_pin, old_user_secret)
    new_mk = computeMasterKey(new_pin, new_user_secret)
    cards = PaymentCards.objects.filter(user=user)
    if cards.exists():
        for card in cards:

            decryptedCardNumber = decrypt(key=old_mk, source=card.card_number, keyType="bytes").decode()
            decryptedCvv = decrypt(key=old_mk, source=card.cvv, keyType="bytes").decode()
            decryptedExpMonth = decrypt(key=old_mk, source=card.expiration_month, keyType="bytes").decode()
            decryptedExpYear = decrypt(key=old_mk, source=card.expiration_year, keyType="bytes").decode()

            encyptedCardNumber = encrypt(key=new_mk, source=decryptedCardNumber, keyType="bytes")
            encyptedCvv = encrypt(key=new_mk, source=decryptedCvv, keyType="bytes")
            encyptedExpMonth = encrypt(key=new_mk, source=decryptedExpMonth, keyType="bytes")
            encyptedExpYr = encrypt(key=new_mk, source=decryptedExpYear, keyType="bytes")

            card.card_number = encyptedCardNumber
            card.cvv = encyptedCvv
            card.expiration_month = encyptedExpMonth
            card.expiration_year = encyptedExpYr
            card.save()
