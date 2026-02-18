from django import template
from django.conf import settings
import os

register = template.Library()

@register.filter
def thumbnail_url(image_url):
    """
    Thumbnail URL generate karta hai by matching filename
    irrespective of extension.

    Priority:
    webp > jpg > jpeg > png
    """

    if not image_url:
        return image_url

    image_url = str(image_url)

    # URL parts
    parts = image_url.split("/")
    original_filename = parts[-1]              # photo.jpg
    folder = "/".join(parts[:-1])               # /media/upload

    # base name nikalo (photo)
    base_name = os.path.splitext(original_filename)[0]

    # thumbnail folder (filesystem path)
    thumb_dir = os.path.join(
        settings.MEDIA_ROOT,
        folder.replace(settings.MEDIA_URL, "").strip("/"),
        "thumbnails"
    )

    # extensions priority
    extensions = ["webp", "jpg", "jpeg", "png"]

    for ext in extensions:
        thumb_file = f"{base_name}.{ext}"
        thumb_path = os.path.join(thumb_dir, thumb_file)

        if os.path.exists(thumb_path):
            return f"{folder}/thumbnails/{thumb_file}"

    # fallback → original image
    return image_url
