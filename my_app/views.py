import random
from datetime import datetime

from django.shortcuts import render
import urllib.parse
import requests
from . import models
from bs4 import BeautifulSoup

base_url = "https://delhi.craigslist.org/search/bbb?query="
image_base_url = "https://images.craigslist.org/{}_300x300.jpg"
user_agent_list = [
   #Chrome
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36',
    'Mozilla/5.0 (Windows NT 5.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.2; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36',
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36',
    #Firefox
    'Mozilla/4.0 (compatible; MSIE 9.0; Windows NT 6.1)',
    'Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko',
    'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0)',
    'Mozilla/5.0 (Windows NT 6.1; Trident/7.0; rv:11.0) like Gecko',
    'Mozilla/5.0 (Windows NT 6.2; WOW64; Trident/7.0; rv:11.0) like Gecko',
    'Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; rv:11.0) like Gecko',
    'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.0; Trident/5.0)',
    'Mozilla/5.0 (Windows NT 6.3; WOW64; Trident/7.0; rv:11.0) like Gecko',
    'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0)',
    'Mozilla/5.0 (Windows NT 6.1; Win64; x64; Trident/7.0; rv:11.0) like Gecko',
    'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; WOW64; Trident/6.0)',
    'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; Trident/6.0)',
    'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.1; Trident/4.0; .NET CLR 2.0.50727; .NET CLR 3.0.4506.2152; .NET CLR 3.5.30729)'
]
# Create your views here.
def Home(request):
    return render(request, 'base.html')

def search(request):

    search_content = request.POST.get('search',None)
    if search_content is not None:
        search_content = search_content.strip()
        models.Search.objects.create(search=search_content, created=datetime.now())
        headers = {'user-agent': random.choice(user_agent_list)}
        search_content_encoded = urllib.parse.quote_plus(search_content)
        final_url = base_url + f'{search_content_encoded}'
        response = requests.get(final_url,headers=headers)
        data = response.text
        soup = BeautifulSoup(data, 'lxml')
        all_posts = soup.find_all('li',{'class':"result-row"})
        post_listings = []
        for post in all_posts:
            post_row = post.find('a',{'class':'result-title'})
            post_title = post_row.text
            post_url = post_row.get('href')
            post_price = post.find('a',{'class':'result-price'})
            if(post_price):
                post_price = post_price.text
            else:
                post_price = 'NA'
            post_image_ids = post.find('a',{'class':'result-image'}).get('data-ids')
            if post_image_ids:
                post_image_ids = post_image_ids.split(',')[0].split(':')[-1]
                post_image_url = image_base_url.format(post_image_ids)
            else:
                post_image_url = "https://craigslist.org/images/peace.jpg"
            post_listings.append((post_title, post_url, post_price, post_image_url))

        stuff_for_frontend = {
            'search_content':search_content,
            'post_listings':post_listings
        }
        return render(request, 'my_app/new_search.html', stuff_for_frontend)
    else:
        return render(request, 'base.html')