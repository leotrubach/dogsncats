from django.db import models
from django.utils.translation import gettext_lazy as _


class Owner(models.Model):
    full_name = models.CharField(max_length=255, verbose_name=_("Full name"))

    class Meta:
        verbose_name = _("Owner")
        verbose_name_plural = _("Owners")

    def __str__(self):
        return self.full_name


class AbstractPet(models.Model):
    name = models.CharField(max_length=50, verbose_name=_("Name"))
    birthday = models.DateField(verbose_name=_("Birthday"))
    owner = models.ForeignKey(
        Owner, on_delete=models.PROTECT, verbose_name=_("Owner")
    )

    class Meta:
        abstract = True

    def __str__(self):
        return self.name


class Dog(AbstractPet):
    class Meta:
        verbose_name = _("Dog")
        verbose_name_plural = _("Dogs")


class Cat(AbstractPet):
    class Meta:
        verbose_name = _("Cat")
        verbose_name_plural = _("Cats")
