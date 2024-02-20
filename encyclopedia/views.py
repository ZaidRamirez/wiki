from markdown2 import Markdown
from django.shortcuts import render
from django.views.decorators.csrf import csrf_protect
import random

from . import util

def converter(title):
    markdowner = Markdown()
    content = util.get_entry(title)
    if content is None:
        return None
    else:
        return markdowner.convert(content)

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def entry(request, title):
    search = converter(title)
    if search == None:
        return render(request, "encyclopedia/error.html", {
            "title": "The page doesn't exist",
            "error": "Sorry, the page you're looking for isn't available at the moment. Please check the name and make sure it is spelled correctly"
        })
    else:
        return render(request, "encyclopedia/search.html",{
            "title": title,
            "content": search
            })
    
def search(request):
    if request.method == "POST":
        form = request.POST['q']
        content = converter(form)
        if content is not None:
            return render(request, "encyclopedia/search.html", {
                "title": form,
                "content": content
            })
        else:
            entries = util.list_entries()
            results = []
            for entry in entries:
                if form.lower() in entry.lower():
                    results.append(entry)
            return render(request, "encyclopedia/results.html", {
                "results" : results
            })
        
def new(request):
    if request.method == 'GET':
        return render(request, "encyclopedia/new.html",)
    else:
        title = request.POST['title']
        content = request.POST['content']
        titleExist = util.get_entry(title)
        if titleExist is not None:
            return render(request, "encyclopedia/error.html", {
                "title": "",
                "error": "The page already exist"
            })
        else:
            util.save_entry(title, content)
            html_content = converter(title)
            return render(request, "encyclopedia/search.html", {
                "title": title,
                "content": html_content
            })
        
def edit(request):
    if request.method == 'POST':
        title = request.POST['title']
        content = util.get_entry(title)
        return render(request, "encyclopedia/edit.html",{
            "title": title,
            "content": content
        })

def save_edit(request):
    if request.method == 'POST':
        title = request.POST['title']
        content = request.POST['content']
        util.save_entry(title, content)
        html_content = converter(title)
        return render(request, "encyclopedia/search.html", {
            "title": title,
            "content": html_content
        })
    
def rand(request):
    entry = random.choice(util.list_entries())
    content = converter(entry)
    return render(request, "encyclopedia/search.html", {
            "title": entry,
            "content": content
        })
