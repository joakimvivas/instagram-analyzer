import instaloader
import os
from PIL import Image

storage_path = "app/storage"
os.makedirs(storage_path, exist_ok=True)

def get_profile(instagram_account: str):
    L = instaloader.Instaloader()
    profile = instaloader.Profile.from_username(L.context, instagram_account)
    return profile

def download_photo(instagram_account: str, post):
    unique_id = f"{instagram_account}_{post.mediaid}"
    image_path = os.path.join(storage_path, unique_id)
    instaloader.Instaloader().download_pic(image_path, post.url, post.date)
    return image_path
