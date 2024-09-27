from ninja import NinjaAPI

from .models import Corner
from .schema import CornerOut, CornersOut

api = NinjaAPI()


@api.get("/corner", response=list[CornersOut])
def corners(request):
    return list(Corner.objects.all())


@api.get("/corner/{corner_id}", response=CornerOut)
def corner(request, corner_id: int):
    return Corner.objects.get(id=corner_id)
