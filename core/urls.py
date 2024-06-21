
from django.contrib import admin
from django.urls import path, include, re_path
from product.views import *
from django.conf import settings
from django.conf.urls.static import static
from teak_admin.views import *
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions


schema_view = get_schema_view(
    openapi.Info(
        title="Teak API ",
        default_version="v1",
        description="API for documentation for teak wood factory",
        terms_of_service="https://robingracejo.netlify.app/",
        contact=openapi.Contact(email="robinrajan440@gmail.com",phone=8086712029),
        license=openapi.License(name="Copyright © 2023 Robin | | All Rights Reserved"),
        x_logo={"url": "https://robingracejo.netlify.app/images/pro.jpeg", "backgroundColor": "#FFFFFF"},
        public=True,
 
    )
)


urlpatterns = [
    path("admin/", admin.site.urls),
    # category urls
    path("api/category/", CategoryListCreateAPI.as_view(), name="category-list-create"),
    # category crud
    path(
        "api/category/<uuid:category_uuid>/",
        CategoryCRUDApi.as_view(),
        name="category-crud",
    ),
    # sub category urls
    path(
        "api/sub-category/", SubCategoryAPI.as_view(), name="sub-category-list-create"
    ),
    # sub category crud
    path(
        "api/sub-category/<uuid:sub_category_uuid>/",
        SubCategoryCRUDApi.as_view(),
        name="sub_category-crud",
    ),
    # subs of subs
    path("api/sub-of-sub/", SubofSubAPI.as_view(), name="subs-of-list-create"),
    # subs of subs crud
    path(
        "api/sub-of-sub/<uuid:subs_uuid>",
        SubsofSubsCRUDAPI.as_view(),
        name="subs-of-crud",
    ),
    # product urls
    path(
        "api/product/", ProductsListCreateAPIview.as_view(), name="product-list-create"
    ),
    # product crud
    path(
        "api/product/<uuid:product_uuid>/", ProductCRUDApi.as_view(), name="product-crud"
    ),

    path(
        "api/banner/", BannerListCreateAPi.as_view(), name="banner-list-create"
    ),

    # search 

    path(
        "api/search/", SearchProductAPI.as_view(), name="search-product"
    ),


     re_path(
        r"^redoc/$", schema_view.with_ui("redoc", cache_timeout=0), name="schema-redoc"
    ),
    re_path(
        r"^swagger(?P<format>\\\\.json|\\\\.yaml)$",
        schema_view.without_ui(cache_timeout=0),
        name="schema-json",
    ),
    re_path(
        r"^swagger/$",
        schema_view.with_ui("swagger", cache_timeout=0),
        name="schema-swagger-ui",
    ),


    
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
