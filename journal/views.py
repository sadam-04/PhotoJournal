from datetime import timedelta
from itertools import groupby
from operator import attrgetter
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.db import models
from django.db.models import Q
from django.db.models.functions import TruncDate
from .forms import JournalEntryForm 
from .models import JournalEntry

# Create your views here.

def homepage(request):
    mostRecentEntry = JournalEntry.objects.annotate(tsDate = TruncDate('timestamp')).order_by('tsDate').reverse().first()
    if (mostRecentEntry):
        mostRecentDate = mostRecentEntry.tsDate

        print("mostRecentDate: " + str(mostRecentDate))

        images = JournalEntry.objects.annotate(tsDate = TruncDate('timestamp')).order_by('tsDate').reverse().filter(Q(tsDate=mostRecentDate) | Q(tsDate=mostRecentDate + timedelta(days=-1)))
        # images2 = JournalEntry.objects.annotate(tsDate = TruncDate('timestamp')).filter(tsDate=mostRecentDate + timedelta(days=1))

        tmp = groupby(images, key=attrgetter('tsDate'))
        print("tmp: ")
        for i in tmp:
            print("i: " + str(i))

        groups = {timestamp: list(group) for timestamp, group in groupby(images, key=attrgetter('tsDate'))} # create a dictionary of days ("date": list of images)

        print(images)

        # latestDay = {mostRecentDate: images} # dictionary in same format as archive page

    else:
        groups = None

    return render(request, "journal/archive.html", {'days': groups})

def archive(request):
    if request.method == "POST":
        form = JournalEntryForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('archive')
    else:
        form = JournalEntryForm()
    # return render(request, "journal/upload.html", {'form': form})

    images = JournalEntry.objects.annotate(tsDate = TruncDate('timestamp')).order_by('tsDate').reverse()
    groups = {timestamp: list(group) for timestamp, group in groupby(images, key=attrgetter('tsDate'))} # create a dictionary of days ("date": list of images)

    # print("Groups:" + str(groups))
    return render(request, "journal/archive.html", {'days': groups, 'form': form})

# def upload(request):
