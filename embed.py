import os
import sys
from mutagen.flac import FLAC, Picture
from PIL import Image
from io import BytesIO


def is_valid_flac(file_path):
    audio = FLAC(file_path)
    if not audio.pictures:
        return False

    for picture in audio.pictures:
        if picture.mime != "image/jpeg" or picture.type != 3:  # Front cover
            return False

        image = Image.open(BytesIO(picture.data))
        if image.format != "JPEG" or image.info.get("progressive", False):
            return False
    return True


def embed_artwork(flac_files, image_data):
    """Embed artwork in FLAC files."""
    for flac_file in flac_files:
        audio = FLAC(flac_file)
        image = Picture()
        image.type = 3
        image.mime = "image/jpeg"
        image.desc = "Cover"
        image.data = image_data

        audio.clear_pictures()
        audio.add_picture(image)
        audio.save()


def process_directory(directory, depth):
    if depth == 0:
        return

    flac_files = []
    image_file = None

    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.lower().endswith(".flac") and not file.startswith("._"):
                flac_path = os.path.join(root, file)
                flac_files.append(flac_path)
        for img_file in files:
            if img_file.lower().endswith(
                (".jpg", ".jpeg", ".png")
            ) and not img_file.startswith("._"):
                image_path = os.path.join(root, img_file)
                img = Image.open(image_path)
                if img.mode == "RGBA":
                    img = img.convert("RGB")
                img = img.resize((300, 300), Image.LANCZOS)
                buffer = BytesIO()
                img.save(
                    buffer,
                    format="JPEG",
                    quality=85,
                    optimize=True,
                    progressive=False,
                )
                image_file = buffer.getvalue()
                break
        if image_file:
            print(f"Embedding artwork in FLAC files in {root}")
            embed_artwork(flac_files, image_file)
            break

        for dir in dirs:
            process_directory(os.path.join(root, dir), depth - 1)
        break


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python script.py <directory> [depth]")
        sys.exit(1)

    directory = sys.argv[1]
    depth = int(sys.argv[2]) if len(sys.argv) > 2 else 1

    process_directory(directory, depth)
    print("Processing complete.")
