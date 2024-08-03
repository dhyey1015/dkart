from category.models import Category

def menu_links(request):
    links = Category.objects.all() #fetch all the categories form database
    return dict(links= links)    