from rest_framework.decorators import api_view
from rest_framework.response import Response

from page.models import Page
from page.serializers import BaseSerializer, HomeSerializer


@api_view()
def home(request):
    page = Page.objects.filter(slug="home").first()
    baseSerializer = HomeSerializer(
        instance=page, many=False, context={"request": request}
    )

    return Response(
        {
            "home": baseSerializer.data,
        }
    )


@api_view()
def base(request):
    base = Page.objects.filter(slug="home").first()
    baseSerializer = BaseSerializer(
        instance=base, many=False, context={"request": request}
    )

    return Response(
        {
            "base": baseSerializer.data,
        }
    )
