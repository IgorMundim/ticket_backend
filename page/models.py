from django.db import models


class LogoLink(models.Model):
    text = models.CharField(max_length=20)
    link = models.CharField(max_length=250)
    srcImg = models.ImageField(
        max_length=200,
        upload_to="covers/%Y/%m/%d/logoLink",
        blank=True,
    )

    def __str__(self):
        return self.text


class MenuLink(models.Model):
    order = models.IntegerField(unique=True)
    text = models.CharField(max_length=20)
    link = models.CharField(max_length=250)
    newTab = models.BooleanField(default=False)

    def __str__(self):
        return self.text

    class Meta:
        ordering = ["order"]


class Banner(models.Model):

    order = models.IntegerField(unique=True)
    title = models.CharField(max_length=200)
    src = models.ImageField(
        max_length=200,
        upload_to="covers/%Y/%m/%d/banner",
    )
    alt = models.CharField(max_length=150)
    description = models.CharField(max_length=200)
    link = models.CharField(max_length=250)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ["order"]


class Footer(models.Model):
    footerHtml = models.CharField(max_length=250)
    src_img = models.ImageField(
        max_length=200, upload_to="covers/%Y/%m/%d/footer", null=True
    )

    alt_text = models.CharField(max_length=150, null=True)

    def __str__(self):
        return self.footerHtml


class Page(models.Model):
    title = models.CharField(max_length=20)
    slug = models.CharField(max_length=20, blank=True)
    footer = models.ForeignKey(Footer, on_delete=models.SET_NULL, null=True)
    banners = models.ManyToManyField(
        Banner,
    )
    menuLink = models.ManyToManyField(
        MenuLink,
    )
    logoLink = models.ForeignKey(
        LogoLink, on_delete=models.SET_NULL, null=True
    )

    def __str__(self):
        return self.title
