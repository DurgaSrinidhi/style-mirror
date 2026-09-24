from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import ValidationError
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response

from .models import (
    UserProfile,
    ReferenceImage,
    EditingProfile,
    Project,
    Export,
    UploadedImage,
    DemoPrompt,
    FeatureExplanation,
    Regeneration,
)

from .serializers import (
    UserProfileSerializer,
    ReferenceImageSerializer,
    EditingProfileSerializer,
    ProjectSerializer,
    ExportSerializer,
    UploadedImageSerializer,
    DemoPromptSerializer,
    FeatureExplanationSerializer,
    RegenerationSerializer,
)


# =========================================================
# USER PROFILE
# =========================================================

class UserProfileViewSet(viewsets.ModelViewSet):

    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):

        return UserProfile.objects.filter(
            id=self.request.user.id
        )

    http_method_names = [
        "get",
        "patch",
        "head",
        "options"
    ]


# =========================================================
# REFERENCE IMAGES
# =========================================================

class ReferenceImageViewSet(viewsets.ModelViewSet):

    serializer_class = ReferenceImageSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):

        return ReferenceImage.objects.filter(
            user=self.request.user
        )

    def perform_create(self, serializer):

        serializer.save(
            user=self.request.user
        )


# =========================================================
# EDITING PROFILES
# =========================================================

class EditingProfileViewSet(viewsets.ModelViewSet):

    serializer_class = EditingProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):

        return EditingProfile.objects.filter(
            user=self.request.user
        )

    def perform_create(self, serializer):

        serializer.save(
            user=self.request.user
        )


# =========================================================
# PROJECTS
# =========================================================

class ProjectViewSet(viewsets.ModelViewSet):

    serializer_class = ProjectSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):

        return Project.objects.filter(
            user=self.request.user
        )

    def perform_create(self, serializer):

        editing_profile = serializer.validated_data.get(
            "editing_profile"
        )

        if (
            editing_profile
            and editing_profile.user != self.request.user
        ):

            raise ValidationError({
                "editing_profile":
                "You do not own this editing profile."
            })

        serializer.save(
            user=self.request.user
        )


# =========================================================
# EXPORTS
# =========================================================

class ExportViewSet(viewsets.ModelViewSet):

    serializer_class = ExportSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):

        return Export.objects.filter(
            project__user=self.request.user
        )

    def perform_create(self, serializer):

        project = serializer.validated_data.get(
            "project"
        )

        if project.user != self.request.user:

            raise ValidationError({
                "project":
                "You do not own this project."
            })

        serializer.save()


# =========================================================
# UPLOADED IMAGES
# =========================================================

class UploadedImageViewSet(viewsets.ModelViewSet):

    serializer_class = UploadedImageSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):

        return UploadedImage.objects.filter(
            user=self.request.user
        )

    def perform_create(self, serializer):

        serializer.save(
            user=self.request.user
        )


# =========================================================
# DEMO PROMPTS
# =========================================================

class DemoPromptViewSet(viewsets.ModelViewSet):

    serializer_class = DemoPromptSerializer
    permission_classes = [IsAuthenticated]

    queryset = DemoPrompt.objects.all()

    http_method_names = [
        "get",
        "post",
        "head",
        "options"
    ]


# =========================================================
# FEATURE EXPLANATIONS
# =========================================================

class FeatureExplanationViewSet(viewsets.ModelViewSet):

    serializer_class = FeatureExplanationSerializer
    permission_classes = [IsAuthenticated]

    queryset = FeatureExplanation.objects.all()

    http_method_names = [
        "get",
        "post",
        "head",
        "options"
    ]


# =========================================================
# REGENERATIONS
# =========================================================

class RegenerationViewSet(viewsets.ModelViewSet):

    serializer_class = RegenerationSerializer
    permission_classes = [IsAuthenticated]

    http_method_names = [
        "get",
        "post",
        "head",
        "options"
    ]

    def get_queryset(self):

        return Regeneration.objects.filter(
            project__user=self.request.user
        ).order_by(
            "project_id",
            "generation_number"
        )

    def perform_create(self, serializer):

        project = serializer.validated_data.get(
            "project"
        )

        # Make sure the project belongs to the logged-in user
        if project.user != self.request.user:

            raise ValidationError({
                "project":
                "You do not own this project."
            })

        # Find the latest generation for this project
        last_generation = (
            Regeneration.objects
            .filter(project=project)
            .order_by("-generation_number")
            .first()
        )

        if last_generation:

            next_generation = (
                last_generation.generation_number + 1
            )

        else:

            next_generation = 1

        serializer.save(
            generation_number=next_generation
        )


# =========================================================
# HISTORY API
# =========================================================

@api_view(["GET"])
@permission_classes([IsAuthenticated])
def history_api(request):

    projects = Project.objects.filter(
        user=request.user
    ).order_by(
        "-created_at"
    )

    history = []

    for project in projects:

        history.append({

            "project_id":
                project.id,

            "project_name":
                project.name,

            "original_image_url":
                project.original_image_url,

            "edited_image_url":
                project.edited_image_url,

            "editing_profile":
                (
                    project.editing_profile.name
                    if project.editing_profile
                    else None
                ),

            "created_at":
                project.created_at,

            "regenerations": [
                {
                    "id": regeneration.id,
                    "generation_number":
                        regeneration.generation_number,
                    "image_url":
                        regeneration.image_url,
                    "created_at":
                        regeneration.created_at,
                }

                for regeneration
                in project.regenerations.all()
            ],
        })

    return Response({

        "count":
            len(history),

        "history":
            history,
    })
from django.shortcuts import render


def style_mirror_home(request):
    return render(
        request,
        "style_mirror/index.html"
    )