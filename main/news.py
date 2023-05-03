import requests
from datetime import date, datetime, timedelta
from django.shortcuts import render

def get_news():
    today = date.today()
    one_month_ago = today - timedelta(days=30)
    url = (f'https://newsapi.org/v2/everything?from={today}&to={one_month_ago}&'
       'domains=thehackernews.com,securityweek.com,krebsonsecurity.com,helpnetsecurity.com,infosecurity-magazine.com,grahamcluley.com,darkreading.com,csoonline.com,cybersecurityventures.com&'
       'q=vulnerability&'
       'language=en&'
       'sortBy=publishedAt&'
       'pageSize=7&'
       'page=1&'
       'apiKey=7af51366b8a545fdb5ed2228b98c57b1')
    response=requests.get(url)
    data = response.json()
    articles = data['articles']
    for article in articles:
        published_at_str = article['publishedAt']
        published_at = datetime.fromisoformat(published_at_str[:-1])
        formatted_published_at = published_at.strftime('%B %d, %Y')
        article['publishedAt'] = formatted_published_at

    context = {
        'articles': articles
    }

    return context