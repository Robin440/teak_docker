from django.shortcuts import render
from django.db.models import Q

# Create your views here.
from rest_framework.views import APIView
from utils.response import *
from product.models import Category, Subcategory, SubofSub
from product.serializers import *
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

# backend developed by robin rajan

# mob : 8086712029


# Category API's


class CategoryListCreateAPI(APIView):
    """api for list and create category"""

    @swagger_auto_schema(
        response_schema={
            "200": openapi.Response(
                description="Category List",
                examples={"application/json": {"catagory": [], "status": "success"}},
            ),
            "400": openapi.Response(
                description="Data required or Integrity errors.",
                examples={
                    "application/json": {
                        "error": [],
                        "status": "failed",
                        "non_binary_field": [],
                    }
                },
            ),
        }
    )
    def get(self, request, *args, **kwargs):
        """
        # Handle GET request to list category.

        * Body params : NA
        * Header params : NA
        * Query params : NA

        * Return : List of categories

        """

        # query for list all category
        category_instance = Category.objects.all()

        # serialization of query
        category_serializer = CategorySerializers(category_instance, many=True)

        # success response
        return HTTP_200({"category": category_serializer.data})

    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "name": openapi.Schema(
                    type=openapi.TYPE_STRING, description="Name of the category"
                ),
                "description": openapi.Schema(
                    type=openapi.TYPE_STRING, description="Description of the category"
                ),
                "image": openapi.Schema(
                    type=openapi.TYPE_FILE,  # Assuming image is a URL or base64-encoded data
                    description="URL or base64-encoded image data",
                ),
            },
            required=[],  # Add required fields if any
        ),
        response_schema={
            "200": openapi.Response(
                description="Category List",
                examples={"application/json": {"catagory": [], "status": "success"}},
            ),
            "400": openapi.Response(
                description="Data required or Integrity errors.",
                examples={
                    "application/json": {
                        "error": [],
                        "status": "failed",
                        "non_binary_field": [],
                    }
                },
            ),
        },
    )
    def post(self, request, *args, **kwargs):
        """
        # Handle POST request to create category.

        * Body params : Provide body params which are name , description and image.
        * Header params : NA.
        * Query params : NA.
        * Return : Newly created category.

        """

        # deserialization of json data to query
        category_serializer = CategorySerializers(data=request.data)

        # validating serializer
        if category_serializer.is_valid():
            category_serializer.save()
        else:
            return HTTP_400({"errors": category_serializer.errors})

        # sucess response
        return HTTP_200(
            {
                "message": "category created successfully",
                "category": category_serializer.data,
            }
        )


class CategoryCRUDApi(APIView):
    """api for category crud"""

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                "category_uuid",
                openapi.IN_PATH,
                description="UUID of the link to update , should pass as path params.",
                type=openapi.TYPE_STRING,
                required=True,
            ),
        ],
        responses={
            "200": openapi.Response(
                description="API returns success message.",
                examples={
                    "application/json": {
                        "message": "",
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
        # Handle GET request to retrieve a link.

        * Body params : NA.

        * Header params : NA.

        * Query params : NA.

        * Return : a HTTP response with json data.

        """

        # receiving uuid
        category_uuid = kwargs.get("category_uuid")
        # handling error in the absence of uuid
        if not category_uuid:
            return HTTP_400("Sorry! you have to provide category uuid")

        # query for category with error handling
        try:
            category_instance = Category.objects.get(uuid=category_uuid)
        except Category.DoesNotExist:
            return HTTP_400("Sorry! Category do not exists in database")

        # serialization
        category_serializer = CategorySerializers(category_instance)

        # success response
        return HTTP_200({"category": category_serializer.data})

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                "category_uuid",
                openapi.IN_PATH,
                description="UUID of the link to list , should pass as path params.",
                type=openapi.TYPE_STRING,
                required=True,
            ),
        ],
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "name": openapi.Schema(
                    type=openapi.TYPE_STRING, description="Name of the category"
                ),
                "description": openapi.Schema(
                    type=openapi.TYPE_STRING, description="Description of the category"
                ),
                "image": openapi.Schema(
                    type=openapi.TYPE_FILE,  # Assuming image is a URL or base64-encoded data
                    description="URL or base64-encoded image data",
                ),
            },
            required=[],  # Add required fields if any
        ),
        responses={
            "200": openapi.Response(
                description="API returns success message.",
                examples={
                    "application/json": {
                        "message": "Link updated successfully.",
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
    def put(self, request, *args, **kwargs):
        """
        # Handle PUT request to update link.

        * Body params : This api accepts name , description and image.

        * Path params : uuid of link which have to update


        """

        # receiving uuid
        category_uuid = kwargs.get("category_uuid")

        # handling error in the absence of uuid
        if not category_uuid:
            return HTTP_400("Sorry! you have to provide category uuid")

        # query for category with error handling
        try:
            category_instance = Category.objects.get(uuid=category_uuid)
        except Category.DoesNotExist:
            return HTTP_400("Sorry! Category do not exists in database")

        # deserialization
        category_serializer = CategorySerializers(
            instance=category_instance, data=request.data, partial=True
        )

        # validating serializer
        if category_serializer.is_valid():
            category_serializer.save()

        else:
            return HTTP_400({"error": category_serializer.errors})

        # success response
        return HTTP_200(
            {
                "message": "category updated successfully",
                "category": category_serializer.data,
            }
        )

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                "category_uuid",
                openapi.IN_PATH,
                description="UUID of the link to delete , should pass as path params.",
                type=openapi.TYPE_STRING,
                required=True,
            ),
        ],
        responses={
            "200": openapi.Response(
                description="API returns success message.",
                examples={
                    "application/json": {
                        "message": "Link deleted successfully.",
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
    def delete(self, request, *args, **kwargs):
        """
        # Handle DELETE request to delete category.

        * Path params : Provid uuid of category which have to delete.

        * Body params : NA

        * Return : A HTTP response of success message as json.

        """

        # receiving uuid
        category_uuid = kwargs.get("category_uuid")

        # handling error in the absence of uuid
        if not category_uuid:
            return HTTP_400("Sorry! you have to provide category uuid")

        # query for category with error handling
        try:
            category_instance = Category.objects.get(uuid=category_uuid)
        except Category.DoesNotExist:
            return HTTP_400("Sorry! category do not found in database")

        # deleting the instance
        category_instance.delete()

        # success response
        return HTTP_200("Category deleted successfully")


# Sub category API's


class SubCategoryAPI(APIView):
    """
    # Handle GET request to list sub cateogory.

    * Body params : NA.
    * Query params : NA.
    * Header params : NA.
    * Path params : NA.

    * Response : List of sub categories.

    """

    @swagger_auto_schema(
        responses={
            "200": openapi.Response(
                description="API list all sub categories.",
                examples={
                    "application/json": {
                        "message": "",
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
        # Handle GET request to list sub category.

        * Body params : NA.
        * Query params : NA.
        * Header params : NA.
        * Path params : NA.

        * Response : List of sub categories.

        """

        # query for list all sub category and serialization
        sub_category_instance = Subcategory.objects.all()
        sub_category_serializer = SubCategorySerializers(
            sub_category_instance, many=True
        )

        # success response
        return HTTP_200({"sub_category": sub_category_serializer.data})

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
                "category": openapi.Schema(
                    type=openapi.TYPE_STRING, description="Category uuid"
                ),
            },
            required=[],  # Add required fields if any
        ),
        responses={
            "200": openapi.Response(
                description="API returns success message.",
                examples={
                    "application/json": {
                        "message": "Subcategory created successfully.",
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
        # Handle POST request to create sub category.

        * Body params : This api accepts body params which are name , description , image and category (uuid of catogory)

        """

        # deserialization
        sub_category_serializer = SubCategorySerializers(data=request.data)

        # receiving category uuid
        category_uuid = request.data.get("category")
        category = None

        # validation and query for category
        if category_uuid:
            try:
                category = Category.objects.get(uuid=category_uuid)
            except Category.DoesNotExist:
                return HTTP_400("Category not found in the database")

        # validating serializer
        if sub_category_serializer.is_valid():
            sub_category_serializer.save(category=category)

            # success response
            return HTTP_200(
                {
                    "message": "Subcategory created successfully",
                    "sub_category": sub_category_serializer.data,
                }
            )

        return HTTP_400({"error": sub_category_serializer.errors})


class SubCategoryCRUDApi(APIView):
    """api for sub category CRUD"""

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                "sub_category_uuid",
                openapi.IN_PATH,
                description="UUID of the sub_category_uuid to list , should pass as path params.",
                type=openapi.TYPE_STRING,
                required=True,
            ),
        ],
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
                            "non_binary_error": [],
                        },
                        "status": "failed",
                    }
                },
            ),
        },
    )
    def get(self, requst, *args, **kwargs):
        """
        # Handle GET request to list sub category by uuid.

        * Path params : Provide sub category uuid to list.

        * Body params : NA.

        * Query params : NA.

        * Return : A HTTP response of Sub category as json data.

        """

        # receiving sub category uuid
        sub_category_uuid = kwargs.get("sub_category_uuid")

        # error handling in the case of uuid absence
        if not sub_category_uuid:
            return HTTP_400("Sorry! you have to provide sub category uuid")

        # validating and query for sub category
        try:
            sub_category_instance = Subcategory.objects.get(uuid=sub_category_uuid)
        except Subcategory.DoesNotExist:
            return HTTP_400("Sorry! sub category is not found in database or deleted.")

        # serialization
        sub_category_serializer = SubCategorySerializers(sub_category_instance)

        # success response
        return HTTP_200({"sub_category": sub_category_serializer.data})

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                "sub_category_uuid",
                openapi.IN_PATH,
                description="UUID of the sub_category_uuid to update , should pass as path params.",
                type=openapi.TYPE_STRING,
                required=True,
            ),
        ],
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
                "category": openapi.Schema(
                    type=openapi.TYPE_STRING, description="Category uuid"
                ),
            },
            required=[],  # Add required fields if any
        ),
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
                            "non_binary_error": [],
                        },
                        "status": "failed",
                    }
                },
            ),
        },
    )
    def put(self, request, *args, **kwargs):
        """
        # Handle PUT request update sub category.

        * Path params : Provide uuid of the sub category.

        * Body params : Provide values as required for name , description , image and category(uuid).

        * Return : A HTTP response of success in json.

        """
        # receiving sub category uuid
        sub_category_uuid = kwargs.get("sub_category_uuid")
        if not sub_category_uuid:
            return HTTP_400("Sorry! you have to provide sub category uuid")

        # validating and query for sub category
        try:
            sub_category_instance = Subcategory.objects.get(uuid=sub_category_uuid)
        except Subcategory.DoesNotExist:
            return HTTP_400("Sorry! sub category is not found in database or deleted.")

        # deserialization
        sub_category_serializer = SubCategorySerializers(
            instance=sub_category_instance, data=request.data, partial=True
        )

        # validation of serializer
        if sub_category_serializer.is_valid():
            sub_category_serializer.save()
        else:
            return HTTP_400({"error": sub_category_serializer.errors})

        # success response
        return HTTP_200(
            {
                "message": "category updated successfully",
                "category": sub_category_serializer.data,
            }
        )

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                "sub_category_uuid",
                openapi.IN_PATH,
                description="UUID of the sub_category_uuid to delete , should pass as path params.",
                type=openapi.TYPE_STRING,
                required=True,
            ),
        ],
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
                            "non_binary_error": [],
                        },
                        "status": "failed",
                    }
                },
            ),
        },
    )
    def delete(self, request, *args, **kwargs):
        """
        # Handle DELETE request to delete sub category .

        * Path params : Provide uuid of sub category to delete.

        * Body params : NA.

        * Return : A HTTP response of success with json.

        """
        # receiving uuid of sub category
        sub_category_uuid = kwargs.get("sub_category_uuid")

        # error handling in the case of uuid
        if not sub_category_uuid:
            return HTTP_400("Sorry! you have to provide sub category uuid")

        # query and validation of sub category
        try:
            sub_category_instance = Subcategory.objects.get(uuid=sub_category_uuid)
        except Subcategory.DoesNotExist:
            return HTTP_400("Sorry! sub category do not found in database")

        # deletion of the instance from db
        sub_category_instance.delete()

        # success response
        return HTTP_200("Sub Category deleted successfully")


# subs of subs API's


class SubofSubAPI(APIView):
    """api for subs of subs list and create"""

    @swagger_auto_schema(
        responses={
            "200": openapi.Response(
                description="API list all sub categories of sub categories.",
                examples={
                    "application/json": {
                        "message": "",
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
        # Handle GET request to list sub category of sub category.

        * Body params : NA.

        * Path params : NA.

        * Header params : NA.

        * Query params : NA.

        * Return : A HTTP response of sub of subs data as json.

        """

        # query for list all sub - sub category and serialization
        subs_instance = SubofSub.objects.all()
        subs_serializer = SubofSubSerializers(subs_instance, many=True)

        # success response
        return HTTP_200({"subs_of": subs_serializer.data})

    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "name": openapi.Schema(
                    type=openapi.TYPE_STRING,
                    description="Name of the sub category of sub category.",
                ),
                "description": openapi.Schema(
                    type=openapi.TYPE_STRING,
                    description="Description of the sub category of sub category.",
                ),
                "image": openapi.Schema(
                    type=openapi.TYPE_FILE,  # Assuming image is a URL or base64-encoded data
                    description="URL or base64-encoded image data",
                ),
                "sub_category": openapi.Schema(
                    type=openapi.TYPE_STRING, description="Sub category uuid"
                ),
            },
            required=[],  # Add required fields if any
        ),
        responses={
            "200": openapi.Response(
                description="API returns success message.",
                examples={
                    "application/json": {
                        "message": "Subcategory of sub category is created successfully.",
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
        # Handle POST request to create sub category of sub  category.

        * Body params : Provide name , description , image and uuid of sub category uuid.

        * Path params : NA.

        * Query params : NA.

        * Header params : NA.

        * Return : A HTTP response a success message with json.

        """

        # deserialization
        subs_serializer = SubofSubSerializers(data=request.data)

        # assigning sub category uuid into a variable from request data
        sub_category_uuid = request.data.get("sub_category")
        sub_category = None

        # query and validating the sub category
        if sub_category_uuid:
            try:
                sub_category = Subcategory.objects.get(uuid=sub_category_uuid)
            except Subcategory.DoesNotExist:
                return HTTP_400("Sorry, subcategory not found in the database")

        # validation of serializer and success response
        if subs_serializer.is_valid():
            subs_serializer.save(sub_category=sub_category)
            return HTTP_200(
                {"message": "Subs of subs created", "subs_of": subs_serializer.data}
            )

        return HTTP_400({"error": subs_serializer.errors})


class SubsofSubsCRUDAPI(APIView):
    """api for subs crud operation"""

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                "subs_uuid",
                openapi.IN_PATH,
                description="UUID of the subs_uuid to update , should pass as path params.",
                type=openapi.TYPE_STRING,
                required=True,
            ),
        ],
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
                            "non_binary_error": [],
                        },
                        "status": "failed",
                    }
                },
            ),
        },
    )
    def get(self, request, *args, **kwargs):
        """
        # Handle GET request to list sub category of sub category.

        * Path params : Provide uuid of sub category of sub category.

        * Body params : NA.

        * Query params : NA.

        * Header params : NA.

        * Return : A HTTP response to sub category of sub category data as json.


        """

        # receiving uuid
        subs_uuid = kwargs.get("subs_uuid")

        # error handling in the case of uuid absence
        if not subs_uuid:
            return HTTP_400("Sorry! you have to provide subs of subs uuid")

        # query for sub sub category and validating
        try:
            subs_instance = SubofSub.objects.get(uuid=subs_uuid)
        except SubofSub.DoesNotExist:
            return HTTP_400("Sorry! Subs of Subs is not found in database or deleted")

        # serialization
        subs_serializer = SubofSubSerializers(subs_instance)

        # success response
        return HTTP_200({"subs_of": subs_serializer.data})

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                "subs_uuid",
                openapi.IN_PATH,
                description="UUID of the subs_uuid to update , should pass as path params.",
                type=openapi.TYPE_STRING,
                required=True,
            ),
        ],
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "name": openapi.Schema(
                    type=openapi.TYPE_STRING,
                    description="Name of the sub category of sub category",
                ),
                "description": openapi.Schema(
                    type=openapi.TYPE_STRING,
                    description="Description of the sub category of sub category",
                ),
                "image": openapi.Schema(
                    type=openapi.TYPE_FILE,  # Assuming image is a URL or base64-encoded data
                    description="URL or base64-encoded image data",
                ),
                "sub_category": openapi.Schema(
                    type=openapi.TYPE_STRING, description="Sub category uuid"
                ),
            },
            required=[],  # Add required fields if any
        ),
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
                            "non_binary_error": [],
                        },
                        "status": "failed",
                    }
                },
            ),
        },
    )
    def put(self, request, *args, **kwargs):
        """
        # Handle PUT request to update sub category of sub category.

        * Body params : Provide name , description ,image and sub category uuid.

        * Path params : Provide uuid of the sub category of sub category.

        * Query params : NA.

        * Request : A HTTP response of success message as json.

        """

        # receiving uuid
        subs_uuid = kwargs.get("subs_uuid")

        # error handling in the case of uuid absence
        if not subs_uuid:
            return HTTP_400("Sorry! you have to provide subs of subs uuid")

        # query and validation of sub sub category uuid
        try:
            subs_instance = SubofSub.objects.get(uuid=subs_uuid)
        except SubofSub.DoesNotExist:
            return HTTP_400("Sorry! Subs of Subs is not found in database or deleted")

        # deserialization
        subs_serializer = SubofSubSerializers(
            instance=subs_instance, data=request.data, partial=True
        )

        # validation of serializer
        if subs_serializer.is_valid():
            subs_serializer.save()
        else:
            return HTTP_400({"error": subs_serializer.errors})

        # success response
        return HTTP_200(
            {
                "message": "Subs of subs updated successfully",
                "subs_of": subs_serializer.data,
            }
        )

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                "subs_uuid",
                openapi.IN_PATH,
                description="UUID of the subs_uuid to delete , should pass as path params.",
                type=openapi.TYPE_STRING,
                required=True,
            ),
        ],
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
                            "non_binary_error": [],
                        },
                        "status": "failed",
                    }
                },
            ),
        },
    )
    def delete(self, request, *args, **kwargs):
        """
        # Handle DELETE request for delete sub category of sub category.

        * Path params : Provide uuid of sub of category of sub category.

        * Body params : NA.

        * Query params : NA.

        * Return : A HTTP response of success message as json.

        """

        # receiving uuid
        subs_uuid = kwargs.get("subs_uuid")

        # error handling in the case of uuid absence
        if not subs_uuid:
            return HTTP_400("Sorry! you have to provide subs of subs uuid")

        # query for sub sub category with error handling
        try:
            subs_instance = SubofSub.objects.get(uuid=subs_uuid)
        except SubofSub.DoesNotExist:
            return HTTP_400("Sorry! Subs of Subs is not found in database or deleted")

        # deletion of instance
        subs_instance.delete()

        # success response
        return HTTP_200("Subs of subs deleted successfully")


# products API's

search_param = openapi.Parameter(
    "search",
    openapi.IN_QUERY,
    description="Search products by name",
    type=openapi.TYPE_STRING,
)


class ProductsListCreateAPIview(APIView):
    """API for list create products"""

    @swagger_auto_schema(
        manual_parameters=[search_param],
        responses={
            "200": openapi.Response(
                description="API returns list of products.",
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

        * Query params : If search , provide search value in query with key of "search".

        * Path params : NA.

        * Body params : NA.

        * Return : A HTTP response with list of product data as json.

        """

        # Get the search query from the request parameters
        query = request.GET.get("search")

        # code snippet for search
        if query:
            product_instance = Product.objects.filter(
                Q(name__icontains=query)
                | Q(description__icontains=query)
                | Q(category__name__icontains=query)
                | Q(category__subcategory__name__icontains=query)
                | Q(category__subcategory__subofsub__name__icontains=query)
            )
        else:
            product_instance = Product.objects.all()

        # serialization
        product_serializer = ProductSerializer(product_instance, many=True)

        # success response
        return HTTP_200({"products": product_serializer.data})

    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "name": openapi.Schema(
                    type=openapi.TYPE_STRING, description="Name of the product."
                ),
                "description": openapi.Schema(
                    type=openapi.TYPE_STRING,
                    description="Description of the product.",
                ),
                "price": openapi.Schema(
                    type=openapi.TYPE_INTEGER,  # Assuming image is a URL or base64-encoded data
                    description="Price of the product.",
                ),
                "unit": openapi.Schema(
                    type=openapi.TYPE_STRING,
                    description="Unit of the product, uuid of model unit.",
                ),
                "qty": openapi.Schema(
                    type=openapi.TYPE_INTEGER, description="Quantity of the product."
                ),
                "image_one": openapi.Schema(
                    type=openapi.TYPE_FILE, description="Product of image."
                ),
                "image_two": openapi.Schema(
                    type=openapi.TYPE_FILE, description="Product of image."
                ),
                "image_three": openapi.Schema(
                    type=openapi.TYPE_FILE, description="Product of image."
                ),
                "image_four": openapi.Schema(
                    type=openapi.TYPE_FILE, description="Product of image."
                ),
                "image_five": openapi.Schema(
                    type=openapi.TYPE_FILE, description="Product of image."
                ),
                "status": openapi.Schema(
                    type=openapi.TYPE_BOOLEAN,
                    description="Status of the product (True or False).",
                ),
                "category": openapi.Schema(
                    type=openapi.TYPE_STRING,
                    description="Category of the product, uuid of model category.",
                ),
                "sold_by": openapi.Schema(
                    type=openapi.TYPE_STRING, description="Details of seller."
                ),
                "material": openapi.Schema(
                    type=openapi.TYPE_STRING, description="Material of product."
                ),
                "brand": openapi.Schema(
                    type=openapi.TYPE_STRING, description="Brand of material."
                ),
                "color": openapi.Schema(
                    type=openapi.TYPE_STRING, description="Color of product."
                ),
                "size": openapi.Schema(
                    type=openapi.TYPE_STRING, description="Size of product."
                ),
                "warranty": openapi.Schema(
                    type=openapi.TYPE_INTEGER, description="Warranty of product."
                ),
                "number_of_box": openapi.Schema(
                    type=openapi.TYPE_INTEGER, description="Number of boxes."
                ),
                "features": openapi.Schema(
                    type=openapi.TYPE_STRING, description="Feature of product."
                ),
                "country_of_origin": openapi.Schema(
                    type=openapi.TYPE_STRING, description="Country of origin."
                ),
                "video": openapi.Schema(
                    type=openapi.TYPE_FILE, description="Video of product."
                ),
                "is_featured": openapi.Schema(
                    type=openapi.TYPE_BOOLEAN,
                    description="Is product featured(True or False).",
                ),
                "created_at": openapi.Schema(
                    type=openapi.TYPE_STRING,
                    description="Date of creation.",
                    format=openapi.FORMAT_DATE,
                ),
            },
            required=[],  # Add required fields if any
        ),
        responses={
            "200": openapi.Response(
                description="API returns success message.",
                examples={
                    "application/json": {
                        "message": "Product is created successfully.",
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
        # Handle POST request to create products.

        * Path params : NA.

        * Query params : NA.

        * Body params : Provide params as required to create product.

        * Return : A HTTP response of success message as json.
        """

        # deserialization
        product_serializer = ProductSerializer(data=request.data)

        # assigning category uuid to variable from request data
        category_uuid = request.data.get("category")
        category = None

        # query for category with error handling
        if category_uuid:
            try:
                category = Category.objects.get(uuid=category_uuid)
            except Category.DoesNotExist:
                return HTTP_400({"error": "Category not found in database"})
        # serializer validation
        if not product_serializer.is_valid():
            return HTTP_400({"error": product_serializer.errors})

        product_serializer.save(category=category)

        # success response
        return HTTP_200(
            {"message": "Product is created", "product": product_serializer.data}
        )


class ProductCRUDApi(APIView):
    """
    API for CRUD operations on products.

    This API provides endpoints for creating, reading, updating, and deleting products.
    """

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                "product_uuid",
                openapi.IN_PATH,
                description="UUID of the product_uuid to list , should pass as path params.",
                type=openapi.TYPE_STRING,
                required=True,
            ),
        ],
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
        # Handle GET request to list product.

        * Path params : Provide uuid of product to list.

        * Query params : NA.

        * Body params : NA.

        * Return : A HTTP response of success message as json.
        """

        # Get the product UUID from the request
        product_uuid = kwargs.get("product_uuid")

        # Check if the product UUID is provided
        if not product_uuid:
            return HTTP_400({"error": "Sorry ! you need to provide product uuid"})

        # Try to retrieve the product instance
        try:
            product_instance = Product.objects.get(uuid=product_uuid)
        except Product.DoesNotExist:
            return HTTP_400(
                {"error": "Sorry! product is not found in database or deleted"}
            )

        # serialization
        product_serializer = ProductSerializer(product_instance)

        # success response
        return HTTP_200({"product": product_serializer.data})

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                "product_uuid",
                openapi.IN_PATH,
                description="UUID of the product_uuid to update , should pass as path params.",
                type=openapi.TYPE_STRING,
                required=True,
            ),
        ],
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "name": openapi.Schema(
                    type=openapi.TYPE_STRING, description="Name of the product."
                ),
                "description": openapi.Schema(
                    type=openapi.TYPE_STRING,
                    description="Description of the product.",
                ),
                "price": openapi.Schema(
                    type=openapi.TYPE_INTEGER,  # Assuming image is a URL or base64-encoded data
                    description="Price of the product.",
                ),
                "unit": openapi.Schema(
                    type=openapi.TYPE_STRING,
                    description="Unit of the product, uuid of model unit.",
                ),
                "qty": openapi.Schema(
                    type=openapi.TYPE_INTEGER, description="Quantity of the product."
                ),
                "image_one": openapi.Schema(
                    type=openapi.TYPE_FILE, description="Product of image."
                ),
                "image_two": openapi.Schema(
                    type=openapi.TYPE_FILE, description="Product of image."
                ),
                "image_three": openapi.Schema(
                    type=openapi.TYPE_FILE, description="Product of image."
                ),
                "image_four": openapi.Schema(
                    type=openapi.TYPE_FILE, description="Product of image."
                ),
                "image_five": openapi.Schema(
                    type=openapi.TYPE_FILE, description="Product of image."
                ),
                "status": openapi.Schema(
                    type=openapi.TYPE_BOOLEAN,
                    description="Status of the product (True or False).",
                ),
                "category": openapi.Schema(
                    type=openapi.TYPE_STRING,
                    description="Category of the product, uuid of model category.",
                ),
                "sold_by": openapi.Schema(
                    type=openapi.TYPE_STRING, description="Details of seller."
                ),
                "material": openapi.Schema(
                    type=openapi.TYPE_STRING, description="Material of product."
                ),
                "brand": openapi.Schema(
                    type=openapi.TYPE_STRING, description="Brand of material."
                ),
                "color": openapi.Schema(
                    type=openapi.TYPE_STRING, description="Color of product."
                ),
                "size": openapi.Schema(
                    type=openapi.TYPE_STRING, description="Size of product."
                ),
                "warranty": openapi.Schema(
                    type=openapi.TYPE_INTEGER, description="Warranty of product."
                ),
                "number_of_box": openapi.Schema(
                    type=openapi.TYPE_INTEGER, description="Number of boxes."
                ),
                "features": openapi.Schema(
                    type=openapi.TYPE_STRING, description="Feature of product."
                ),
                "country_of_origin": openapi.Schema(
                    type=openapi.TYPE_STRING, description="Country of origin."
                ),
                "video": openapi.Schema(
                    type=openapi.TYPE_FILE, description="Video of product."
                ),
                "is_featured": openapi.Schema(
                    type=openapi.TYPE_BOOLEAN,
                    description="Is product featured(True or False).",
                ),
                "created_at": openapi.Schema(
                    type=openapi.TYPE_STRING,
                    description="Date of creation.",
                    format=openapi.FORMAT_DATE,
                ),
            },
            required=[],  # Add required fields if any
        ),
        responses={
            "200": openapi.Response(
                description="API returns success message.",
                examples={
                    "application/json": {
                        "message": "Product is updated successfully.",
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
    def put(self, request, *args, **kwargs):
        """
        # Handle PUT request to update product.

        * Path params : Provide uuid of the product.

        * Body params : NA.

        * Query params : NA.

        * Return : A HTTP responses of success message as json.
        """

        # receiving uuid of product
        product_uuid = kwargs.get("product_uuid")

        # error handling in the case of uuid absence
        if not product_uuid:
            return HTTP_400({"error": "Sorry ! you need to provide product uuid"})

        # query for product with error handling
        try:
            product_instance = Product.objects.get(uuid=product_uuid)
        except Product.DoesNotExist:
            return HTTP_400(
                {"error": "Sorry! product is not found in database or deleted"}
            )

        # assigning category uuid to variable
        category_uuid = request.data.get("category")
        category = None

        # query for category with error handling
        if category_uuid:
            try:
                category = Category.objects.get(uuid=category_uuid)
            except Category.DoesNotExist:
                return HTTP_400(
                    {"error": "Sorry! Category is not found in database or deleted"}
                )

        # deserialization
        product_serializer = ProductSerializer(
            instance=product_instance, data=request.data, partial=True
        )

        # validation of serializer
        if not product_serializer.is_valid():
            return HTTP_400({"error": product_serializer.errors})
        product_serializer.save(category=category)

        # success response
        return HTTP_200(
            {
                "message": "Product is updated successfully",
                "product": product_serializer.data,
            }
        )

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                "product_uuid",
                openapi.IN_PATH,
                description="UUID of the product_uuid to delete , should pass as path params.",
                type=openapi.TYPE_STRING,
                required=True,
            ),
        ],
        responses={
            "200": openapi.Response(
                description="API returns success message.",
                examples={
                    "application/json": {
                        "message": "Product is deleted successfully.",
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
    def delete(self, request, *args, **kwargs):
        """
        # Handle DELETE request to delete product.

        * Path params : Provide uuid of product to delete.

        * Body params : NA.

        * Query params : NA.

        * Return : A HTTP response of success as json.
        """

        # receiving product uuid
        product_uuid = kwargs.get("product_uuid")

        # error handling in the case of uuid absence
        if not product_uuid:
            return HTTP_400({"error": "Sorry ! you need to provide product uuid"})

        # query for product with error handling
        try:
            product_instance = Product.objects.get(uuid=product_uuid)
        except Product.DoesNotExist:
            return HTTP_400(
                {"error": "Sorry! product is not found in database or deleted"}
            )

        # deletion of product instance
        product_instance.delete()

        # success response
        return HTTP_200({"message": "Product deleted successfully"})


search_param = openapi.Parameter(
    "search",
    openapi.IN_QUERY,
    description="Search products by name.",
    type=openapi.TYPE_STRING,
)


# separate api for search products
class SearchProductAPI(APIView):
    """
    API for searching products.

    This API provides a single endpoint for searching products based on a query string.
    """

    @swagger_auto_schema(
        manual_parameters=[search_param],
        responses={
            "200": openapi.Response(
                description="API returns list of products if search query is valid.",
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
        # Handle GET request to search products.

        * Path params : NA.

        * Body params : NA.

        * Query params : NA.

        * Return : A HTTP response of success message as json.
        """

        # Get the search query from the request
        query = request.GET.get("search")

        # Check if the search query is provided
        if not query:
            return HTTP_400({"error": "Sorry! you need to provide search query"})

        # Filter products based on the search query
        product_instance = Product.objects.filter(
            Q(name__icontains=query)
            | Q(description__icontains=query)
            | Q(category__name__icontains=query)
            | Q(category__subcategory__name__icontains=query)
            | Q(category__subcategory__subofsub__name__icontains=query)
        )

        # Serialize the filtered products
        product_serializer = ProductSerializer(product_instance, many=True)

        # Return a 200 success response with the filtered products
        return HTTP_200({"product": product_serializer.data})




class ProductListbyCategory(APIView):
    """
    # Handle GET request to list products by category.

    """

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                "category, sub category and sub of sub category",
                openapi.IN_PATH,
                description="Listing of product by category subcategory and subofsub category",
                type=openapi.TYPE_STRING,
                required=True,
            ),
        ],
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

    def  get(self, request, *args, **kwargs):
        """
        Handle GET request to list products by category.
        
        *  Path params : Provide  category id.
        *  Body params : NA.
        *  Query params : NA.
        *  Return : A HTTP response of success message as json.

        """

        # Get the category id from the path
        uuid = kwargs.get("uuid")

          # Check if the category id is provided
        if not uuid:
            return HTTP_400({"error": "Sorry! you need to provide category id"})
    
        # Get identifier for select  category sub category  and sub of sub category.
        identifier = kwargs.get("identifier")

        if not identifier:
            return HTTP_400(
                error="Identifier is required to list products by category."
            )
        
        identifier_list = ["category","sub_category","sub_of_sub"]
        
        if identifier == "category":
            try:
                category = Category.objects.get(uuid=uuid)
            except Category.DoesNotExist:
                return HTTP_400({"error": "Category not found"})
            products = Product.objects.filter(category=uuid)
        elif identifier == "sub_category":
            try:
                sub_category = Subcategory.objects.get(uuid=uuid)
            except Subcategory.DoesNotExist:
                return HTTP_400({"error": "Sub category not found"})
            
            products = Product.objects.filter(sub_category=uuid)
        elif identifier == "sub_of_sub":
            try:
                sub_of_sub = SubofSub.objects.get(uuid=uuid)
            except SubofSub.DoesNotExist:
                return HTTP_400({"error": "Sub of sub category not found"})
            
            products = Product.objects.filter(sub_of_sub=uuid)
        elif identifier not in  identifier_list:
            return HTTP_400(
                "Invalid identifier. Please select category, sub_category or sub_of_sub."
                )
      
        # Serialize the filtered products
        product_serializer = ProductSerializer(products, many=True)
        # Return a 200 success response with the filtered products
        return HTTP_200({"product": product_serializer.data})

        



