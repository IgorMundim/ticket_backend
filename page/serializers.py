from rest_framework import serializers

from event.models import Address, Category, Event, Image
from page.models import Banner, Footer, LogoLink, MenuLink, Page


class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = [
            "id",
            "image_url",
            "alt_text",
        ]


class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = [
            "id",
            "city",
            "uf",
        ]


class BasicEventSerializer(serializers.ModelSerializer):
    address = AddressSerializer(many=False, read_only=True)
    image = ImageSerializer(many=False, read_only=True)

    class Meta:
        model = Event
        fields = [
            "id",
            "name",
            "date_end",
            "address",
            "image",
        ]


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = [
            "id",
            "name",
            "slug",
            "image_url",
            "alt_text",
        ]


class LogoLinkSerializer(serializers.ModelSerializer):
    class Meta:
        model = LogoLink
        fields = ["id", "text", "link", "srcImg"]


class MenuLinkSerializer(serializers.ModelSerializer):
    class Meta:
        model = MenuLink
        fields = ["id", "order", "text", "link", "newTab"]


class FooterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Footer
        fields = ["id", "footerHtml", "src_img", "alt_text"]


class BannerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Banner
        fields = ["id", "order", "title", "src", "alt", "description", "link"]


class HomeSerializer(serializers.ModelSerializer):
    logoLink = LogoLinkSerializer(many=False, read_only=True)
    footer = FooterSerializer(many=False, read_only=True)
    banners = BannerSerializer(many=True, read_only=True)
    menuLink = MenuLinkSerializer(many=True, read_only=True)

    class Meta:
        model = Page
        fields = [
            "title",
            "banners",
            "slug",
            "menuLink",
            "logoLink",
            "footer",
        ]


class BaseSerializer(serializers.ModelSerializer):
    logoLink = LogoLinkSerializer(many=False, read_only=True)
    footer = FooterSerializer(many=False, read_only=True)
    menuLink = MenuLinkSerializer(many=True, read_only=True)

    class Meta:
        model = Page
        fields = [
            "title",
            "menuLink",
            "logoLink",
            "footer",
        ]
