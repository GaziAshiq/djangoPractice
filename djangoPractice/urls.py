from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from debug_toolbar.toolbar import debug_toolbar_urls

from core import views as core_views

admin.site.site_header = "Django Practice Admin"
admin.site.site_title = "Admin Portal"
admin.site.index_title = "Welcome to Django Practice"

urlpatterns = [
    path("", core_views.index),
    path("hello/", core_views.say_hello),
    path("objects/", core_views.objects__retrieve_filter),
    path("tags/", core_views.tags_items),
    path("create_object/", core_views.create_collection),
    path("update_object/", core_views.update_collection),
    path("delete_object/", core_views.delete_collection),
    path("create_order/", core_views.save_order),
    path("raw_sql/", core_views.raw_sql_query),
    path("core/", core_views.about),
    path("admin/", admin.site.urls),
    path("__reload__/", include("django_browser_reload.urls")),
]
if settings.DEBUG:
    urlpatterns += debug_toolbar_urls()
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
