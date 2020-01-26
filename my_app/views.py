from datetime import datetime

from django.shortcuts import render
import urllib.parse
import requests
from . import models
from bs4 import BeautifulSoup

base_url = "https://delhi.craigslist.org/search/bbb?query="

# Create your views here.
def Home(request):
    return render(request, 'base.html')

def search(request):
    search_content = request.POST.get('search').strip()
    models.Search.objects.create(search=search_content, created=datetime.now())
    search_content_encoded = urllib.parse.quote_plus(search_content)
    final_url = base_url + f'{search_content_encoded}'
    response = requests.get(final_url)
    data = response.text
    soup = BeautifulSoup(data, 'html.parser')
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
            post_price = None
        post_image_ids = post.find('a',{'class':'result-image'}).get('data-ids')
        if post_image_ids:
            post_image_ids = post_image_ids.split(',')
            if(len(post_image_ids) > 0):
                post_image_final_id_list = []
                for image_id in post_image_ids:
                    final_id = image_id.split(':')[-1]
                    post_image_final_id_list.append(final_id)
        post_listings.append((post_title, post_url, post_price, post_image_final_id_list))

    stuff_for_frontend = {
        'search_content':search_content,
        'post_listings':post_listings
    }
    print(stuff_for_frontend)
    return render(request, 'my_app/new_search.html', stuff_for_frontend)