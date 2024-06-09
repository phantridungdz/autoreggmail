import uuid
import cloudinary
import cloudinary.uploader

def upload_cloudinary_image(image):
    unique_public_id = "captcha_" + str(uuid.uuid4())
    cloudinary.config(
        cloud_name="",
        api_key="",
        api_secret=""
    )

    return cloudinary.uploader.upload(image, public_id=unique_public_id)