from .models import TagsModel

def all_tags(request):
    return {'tags': TagsModel.objects.all()}