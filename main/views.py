from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import ToDo, Item
from django.contrib.auth import logout
import requests
from datetime import date, timedelta, datetime
import openai, os
from .youtube import search_videos
from .news import get_news
from .gpt_api import get_gpt_api
from django.contrib.auth.decorators import login_required

open_ai_key = os.getenv("OPENAI_API_KEY")
 
# Create your views here.

def resources(request):
    """
    Render the "Resources" page, which displays cybersecurity remediation
    videos from YouTube.
    """
    if request.method == 'GET':
        query = request.GET.get('q', 'What are common best practice cybersecurity measures?')
    else:
        query = 'What are common best practice cybersecurity measures?'

    videos = search_videos(query)

    context = {'videos': videos, 'query': query}
    return render(request, 'main/resources.html', context)


def index(response): 
    return render(response, "main/base.html", {})

def home(response): 
    return render(response, "main/home.html", {})

def news(request):
    context = get_news()
    return render(request, 'main/news.html', context)
    
def breachbites(request):
    gen_daily = request.POST.get('gen_daily')
    today = date.today()
    one_month_ago = today - timedelta(days=30)
    # user generated daily remediation tip for vulernability
    if gen_daily:
        found_vuln = True
        page = 1
        while found_vuln: 
            url = (f'https://newsapi.org/v2/everything?from={today}&to={one_month_ago}&page={page}&'
            'domains=thehackernews.com,securityweek.com,krebsonsecurity.com,helpnetsecurity.com,infosecurity-magazine.com,grahamcluley.com,darkreading.com,csoonline.com,cybersecurityventures.com&'
            'language=en&'
            'q=vulnerability&'
            'sortBy=publishedAt&'
            'pageSize=1&'
            'apiKey=')
            response=requests.get(url)
            data = response.json()
            articles = data['articles']
            result = get_gpt_api(articles[0]['content'])
            if ("False" in result):
                page += 1
            else: 
                found_vuln = False
            context = {
            'articles': articles,
            'response': result,
            }
        return render(request, 'main/breachbites.html', context)
    # user loaded website
    else: 
        url = (f'https://newsapi.org/v2/everything?from={today}&to={one_month_ago}&'
            'domains=thehackernews.com,securityweek.com,krebsonsecurity.com,helpnetsecurity.com,infosecurity-magazine.com,grahamcluley.com,darkreading.com,csoonline.com,cybersecurityventures.com&'
            'language=en&'
            'q=vulnerability&'
            'sortBy=publishedAt&'
            'pageSize=1&'
            'page=1&'
            'apiKey=')
        response=requests.get(url)
        data = response.json()
        articles = data['articles']
        context = {
        'articles': articles
        }
        return render(request, 'main/breachbites.html', context)

def login(response):
    return render(response, "registration/login.html", {})

def logout_view(request):
    logout(request)
    return redirect('')
