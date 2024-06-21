from django.shortcuts import render

# Create your views here.
from rest_framework.views import APIView
from utils.response import *
from teak_admin.serializers import BannerSerializer
from teak_admin.models import Banner
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi


class BannerListCreateAPi(APIView):
    """
    API for listing and creating banners.

    This API provides a single endpoint for both listing and creating banners.
    """

    @swagger_auto_schema(

        responses={
            "200": openapi.Response(
                description="API returns success message.",
                examples={
                    "application/json": {
                        "message": [],
                        "status": "success",
                    }
                },
            ),
            "400": openapi.Response(
                description="Data required or Integrity errors.",
                examples={
                    "application/json": {
                        "error": {
                            "name": [],
                        },
                        "status": "failed",
                    }
                },
            ),
        },
    )

    def get(self, request, *args, **kwargs):
        """
        # Handle GET request to list all products.

        * Path params : NA.

        * Body params : NA.

        * Query params : NA.

        * Return : A HTTP response of success as json.

        """
        banner_instance = Banner.objects.all()
        banner_serializer = BannerSerializer(banner_instance, many=True)
        return HTTP_200({"banner": banner_serializer.data})

  
    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "name": openapi.Schema(
                    type=openapi.TYPE_STRING, description="Name of the sub category"
                ),
                "description": openapi.Schema(
                    type=openapi.TYPE_STRING,
                    description="Description of the sub category",
                ),
                "image": openapi.Schema(
                    type=openapi.TYPE_FILE,  # Assuming image is a URL or base64-encoded data
                    description="URL or base64-encoded image data",
                ),
                "is_status": openapi.Schema(
                    type=openapi.TYPE_BOOLEAN, description="Status of banner(True ot False)."
                ),
            },
            required=[],  # Add required fields if any
        ),
        responses={
            "200": openapi.Response(
                description="API returns success message.",
                examples={
                    "application/json": {
                        "message": "Banner created successfully.",
                        "status": "success",
                    }
                },
            ),
            "400": openapi.Response(
                description="Data required or Integrity errors.",
                examples={
                    "application/json": {
                        "error": {
                            "name": [],
                        },
                        "status": "failed",
                    }
                },
            ),
        },
    )
    def post(self, request, *args, **kwargs):
        """
        # Handle POST request create banner.

        * Path params : NA.

        * Body params : NA.

        * Query params : NA.

        * Return : A HTTP responses as success message as json.
        
        """
        # Create a new banner serializer instance
        banner_serializer = BannerSerializer(data=request.data)
        
        # Check if the serializer is valid
        if not banner_serializer.is_valid():
            # Return a 400 error if the serializer is not valid
            return HTTP_400({"error": banner_serializer.errors})
        
        # Save the banner
        banner_serializer.save()
        
        # Return a 200 success response with the created banner
        return HTTP_200(
            {"message": "banner created successfully", "banner": banner_serializer.data}
        )
