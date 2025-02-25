from itertools import groupby
from operator import attrgetter
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.db import models
from .forms import JournalEntryForm 
from .models import JournalEntry

# Create your views here.

def homepage(request):
    images = JournalEntry.objects.all().order_by('date').reverse()
    groups = {date: list(group) for date, group in groupby(images, key=attrgetter('date'))}

    print("Groups:" + str(groups))
    return render(request, "journal/homepage.html", {'days': groups})

def upload(request):
    if request.method == "POST":
        form = JournalEntryForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('homepage')
    else:
        form = JournalEntryForm()
    return render(request, "journal/upload.html", {'form': form})