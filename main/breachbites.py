from datetime import date, timedelta
import requests
from django.shortcuts import render
from .gpt_api import gpt_api

def get_breachbites(request):
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
            'apiKey=7af51366b8a545fdb5ed2228b98c57b1')
            response=requests.get(url)
            data = response.json()
            articles = data['articles']
            result = gpt_api(articles[0]['content'])
            if "False" in result:
                page += 1
            else: 
                found_vuln = False
        return render(request, 'main/breachbites.html', {"response": articles})
    # user loaded website
    else: 
        url = (f'https://newsapi.org/v2/everything?from={today}&to={one_month_ago}&'
            'domains=thehackernews.com,securityweek.com,krebsonsecurity.com,helpnetsecurity.com,infosecurity-magazine.com,grahamcluley.com,darkreading.com,csoonline.com,cybersecurityventures.com&'
            'language=en&'
            'q=vulnerability&'
            'sortBy=publishedAt&'
            'pageSize=1&'
            'page=1&'
            'apiKey=7af51366b8a545fdb5ed2228b98c57b1')
        response=requests.get(url)
        data = response.json()
        articles = data['articles']
        context = {
        'articles': articles
        }
        return render(request, 'main/breachbites.html', context)
