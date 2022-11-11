from django.contrib import admin

from page import models


# Register your models here.
@admin.register(models.Banner)
class BannerAdmin(admin.ModelAdmin):
    list_display = ("order", "title")


@admin.register(models.MenuLink)
class MenuLinkAdmin(admin.ModelAdmin):
    list_display = ("order", "text")


@admin.register(models.LogoLink)
class LogoLinkAdmin(admin.ModelAdmin):
    list_display = ["text"]


@admin.register(models.Page)
class PageAdmin(admin.ModelAdmin):
    list_display = ["title"]


@admin.register(models.Footer)
class FooterAdmin(admin.ModelAdmin):
    list_display = ["footerHtml"]
