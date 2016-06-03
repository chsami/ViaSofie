from webapp.models import *
def header(request):
    cover = Data.objects.get(id=10)
    return {
        'conttest': "conttest",
    }
