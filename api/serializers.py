from rest_framework import serializers

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


# =========================================================
# USER PROFILE
# =========================================================

class UserProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserProfile
        fields = "__all__"

        read_only_fields = [
            "id",
            "supabase_user_id",
            "email",
            "created_at",
        ]


# =========================================================
# REFERENCE IMAGE
# =========================================================

class ReferenceImageSerializer(serializers.ModelSerializer):

    class Meta:
        model = ReferenceImage
        fields = "__all__"

        read_only_fields = [
            "id",
            "user",
            "created_at",
        ]


# =========================================================
# EDITING PROFILE
# =========================================================

class EditingProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = EditingProfile
        fields = "__all__"

        read_only_fields = [
            "id",
            "user",
            "created_at",
            "updated_at",
        ]


# =========================================================
# PROJECT
# =========================================================

class ProjectSerializer(serializers.ModelSerializer):

    class Meta:
        model = Project
        fields = "__all__"

        read_only_fields = [
            "id",
            "user",
            "created_at",
        ]


# =========================================================
# EXPORT
# =========================================================

class ExportSerializer(serializers.ModelSerializer):

    class Meta:
        model = Export
        fields = "__all__"

        read_only_fields = [
            "id",
            "created_at",
        ]


# =========================================================
# UPLOADED IMAGE
# =========================================================

class UploadedImageSerializer(serializers.ModelSerializer):

    class Meta:
        model = UploadedImage
        fields = "__all__"

        read_only_fields = [
            "id",
            "user",
            "created_at",
        ]


# =========================================================
# DEMO PROMPT
# =========================================================

class DemoPromptSerializer(serializers.ModelSerializer):

    class Meta:
        model = DemoPrompt
        fields = "__all__"

        read_only_fields = [
            "id",
            "created_at",
        ]


# =========================================================
# FEATURE EXPLANATION
# =========================================================

class FeatureExplanationSerializer(serializers.ModelSerializer):

    class Meta:
        model = FeatureExplanation
        fields = "__all__"

        read_only_fields = [
            "id",
            "created_at",
        ]


# =========================================================
# REGENERATION
# =========================================================

class RegenerationSerializer(serializers.ModelSerializer):

    class Meta:
        model = Regeneration
        fields = "__all__"

        read_only_fields = [
            "id",
            "created_at",
            "generation_number",
        ]