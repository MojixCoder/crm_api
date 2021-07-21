
def image_upload_to(instance, filename) -> str:
    return f"user/{instance.username}/{filename}"
