import os

from django.core.files.storage import default_storage
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from .models import UploadedImage, EditingProfile
from .style_analyzer import analyze_image


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def create_style_profile_api(request):

    # --------------------------------
    # Get uploaded image
    # --------------------------------

    image = request.FILES.get("image")

    if not image:
        return Response(
            {"error": "Please upload an image."},
            status=status.HTTP_400_BAD_REQUEST
        )

    # --------------------------------
    # Save uploaded reference image
    # --------------------------------

    uploaded_image = UploadedImage.objects.create(
        user=request.user,
        image=image,
        image_type="reference"
    )

    # --------------------------------
    # Get actual file path
    # --------------------------------

    image_path = uploaded_image.image.path

    # --------------------------------
    # Analyze image using OpenCV
    # --------------------------------

    try:
        style_values = analyze_image(image_path)

    except Exception as e:

        uploaded_image.delete()

        return Response(
            {
                "error": "Image analysis failed.",
                "details": str(e)
            },
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

    # --------------------------------
    # Create Editing Profile
    # --------------------------------

    profile_name = request.data.get(
        "name",
        "AI Generated Style"
    )

    profile = EditingProfile.objects.create(
        user=request.user,
        name=profile_name,

        lightness=style_values["lightness"],
        contrast=style_values["contrast"],
        warmth=style_values["warmth"],
        tint=style_values["tint"],
        saturation=style_values["saturation"],

        curve=style_values["curve"],
        hsl=style_values["hsl"],

        fade=style_values["fade"],
        highlight=style_values["highlight"],
        shadow=style_values["shadow"],
        color=style_values["color"],
        hue=style_values["hue"],
        vignette=style_values["vignette"],
        sharpen=style_values["sharpen"],
        grain=style_values["grain"],
    )

    # --------------------------------
    # Return result
    # --------------------------------

    return Response(
        {
            "message": "Style profile generated successfully.",

            "profile_id": profile.id,

            "profile_name": profile.name,

            "reference_image_id": uploaded_image.id,

            "style": style_values,
        },
        status=status.HTTP_201_CREATED
    )