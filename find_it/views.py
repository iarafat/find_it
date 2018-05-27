from django.shortcuts import render
from django.db import IntegrityError
from scraping.utils import *
from scraping.models import *


def home(request):
    city = City.objects.get(name='Киев')
    specialty = Specialty.objects.get(name='Python')
    url_qs = Url.objects.filter(city=city, specialty=specialty)
    site = Site.objects.all()
    url_w = url_qs.get(site=site.get(name='Work.ua')).url_address
    jobs = []
    # jobs.extend(djinni())
    # jobs.extend(rabota())
    jobs.extend(work(url_w))
    # jobs.extend(dou())
    
    # v = Vacancy.objects.filter(city=city.id, specialty=specialty.id).values('url')
    # url_list = [i['url'] for i in v]
    for job in jobs:
        vacancy = Vacancy(city=city, specialty=specialty, url=job['href'],
                                title=job['title'], description=job['descript'], company=job['company'])
        try:
            vacancy.save()
        except IntegrityError:
            pass

    return render(request, 'base.html', {'jobs': jobs})