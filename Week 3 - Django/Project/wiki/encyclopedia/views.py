from django.shortcuts import render,redirect
from django.views import View
from .util import get_entry, list_entries,save_entry,delete_item
import markdown2
from django.http import HttpResponse
from .forms import EntryForm
import random

class index(View):
    def get(self, request):
        entries = list_entries()
        search_item = request.GET.get('q')
        if search_item:
            search_results = [entry for entry in entries if search_item.lower() in entry.lower() ]
            if len(search_results) == 0:
                return render(request, "encyclopedia/index.html", {"entries": search_results, 'title': 'Search results', 'message':True})
            return render(request, "encyclopedia/index.html", {"entries": search_results, 'title': 'Search results'})
        return render(request, "encyclopedia/index.html", {
        "entries": entries,
        "title": 'All Pages'

    })

class entry_page(View):
    def get(self, request, *args, **kwargs):
        title = kwargs.get('title')
        entry = get_entry(title)
        if entry:
            entry = markdown2.markdown(entry)
            return render(request, 'encyclopedia/entry_page.html', {'title': title,'content': entry })
        else:
            return render(request, 'encyclopedia/error_page.html')

class create_entry(View):
    def get(self, request):
        form = EntryForm()
        return render(request, 'encyclopedia/create_entry.html', {'form': form })
    def post(self, request):
        form = EntryForm(request.POST)
        if form.is_valid():
            entry_title = form.cleaned_data["title"]
            entry_content = form.cleaned_data["content"]
            if not get_entry(entry_title):
                save_entry(entry_title, entry_content)
                return redirect('entry_page', entry_title)
            else:
                return render(request,'encyclopedia/create_entry.html', {'form': form, 'message': 'There is an entry with the same title.' })
        else:
            return render(request,'encyclopedia/create_entry.html', {'form': form })
            

class update_entry(View):
    def get(self, request, *args, **kwargs):
        title = kwargs.get('title')
        entry_content = get_entry(title)
        form = EntryForm(initial={'title':title, 'content': entry_content})
        return render(request, 'encyclopedia/update_entry.html', {'form': form })
    
    def post(self, request, *args, **kwargs):
        title = kwargs.get('title')
        form = EntryForm(request.POST)
        if form.is_valid():
            entry_title = form.cleaned_data["title"]
            entry_content = form.cleaned_data["content"]
            save_entry(entry_title, entry_content)
            return redirect('entry_page', entry_title)
        else:
            return render(request,'encyclopedia/create_entry.html', {'form': form , 'message': 'Invalid form data'})

class random_entry(View):
    def get(self, request):
        entries = list_entries()
        entry_title = random.choice(entries)
        entry = get_entry(entry_title)
        entry = markdown2.markdown(entry)
        return render(request, 'encyclopedia/entry_page.html', {'title': entry_title,'content': entry })

class delete_entry(View):
    def get(self, request, *args, **kwargs):
        title = kwargs.get('title')
        delete_item(title)            
        return redirect('index')
        





        

