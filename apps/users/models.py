from django.core.exceptions import ValidationError
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from django_enumfield import enum
from apps.pets import models as pets_models
from .enums import UserRole


class User(AbstractUser):
    role = enum.EnumField(UserRole, verbose_name=_("Role"))
    owner = models.ForeignKey(
        pets_models.Owner,
        verbose_name=_("Owner"),
        on_delete=models.PROTECT,
        blank=True,
        null=True,
    )

    class Meta:
        verbose_name = _("User")
        verbose_name_plural = _("Users")

    def clean(self):
        if self.role == UserRole.OWNER and not self.owner:
            raise ValidationError(
                _("Owner field must be specified if user role is OWNER")
            )
        if self.owner and self.role != UserRole.OWNER:
            raise ValidationError(
                _("Owner may not be specified if user role is not OWNER")
            )

    def has_perm(self, perm, obj=None):
        if self.is_superuser:
            return True
        if self.role == UserRole.OWNER:
            return self.owner_has_perm(perm, obj)
        return super().has_perm(perm, obj)

    def has_module_perms(self, app_label):
        if self.is_superuser:
            return True
        if self.role == UserRole.OWNER:
            if app_label == "pets":
                return True
            else:
                return False
        return super().has_module_perms(app_label)

    def owner_has_perm(self, perm, obj):
        """
        Permissions for pet owner users
        """
        perm = perm.lower() if perm else ""
        app, action_model = perm.split(".")
        action, model = action_model.split("_", 1)
        if app != "pets":
            return super().has_perm(perm, obj)
        if model == "owner":
            if obj:
                if obj == self.owner:
                    return action != "delete"
                else:
                    return action not in ("change", "delete")
            else:
                return action != 'add'
        if model in ("cat", "dog"):
            if obj:
                if obj.owner != self.owner:
                    return action not in ["change", "delete"]
        return True
