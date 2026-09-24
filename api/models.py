from django.db import models


# =========================================================
# USER PROFILE
# =========================================================

class UserProfile(models.Model):

    supabase_user_id = models.CharField(
        max_length=255,
        unique=True
    )

    email = models.EmailField()

    name = models.CharField(
        max_length=150,
        blank=True
    )

    profile_picture = models.ImageField(
        upload_to="profile_pictures/",
        blank=True,
        null=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    @property
    def is_authenticated(self):
        return True

    def __str__(self):
        return self.email


# =========================================================
# REFERENCE IMAGES
# =========================================================

class ReferenceImage(models.Model):

    user = models.ForeignKey(
        UserProfile,
        on_delete=models.CASCADE,
        related_name="reference_images"
    )

    image_url = models.URLField()

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return f"Reference Image {self.id}"


# =========================================================
# EDITING PROFILES
# =========================================================

class EditingProfile(models.Model):

    user = models.ForeignKey(
        UserProfile,
        on_delete=models.CASCADE,
        related_name="editing_profiles"
    )

    name = models.CharField(
        max_length=150
    )

    lightness = models.FloatField(default=0)
    contrast = models.FloatField(default=0)
    warmth = models.FloatField(default=0)
    tint = models.FloatField(default=0)
    saturation = models.FloatField(default=0)

    curve = models.JSONField(default=dict)
    hsl = models.JSONField(default=dict)

    fade = models.FloatField(default=0)
    highlight = models.FloatField(default=0)
    shadow = models.FloatField(default=0)
    color = models.FloatField(default=0)
    hue = models.FloatField(default=0)
    vignette = models.FloatField(default=0)
    sharpen = models.FloatField(default=0)
    grain = models.FloatField(default=0)

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    def __str__(self):
        return self.name


# =========================================================
# PROJECTS
# =========================================================

class Project(models.Model):

    user = models.ForeignKey(
        UserProfile,
        on_delete=models.CASCADE,
        related_name="projects"
    )

    name = models.CharField(
        max_length=150
    )

    original_image_url = models.URLField(
        blank=True
    )

    edited_image_url = models.URLField(
        blank=True
    )

    editing_profile = models.ForeignKey(
        EditingProfile,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return self.name


# =========================================================
# EXPORTS
# =========================================================

class Export(models.Model):

    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        related_name="exports"
    )

    file_url = models.URLField()

    file_type = models.CharField(
        max_length=20
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return f"Export {self.id}"


# =========================================================
# UPLOADED IMAGES
# =========================================================

class UploadedImage(models.Model):

    user = models.ForeignKey(
        UserProfile,
        on_delete=models.CASCADE,
        related_name="uploaded_images"
    )

    image = models.ImageField(
        upload_to="uploads/"
    )

    image_type = models.CharField(
        max_length=20,
        choices=[
            ("reference", "Reference"),
            ("original", "Original"),
        ]
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return f"{self.image_type} image {self.id}"


# =========================================================
# DEMO PROMPTS / EXAMPLES
# =========================================================

class DemoPrompt(models.Model):

    title = models.CharField(
        max_length=150
    )

    description = models.TextField(
        blank=True
    )

    prompt = models.TextField()

    example_image_url = models.URLField(
        blank=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return self.title


# =========================================================
# FEATURE EXPLANATIONS
# =========================================================

class FeatureExplanation(models.Model):

    feature_name = models.CharField(
        max_length=100,
        unique=True
    )

    short_description = models.CharField(
        max_length=255
    )

    detailed_explanation = models.TextField()

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return self.feature_name


# =========================================================
# REGENERATIONS
# =========================================================

class Regeneration(models.Model):

    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        related_name="regenerations"
    )

    generation_number = models.PositiveIntegerField()

    image_url = models.URLField()

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return f"{self.project.name} - Generation {self.generation_number}"