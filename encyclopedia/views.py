from django.shortcuts import render
from django.http import HttpResponse, HttpRequest, HttpResponseRedirect
from django import forms
from django.contrib import messages 

from . import util

import re
from markdown2 import Markdown
import random

class NewPageForm(forms.Form):
    page = forms.CharField(label="Title")


def search_result(oldrequest):
    entries = util.list_entries()
    value = oldrequest.POST.get('q')
    request = HttpRequest()
    request.META = oldrequest.META
    request.method = 'GET'
    results = []
    for entry in entries:
        if value != None:
            if value.lower() == entry.lower():
                return HttpResponseRedirect(f'/wiki/{entry}')
            if entry.lower().find(value.lower()) != -1:
                results.append(entry)
    return render(request, "encyclopedia/search_result.html", {
        "results" : results
    })

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })


def template(request, entry):
    content = util.get_entry(entry)
    if content:
        return render(request, "encyclopedia/entry.html",{
            "title" : entry,
            "content": Markdown().convert(content)
        })
    else:
        return HttpResponse("Page not found (404)")

def create(request):
    if request.method == 'POST':
        form = NewPageForm(request.POST)
        if form.is_valid():
            entries = util.list_entries()
            entries = [entry.lower() for entry in entries]
            title = form.cleaned_data["page"]
            if title.lower() in entries:
                return render(request,"encyclopedia/create.html", {
        "form" : NewPageForm(),
        "error" : True
    })
            content = request.POST.get('content')
            util.save_entry(title, content)
            return HttpResponseRedirect(f"/wiki/{title}")
    return render(request,"encyclopedia/create.html", {
        "form" : NewPageForm(),
        "error" : False
    })


def edit(request, entry):
    if request.method == "POST":
        content = request.POST.get('content')
        util.save_entry(entry, content)
        return HttpResponseRedirect(f"/wiki/{entry}")
    return render(request,"encyclopedia/edit.html", {
        "title" : entry,
        "content" : util.get_entry(entry)
    })

def ran_entry(request):
    entries = util.list_entries()
    random_entry = random.choice(entries)
    return HttpResponseRedirect(f'/wiki/{random_entry}')


