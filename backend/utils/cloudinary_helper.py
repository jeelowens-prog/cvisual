import cloudinary
import cloudinary.uploader
import os
from dotenv import load_dotenv

load_dotenv()

# Configure Cloudinary
cloudinary.config(
    cloud_name=os.getenv('CLOUDINARY_CLOUD_NAME'),
    api_key=os.getenv('CLOUDINARY_API_KEY'),
    api_secret=os.getenv('CLOUDINARY_API_SECRET')
)

def upload_image(file, folder='cvisual'):
    """
    Upload image to Cloudinary
    
    Args:
        file: File object from request.files
        folder: Cloudinary folder name
    
    Returns:
        dict: Upload result with secure_url and public_id
    """
    try:
        result = cloudinary.uploader.upload(
            file,
            folder=folder,
            resource_type='auto',
            transformation=[
                {'quality': 'auto:best'},
                {'fetch_format': 'auto'}
            ]
        )
        return result
    except Exception as e:
        raise Exception(f"Cloudinary upload failed: {str(e)}")

def delete_image(public_id):
    """
    Delete image from Cloudinary
    
    Args:
        public_id: Cloudinary public_id of the image
    
    Returns:
        dict: Deletion result
    """
    try:
        result = cloudinary.uploader.destroy(public_id)
        return result
    except Exception as e:
        raise Exception(f"Cloudinary deletion failed: {str(e)}")

def upload_multiple_images(files, folder='cvisual'):
    """
    Upload multiple images to Cloudinary
    
    Args:
        files: List of file objects
        folder: Cloudinary folder name
    
    Returns:
        list: List of upload results
    """
    results = []
    for file in files:
        try:
            result = upload_image(file, folder)
            results.append(result)
        except Exception as e:
            results.append({'error': str(e)})
    return results
