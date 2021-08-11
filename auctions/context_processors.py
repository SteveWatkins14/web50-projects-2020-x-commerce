from .Category import *

def extras(request):
    return { "categories": Category }