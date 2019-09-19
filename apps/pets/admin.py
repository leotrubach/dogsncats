from apps.users.enums import UserRole
from . import models as M
from django.contrib import admin


class PetInline(admin.TabularInline):
    def has_delete_permission(self, request, obj=None):
        if request.user.role == UserRole.OWNER:
            if obj:
                return obj == request.user.owner
        return super().has_delete_permission(request, obj)

    def has_change_permission(self, request, obj=None):
        if request.user.role == UserRole.OWNER:
            if obj:
                return obj == request.user.owner
        return super().has_change_permission(request, obj)

    def has_add_permission(self, request, obj=None):
        if request.user.role == UserRole.OWNER:
            if obj:
                return obj == request.user.owner
        return super().has_add_permission(request, obj)


class CatsInline(PetInline):
    model = M.Cat


class DogsInline(PetInline):
    model = M.Dog


class OwnerAdmin(admin.ModelAdmin):
    list_display = ["full_name"]
    inlines = [CatsInline, DogsInline]

    def has_change_permission(self, request, obj=None):
        if request.user.role == UserRole.OWNER:
            if obj:
                return obj == request.user.owner
        return super().has_change_permission(request, obj)

    def has_delete_permission(self, request, obj=None):
        if request.user.role == UserRole.OWNER:
            return False
        return super().has_change_permission(request, obj)


class PetAdmin(admin.ModelAdmin):
    list_display = ["name", "owner"]

    def render_change_form(self, request, context, *args, **kwargs):
        if request.user.role == UserRole.OWNER:
            owner_field = context["adminform"].form.fields.get("owner")
            if owner_field:
                owner_field.queryset = M.Owner.objects.filter(
                    user=request.user
                )
                owner_field.initial = request.user.owner
        return super(PetAdmin, self).render_change_form(request, context, args, kwargs)

    def has_delete_permission(self, request, obj=None):
        if request.user.role == UserRole.OWNER:
            if obj:
                return obj.owner == request.user.owner
        return super().has_delete_permission(request, obj)

    def has_change_permission(self, request, obj=None):
        if request.user.role == UserRole.OWNER:
            if obj:
                return obj.owner == request.user.owner
        return super().has_change_permission(request, obj)


admin.site.register(M.Owner, OwnerAdmin)
admin.site.register(M.Cat, PetAdmin)
admin.site.register(M.Dog, PetAdmin)
