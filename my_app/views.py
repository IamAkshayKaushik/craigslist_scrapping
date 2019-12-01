from django.shortcuts import render

# Create your views here.
def Home(request):
    return render(request, 'base.html')

def search(request):
    search_content = request.POST.get('search')
    print(search_content)
    stuff_for_frontend = {
        'search_content':search_content,
    }
    return render(request, 'my_app/new_search.html', stuff_for_frontend)