from datetime import timedelta
from itertools import groupby
from operator import attrgetter
from django.shortcuts import render, redirect
from django.db.models import Q
from django.db.models.functions import TruncDate
from django.contrib.auth.models import User

from PhotoJournal import settings
from .forms import JournalEntryForm 
from .models import JournalEntry

from django.contrib import auth

# Create your views here.

def homepage(request):
    mostRecentEntry = JournalEntry.objects.annotate(tsDate = TruncDate('timestamp')).order_by('tsDate').reverse().first()
    if (mostRecentEntry):
        mostRecentDate = mostRecentEntry.tsDate

        print("mostRecentDate: " + str(mostRecentDate))

        images = JournalEntry.objects.annotate(tsDate = TruncDate('timestamp')).order_by('tsDate').filter(visible=True).reverse()
        groups = {timestamp: list(group) for timestamp, group in groupby(images, key=attrgetter('tsDate'))} # create a dictionary of days ("date": list of images)

        # images = JournalEntry.objects.annotate(tsDate = TruncDate('timestamp')).order_by('tsDate').reverse().filter(Q(tsDate=mostRecentDate) | Q(tsDate=mostRecentDate + timedelta(days=-1))).filter(visible=True)
        # # images2 = JournalEntry.objects.annotate(tsDate = TruncDate('timestamp')).filter(tsDate=mostRecentDate + timedelta(days=1))

        # tmp = groupby(images, key=attrgetter('tsDate'))
        # # print("tmp: ")
        # # for i in tmp:
        # #     print("i: " + str(i))

        # groups = {timestamp: list(group) for timestamp, group in groupby(images, key=attrgetter('tsDate'))} # create a dictionary of days ("date": list of images)

        # print(images)

        # latestDay = {mostRecentDate: images} # dictionary in same format as archive page

    else:
        groups = None

    return render(request, "journal/archive.html", {'days': groups})

def archive(request):
    # only superusers may access the archive page
    if not request.user.is_superuser:
        return redirect(f"{settings.LOGIN_URL}?next={request.path}")
    else:
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

def hide(request):
    if request.user.is_superuser and request.method == 'POST':
        id = request.POST["target_id"]
        target = JournalEntry.objects.filter(id=id).first()
        if target is not None:
            target.visible = False
            # print("Visibility: " + str(target.visible))
            target.save(update_fields=['visible'])
    return redirect('archive')

def show(request):
    if request.user.is_superuser and request.method == 'POST':
        id = request.POST["target_id"]
        target = JournalEntry.objects.filter(id=id).first()
        if target is not None:
            target.visible = True
            target.save(update_fields=['visible'])
    return redirect('archive')


def login(request):
    if request.method == "POST":
        user = auth.authenticate(request, username=request.POST["username"], password=request.POST["password"])
        if user:
            auth.login(request, user)
            return redirect("homepage")
    return render(request, 'journal/login.html')

def logout(request):
    auth.logout(request)
    return redirect('homepage')

# def upload(request):
