import hashlib
import piexif
import os
from PIL import Image, PngImagePlugin
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import padding

def load_public_key(path="public_key.pem"):
    with open(path, "rb") as key_file:
        public_key = serialization.load_pem_public_key(
            key_file.read()
        )
    return public_key

def extract_signature_from_jpeg(image_path):
    exif_dict = piexif.load(image_path)
    description = exif_dict["0th"].get(piexif.ImageIFD.ImageDescription, None)
    if description is None:
        return None
    return bytes.fromhex(description.decode('utf-8'))

def extract_signature_from_png(image_path):
    img = Image.open(image_path)
    try:
        signature_hex = img.info.get("Signature", None)
        if signature_hex:
            return bytes.fromhex(signature_hex)
    except Exception:
        return None
    return None

def strip_metadata_jpeg(image_path):
    img = Image.open(image_path)
    exif_dict = piexif.load(img.info.get('exif', b''))
    exif_dict["0th"][piexif.ImageIFD.ImageDescription] = b''
    exif_bytes = piexif.dump(exif_dict)
    
    temp_path = "temp_stripped.jpg"
    img.save(temp_path, exif=exif_bytes)
    
    return temp_path

def strip_metadata_png(image_path):
    img = Image.open(image_path)
    meta = PngImagePlugin.PngInfo()

    for k, v in img.info.items():
        if k != "Signature":
            meta.add_text(k, v)

    temp_path = "temp_stripped.png"
    img.save(temp_path, "png", pnginfo=meta)
    
    return temp_path

def verify_signature(public_key, signature, data):
    try:
        public_key.verify(
            signature,
            data,
            padding.PSS(
                mgf=padding.MGF1(hashes.SHA256()),
                salt_length=padding.PSS.MAX_LENGTH
            ),
            hashes.SHA256()
        )
        return True
    except Exception as e:
        print(f"Verification failed: {e}")
        return False

def verify_metadata(image_path):
    public_key = load_public_key()

    if image_path.lower().endswith(".png"):
        signature = extract_signature_from_png(image_path)
        if not signature:
            print("No signature found!")
            return
        temp_clean_path = strip_metadata_png(image_path)

    elif image_path.lower().endswith(".jpg") or image_path.lower().endswith(".jpeg"):
        signature = extract_signature_from_jpeg(image_path)
        if not signature:
            print("No signature found!")
            return
        temp_clean_path = strip_metadata_jpeg(image_path)

    else:
        raise ValueError("Unsupported file format for metadata verification (only JPEG/PNG allowed)")

    img = Image.open(temp_clean_path).convert('RGB')
    pixels = img.tobytes()
    digest = hashlib.sha256(pixels).digest()

    os.remove(temp_clean_path)

    if verify_signature(public_key, signature, digest):
        print("Signature is valid and matches the image!")
    else:
        print("Signature is invalid.")
