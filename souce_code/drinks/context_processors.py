from drinks.models import Brand
def get_brand_names(request):
    return {'brand_names':  [b.name for b in Brand.objects.all()]}

