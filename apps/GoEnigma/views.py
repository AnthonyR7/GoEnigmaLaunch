from __future__ import unicode_literals
from django.shortcuts import render, HttpResponse, redirect
from .models import *
from django.shortcuts import render, redirect, HttpResponse
from django.contrib import messages
from django.urls import reverse
from django.contrib.auth.hashers import make_password
from django.core.exceptions import ObjectDoesNotExist
from datetime import date, datetime
from time import strptime

def index(request):
    userBio = Bio.objects.all()
    for bio in userBio:
        print(bio.title)    
        content = {
            "title" : bio.title,
            "qA" : bio.quoteA,
            "qB" : bio.quoteB,
            "desc" : bio.desc,
            "authorA" : bio.authorA,
            "authorB" : bio.authorB
        }
        print("My desc", bio.desc)
    return render(request, "GoEnigma/EMusic.html", content)

def loginPg(request):
    return render(request, "GoEnigma/loginForm.html")


def login(request):
    errors = User.objects.log_validator(request.POST)
    if len(errors):
        for words in errors:
            messages.error(request, words)
    else:
        conformed_user = User.objects.get(email = request.POST['confirm_email'])
        request.session['client'] = {
            "id" : conformed_user.id
        }
        return redirect("/dashboard")
    return redirect('/loginPg')

def logOut(request):
    # if key not in session uses except
    try:
        del request.session['client']
        # print ("Key will be del, redirect activated")
        return redirect('/loginPg')
    except:
        # print ("except was hit")
        return redirect('/loginPg')
    return redirect('/loginPg')

def regPg(request):
    return render(request, "GoEnigma/register.html")

def register(request):
    errors = User.objects.reg_validator(request.POST)
    if len(errors):
        for words in errors:
            messages.error(request, words)
        return redirect("/registerPg")
    else:
        great =[]
        great.append("Successfully Registered, Thank you")
        hash1 = make_password(request.POST['password'], salt = None, hasher = 'default')
        # to prevent anyone from making more users
        allUsers = User.objects.all()
        print(len(allUsers))
        if len(allUsers) > 3:
            messages.error(request, "Unable to add any more users")
            redirect("/registerPg")
            
        else:
            user = User.objects.create(
                name = request.POST['name'],
                password = hash1, 
                email = request.POST["email"]
                )
            Bio.objects.create(userData = user)
            for good in great:
                messages.success(request, good)
    return render(request, "GoEnigma/loginForm.html")

# def logOut(request):
#     try:
#         del request.session['client']
#         print ("Key will be del, redirect activated")
#         return redirect('/')
#     except:
#         print ("except was hit")
#         return redirect('/')
#     return redirect('/login')

def dash(request):
    try:
        _id = request.session['client']['id']
    except:
        return redirect("/loginPg")
        
    userBio = Bio.objects.get(userData = User.objects.get(id = request.session['client']['id']))
    print(userBio.title, "look here yo!!!!!!!!!!!!")    
    content = {
        "title" : userBio.title,
        "qA" : userBio.quoteA,
        "qB" : userBio.quoteB,
        "desc" : userBio.desc,
        "authorA" : userBio.authorA,
        "authorB" : userBio.authorB
    }

    return render(request, "GoEnigma/dashboard.html", content)

    
def checkAll(bioA, bioB, bioC,bioD):
    result = ""
    if len(str(bioA)) != 0 and len(str(bioB)) != 0 and len(str(bioC)) != 0 and len(str(bioD)) != 0:
        result = True
    else:
        result = False
    return result

def processInput(request):
    note = []
    userBio = Bio.objects.get(userData = User.objects.get(id = request.session['client']['id']))
    if checkAll(request.POST["title"], request.POST["qA"], request.POST["qB"], request.POST["desc"]) == True:
        userBio.title = request.POST["title"]
        userBio.quoteA = request.POST["qA"]
        userBio.quoteB = request.POST["qB"]
        userBio.desc = request.POST["desc"]
        userBio.save()
    
    else:
        if request.POST["title"]:
            if len(str(request.POST["title"])) < 15:
                userBio.title = request.POST["title"]
            else:
                note.append("Title must be less then 15 characters")
                

        if request.POST["authorA"]:
            if len(str(request.POST["authorA"])) < 15:
                userBio.authorA = request.POST["authorA"]
            else:
                note.append("Author A needs to be less then 15 Charaters")

        if request.POST["authorB"]:
            if len(str(request.POST["authorB"])) < 15:
                userBio.authorB = request.POST["authorB"]
            else:
                note.append("Author B needs to be less then 15 Charaters")

        if request.POST["qA"]:
            print("quoute A here")
            if len(str(request.POST["qA"])) < 15:
                userBio.quoteA = request.POST["qA"]
            else:
                note.append("Quote A needs to be less than 15 Characters")
            
        if request.POST["qB"]:
            print("qoute B here")
            if len(str(request.POST["qB"])) < 15:
                userBio.quoteB = request.POST["qB"]
            else:
                note.append("Quote B needs to be less than 15 Characters")

        if request.POST["desc"]:
            if len(str(request.POST["desc"])) < 15:
                userBio.desc = request.POST["desc"]
            else:
                note.append("Description needs to be less than 15 Characters")
        userBio.save()
    if len(note) > 0:
        print(note)
        for words in note:
            messages.error(request, words)
    return redirect("/dashboard")
