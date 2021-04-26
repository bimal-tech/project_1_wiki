import markdown2
import secrets

from django.shortcuts import render
from django.http import HttpResponseRedirect
from django import forms
from django.urls import reverse

from . import util
from markdown2 import Markdown


class Addnewpage(forms.Form):
    title = forms.CharField(label="Entry title", widget=forms.TextInput(attrs={'class': 'form-control col-md-8 col-lg-8'}))
    content = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control col-md-8 col-lg-10', 'rows': 10}))
    edit = forms.BooleanField(initial=False, widget=forms.HiddenInput(), required=False)


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })


def add(request, entry):
    markdowner = Markdown()
    entryPage = util.get_entry(entry)
    if entryPage is None:
        return render(request, "encyclopedia/nonexisting.html", {
            "addTitle": entry,
            "error_link": "/",
            "messege1": "Unexpected error due to invalid contents.",
            
            
        })
    else:
        return render(request, "encyclopedia/add.html", {
            "entry": markdowner.convert(entryPage),
            "addTitle": entry
        })


def newpage(request):
    if request.method == "POST":
        form = Addnewpage(request.POST)
        if form.is_valid():
            title = form.cleaned_data["title"]
            content = form.cleaned_data["content"]
            if(util.get_entry(title) is None ):
                util.save_entry(title,content)
            elif(form.cleaned_data["edit"] is True):
                util.save_entry(title, content)
                return HttpResponseRedirect(reverse("add", kwargs={'entry': title}))


            else:
                return render(request, "encyclopedia/nonexisting.html", {
                "form": form,
                "existing": True,
                "entry": title,
                "error_link": "/newpage",
                "messege1": "This entry already exists.",
                
                })

            return render(request, "encyclopedia/newpage.html", {
             "form": Addnewpage(),
             "existing": False
            })

    else:
        return render(request,"encyclopedia/newpage.html", {
            "form": Addnewpage(),
            "existing": False
        })

def edit (request,entry):
    entryPage = util.get_entry(entry)
    if entryPage is None:
        return render(request, "encyclopedia/nonexisting.html", {
            "addTitle": entry,

        })
    else:
        form = Addnewpage()
        form.fields["title"].initial = entry     
        form.fields["title"].widget = forms.HiddenInput()
        form.fields["content"].initial = entryPage
        form.fields["edit"].initial = True
        return render(request, "encyclopedia/newpage.html", {
            "form": form,
            "edit": form.fields["edit"].initial,
            "entryTitle": form.fields["title"].initial

        })        

def random(request):
    entries = util.list_entries()
    randomEntry = secrets.choice(entries)
    return HttpResponseRedirect(reverse('add', kwargs={'entry': randomEntry}))



def search(request):
    value = request.GET.get('q','')
    if(util.get_entry(value) is not None):
        return HttpResponseRedirect(reverse("add", kwargs={'entry': value }))
    else:
        subStringEntries = []
        for entry in util.list_entries():
            if value.upper() in entry.upper():
                subStringEntries.append(entry)

        if subStringEntries==[]:
            return render(request, "encyclopedia/index.html", {
        "entries": subStringEntries,
        "search": True,
        "value": value,
        "notfound":True
                })
        
        else:
            return render(request, "encyclopedia/index.html", {
        "entries": subStringEntries,
        "search": True,
        "value": value,
        "notfound":False

                })
           

        
