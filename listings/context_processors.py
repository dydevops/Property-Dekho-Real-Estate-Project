from .models import City,Locality

def mylocation(request):
    lcity = City.objects.filter(status=1).order_by('created_on')[0:6]
    return dict(mycity=lcity)

def mylocality(request):
    lclty= Locality.objects.filter(status=1).order_by('created_on')[0:6]
    return dict(local=lclty)