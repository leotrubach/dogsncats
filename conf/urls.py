from django.conf import settings
from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView
from rest_framework import routers
from apps.pets import viewsets as pets_viesets
from rest_framework.schemas import get_schema_view

router = routers.DefaultRouter()
router.register(r"owners", pets_viesets.OwnerViewSet, base_name="owner")
router.register(r"cats", pets_viesets.CatViewSet, base_name="cat")
router.register(r"dogs", pets_viesets.DogViewSet, base_name="dog")

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include((router.urls, "pets"), namespace="api")),
    path("api-auth/", include("rest_framework.urls", namespace="rest_framework")),
]

if settings.DEBUG:
    urlpatterns += [
        path(
            "openapi",
            get_schema_view(title="Dogs'n'Cats", description="API", version="1.0.0"),
            name="openapi-schema",
        ),
        path(
            "swagger-ui/",
            TemplateView.as_view(template_name="swagger-ui.html"),
            name="swagger-ui",
        ),
    ]
