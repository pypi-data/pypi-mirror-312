from django.urls import path, include
from rest_framework.schemas import get_schema_view
from rest_framework_swagger.renderers import SwaggerUIRenderer, OpenAPICodec
from rest_framework.documentation import include_docs_urls
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from django.views.decorators.clickjacking import xframe_options_exempt

schema_view = get_schema_view(
    openapi.Info(
        title="PhenoTools API", 
        default_version="V1",
        description="The interface documentation of PhenoTools",
        contact=openapi.Contact(
            email="postmaster@team.phenonet.org", url="https://phenonet.org"
        ),
    ),
    public=True,
)

urlpatterns = [
    # path("docs/", include_docs_urls(title="PhenoTool API")),
    path("docs/", xframe_options_exempt(schema_view.with_ui("redoc", cache_timeout=0)), name="schema-redoc"),
    path("", include("system.urls")),
    path("", include("task.urls")),
    path("", include("file.urls")), 
    path("", include("model.urls")),
    path("", include("dataset.urls")),
]
