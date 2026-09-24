import os
import cv2

from django.conf import settings

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import (
    EditingProfile,
    Project,
    Regeneration,
)

from style_editor import apply_style


# =========================================================
# APPLY STYLE API
# =========================================================

@api_view(["POST"])
@permission_classes([IsAuthenticated])
def apply_style_api(request):

    profile_id = request.data.get("profile_id")
    project_id = request.data.get("project_id")

    if not profile_id:
        return Response(
            {"error": "profile_id is required."},
            status=400
        )

    if not project_id:
        return Response(
            {"error": "project_id is required."},
            status=400
        )

    try:
        profile = EditingProfile.objects.get(
            id=profile_id,
            user=request.user
        )
    except EditingProfile.DoesNotExist:
        return Response(
            {"error": "Editing profile not found."},
            status=404
        )

    try:
        project = Project.objects.get(
            id=project_id,
            user=request.user
        )
    except Project.DoesNotExist:
        return Response(
            {"error": "Project not found."},
            status=404
        )

    if not project.original_image_url:
        return Response(
            {"error": "Project does not have an original image."},
            status=400
        )

    image_url = project.original_image_url

    media_prefix = "/media/"

    if media_prefix not in image_url:
        return Response(
            {"error": "Invalid image URL."},
            status=400
        )

    relative_path = image_url.split(
        media_prefix,
        1
    )[1]

    image_path = os.path.join(
        settings.MEDIA_ROOT,
        relative_path
    )

    if not os.path.exists(image_path):
        return Response(
            {"error": "Original image file not found."},
            status=404
        )

    profile_data = {
        "lightness": profile.lightness,
        "contrast": profile.contrast,
        "warmth": profile.warmth,
        "tint": profile.tint,
        "saturation": profile.saturation,
        "highlight": profile.highlight,
        "shadow": profile.shadow,
        "hue": profile.hue,
    }

    try:
        edited_image = apply_style(
            image_path,
            profile_data
        )
    except Exception as e:
        return Response(
            {
                "error": "Failed to apply style.",
                "details": str(e)
            },
            status=500
        )

    output_filename = (
        f"edited_project_{project.id}.jpg"
    )

    output_path = os.path.join(
        settings.MEDIA_ROOT,
        output_filename
    )

    success = cv2.imwrite(
        output_path,
        edited_image
    )

    if not success:
        return Response(
            {"error": "Failed to save edited image."},
            status=500
        )

    edited_image_url = (
        request.build_absolute_uri(
            settings.MEDIA_URL +
            output_filename
        )
    )

    project.edited_image_url = edited_image_url

    project.save(
        update_fields=[
            "edited_image_url"
        ]
    )

    return Response({
        "message": "Style applied successfully.",
        "project_id": project.id,
        "profile_id": profile.id,
        "original_image_url": project.original_image_url,
        "edited_image_url": edited_image_url
    })


# =========================================================
# REGENERATE API
# =========================================================

@api_view(["POST"])
@permission_classes([IsAuthenticated])
def regenerate_api(request, project_id):

    # -----------------------------------------------------
    # Get user's project
    # -----------------------------------------------------

    try:

        project = Project.objects.get(
            id=project_id,
            user=request.user
        )

    except Project.DoesNotExist:

        return Response(
            {
                "error":
                "Project not found."
            },
            status=404
        )

    # -----------------------------------------------------
    # Check editing profile
    # -----------------------------------------------------

    if not project.editing_profile:

        return Response(
            {
                "error":
                "Project does not have an editing profile."
            },
            status=400
        )

    # -----------------------------------------------------
    # Check original image
    # -----------------------------------------------------

    if not project.original_image_url:

        return Response(
            {
                "error":
                "Project does not have an original image."
            },
            status=400
        )

    # -----------------------------------------------------
    # Convert image URL to local file path
    # -----------------------------------------------------

    image_url = project.original_image_url

    media_prefix = "/media/"

    if media_prefix not in image_url:

        return Response(
            {
                "error":
                "Invalid original image URL."
            },
            status=400
        )

    relative_path = image_url.split(
        media_prefix,
        1
    )[1]

    image_path = os.path.join(
        settings.MEDIA_ROOT,
        relative_path
    )

    if not os.path.exists(image_path):

        return Response(
            {
                "error":
                "Original image file not found."
            },
            status=404
        )

    # -----------------------------------------------------
    # Get editing profile
    # -----------------------------------------------------

    profile = project.editing_profile

    profile_data = {

        "lightness":
        profile.lightness,

        "contrast":
        profile.contrast,

        "warmth":
        profile.warmth,

        "tint":
        profile.tint,

        "saturation":
        profile.saturation,

        "highlight":
        profile.highlight,

        "shadow":
        profile.shadow,

        "hue":
        profile.hue,
    }

    # -----------------------------------------------------
    # Apply style again
    # -----------------------------------------------------

    try:

        regenerated_image = apply_style(
            image_path,
            profile_data
        )

    except Exception as e:

        return Response(
            {
                "error":
                "Failed to regenerate image.",

                "details":
                str(e)
            },
            status=500
        )

    # -----------------------------------------------------
    # Find next generation number
    # -----------------------------------------------------

    last_generation = (
        Regeneration.objects
        .filter(
            project=project
        )
        .order_by(
            "-generation_number"
        )
        .first()
    )

    if last_generation:

        generation_number = (
            last_generation.generation_number + 1
        )

    else:

        generation_number = 1

    # -----------------------------------------------------
    # Save regenerated image
    # -----------------------------------------------------

    output_filename = (
        f"regenerated_project_"
        f"{project.id}_"
        f"generation_"
        f"{generation_number}.jpg"
    )

    output_path = os.path.join(
        settings.MEDIA_ROOT,
        output_filename
    )

    success = cv2.imwrite(
        output_path,
        regenerated_image
    )

    if not success:

        return Response(
            {
                "error":
                "Failed to save regenerated image."
            },
            status=500
        )

    # -----------------------------------------------------
    # Create URL
    # -----------------------------------------------------

    regenerated_image_url = (
        request.build_absolute_uri(
            settings.MEDIA_URL +
            output_filename
        )
    )

    # -----------------------------------------------------
    # Save regeneration in database
    # -----------------------------------------------------

    regeneration = Regeneration.objects.create(

        project=project,

        generation_number=
        generation_number,

        image_url=
        regenerated_image_url
    )

    # -----------------------------------------------------
    # Update latest project image
    # -----------------------------------------------------

    project.edited_image_url = (
        regenerated_image_url
    )

    project.save(
        update_fields=[
            "edited_image_url"
        ]
    )

    # -----------------------------------------------------
    # Response
    # -----------------------------------------------------

    return Response({

        "message":
        "Image regenerated successfully.",

        "project_id":
        project.id,

        "generation_id":
        regeneration.id,

        "generation_number":
        regeneration.generation_number,

        "image_url":
        regeneration.image_url,

        "created_at":
        regeneration.created_at,
    })