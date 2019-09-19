from django.utils.translation import gettext_lazy as _

from django_enumfield import enum


class UserRole(enum.Enum):
    NONE = 0
    OWNER = 1

    labels = {
        OWNER: _("Owner"),
    }
    __default__ = NONE
