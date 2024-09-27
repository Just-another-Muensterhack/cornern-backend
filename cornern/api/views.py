from ninja import NinjaAPI

from .models import Corner
from .schema import CornersOut

api = NinjaAPI()


@api.get("/corner", response=list[CornersOut])
def hello(request):
    return list(Corner.objects.all())
