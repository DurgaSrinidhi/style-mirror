import os
import tempfile

import cv2
import requests

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import (
    EditingProfile,
    Project,
    Regeneration,
)

from .supabase_storage import upload_file

from style_editor import apply_style


# =========================================================
# DOWNLOAD IMAGE FROM URL
# =========================================================

def download_image_from_url(image_url):
    """
    Download an image from a URL into a temporary local file.
    OpenCV needs a local file to process the image.
    """

    response = requests.get(
        image_url,
        timeout=60
    )

    response.raise_for_status()

    temp_file = tempfile.NamedTemporaryFile(
        suffix=".jpg",
        delete=False
    )

    temp_file.write(response.content)
    temp_file.close()

    return temp_file.name


# =========================================================
# SAVE OPENCV IMAGE TO TEMP FILE
# =========================================================

def save_opencv_image_to_temp(image):
    """
    Save an OpenCV image into a temporary JPEG file.
    """

    temp_file = tempfile.NamedTemporaryFile(
        suffix=".jpg",
        delete=False
    )

    temp_path = temp_file.name
    temp_file.close()

    success = cv2.imwrite(
        temp_path,
        image
    )

    if not success:
        raise RuntimeError(
            "Failed to save processed image."
        )

    return temp_path


# =========================================================
# APPLY STYLE API
# =========================================================

@api_view(["POST"])
@permission_classes([IsAuthenticated])
def apply_style_api(request):

    profile_id = request.data.get("profile_id")
    project_id = request.data.get("project_id")

    # -----------------------------------------------------
    # Validate profile ID
    # -----------------------------------------------------

    if not profile_id:

        return Response(
            {
                "error":
                "profile_id is required."
            },
            status=400
        )

    # -----------------------------------------------------
    # Validate project ID
    # -----------------------------------------------------

    if not project_id:

        return Response(
            {
                "error":
                "project_id is required."
            },
            status=400
        )

    # -----------------------------------------------------
    # Get editing profile
    # -----------------------------------------------------

    try:

        profile = EditingProfile.objects.get(
            id=profile_id,
            user=request.user
        )

    except EditingProfile.DoesNotExist:

        return Response(
            {
                "error":
                "Editing profile not found."
            },
            status=404
        )

    # -----------------------------------------------------
    # Get project
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

    image_path = None
    output_path = None

    try:

        # -------------------------------------------------
        # Download original image
        # -------------------------------------------------

        image_path = download_image_from_url(
            project.original_image_url
        )

        # -------------------------------------------------
        # Editing profile values
        # -------------------------------------------------

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

        # -------------------------------------------------
        # Apply STYLE MIRROR editing
        # -------------------------------------------------

        edited_image = apply_style(
            image_path,
            profile_data
        )

        # -------------------------------------------------
        # Save result temporarily
        # -------------------------------------------------

        output_path = save_opencv_image_to_temp(
            edited_image
        )

        # -------------------------------------------------
        # Upload edited image to Supabase
        # -------------------------------------------------

        edited_image_url = upload_file(
            output_path,
            folder="edited"
        )

    except requests.RequestException as e:

        return Response(
            {
                "error":
                "Could not download the original image.",

                "details":
                str(e)
            },
            status=500
        )

    except Exception as e:

        return Response(
            {
                "error":
                "Failed to apply style.",

                "details":
                str(e)
            },
            status=500
        )

    finally:

        # -------------------------------------------------
        # Remove temporary files
        # -------------------------------------------------

        if image_path and os.path.exists(image_path):

            os.remove(image_path)

        if output_path and os.path.exists(output_path):

            os.remove(output_path)

    # -----------------------------------------------------
    # Save Supabase URL in database
    # -----------------------------------------------------

    project.edited_image_url = edited_image_url

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
        "Style applied successfully.",

        "project_id":
        project.id,

        "profile_id":
        profile.id,

        "original_image_url":
        project.original_image_url,

        "edited_image_url":
        edited_image_url
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

    image_path = None
    output_path = None

    try:

        # -------------------------------------------------
        # Download original image
        # -------------------------------------------------

        image_path = download_image_from_url(
            project.original_image_url
        )

        # -------------------------------------------------
        # Get editing profile
        # -------------------------------------------------

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

        # -------------------------------------------------
        # Apply style again
        # -------------------------------------------------

        regenerated_image = apply_style(
            image_path,
            profile_data
        )

        # -------------------------------------------------
        # Save regenerated image temporarily
        # -------------------------------------------------

        output_path = save_opencv_image_to_temp(
            regenerated_image
        )

        # -------------------------------------------------
        # Upload to Supabase
        # -------------------------------------------------

        regenerated_image_url = upload_file(
            output_path,
            folder="regenerated"
        )

    except requests.RequestException as e:

        return Response(
            {
                "error":
                "Could not download the original image.",

                "details":
                str(e)
            },
            status=500
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

    finally:

        # -------------------------------------------------
        # Remove temporary files
        # -------------------------------------------------

        if image_path and os.path.exists(image_path):

            os.remove(image_path)

        if output_path and os.path.exists(output_path):

            os.remove(output_path)

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