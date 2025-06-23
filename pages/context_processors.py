from .models import General

def general_info(request):
    general = General.objects.filter(status=1).first()
    return dict(genlt=general)