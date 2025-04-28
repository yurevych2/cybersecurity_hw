import hashlib
import piexif
from PIL import Image, PngImagePlugin
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import padding

def load_private_key(path="private_key.pem"):
    with open(path, "rb") as key_file:
        private_key = serialization.load_pem_private_key(
            key_file.read(),
            password=None,
        )
    return private_key

def sign_data(private_key, data):
    signature = private_key.sign(
        data,
        padding.PSS(
            mgf=padding.MGF1(hashes.SHA256()),
            salt_length=padding.PSS.MAX_LENGTH
        ),
        hashes.SHA256()
    )
    return signature

def embed_signature_to_jpeg(image_path, output_path, signature):
    img = Image.open(image_path)
    exif_dict = {"0th": {}, "Exif": {}, "GPS": {}, "1st": {}, "thumbnail": None}
    exif_dict["0th"][piexif.ImageIFD.ImageDescription] = signature.hex()
    exif_bytes = piexif.dump(exif_dict)
    img.save(output_path, "jpeg", exif=exif_bytes)

def embed_signature_to_png(image_path, output_path, signature):
    img = Image.open(image_path)
    meta = PngImagePlugin.PngInfo()
    meta.add_text("Signature", signature.hex())
    img.save(output_path, "png", pnginfo=meta)

def sign_metadata(image_path, output_path):
    private_key = load_private_key()

    img = Image.open(image_path).convert('RGB') # to load pixels, not file bytes
    pixels = img.tobytes()
    digest = hashlib.sha256(pixels).digest()

    signature = sign_data(private_key, digest)

    if image_path.lower().endswith(".png"):
        embed_signature_to_png(image_path, output_path, signature)
    elif image_path.lower().endswith(".jpg") or image_path.lower().endswith(".jpeg"):
        embed_signature_to_jpeg(image_path, output_path, signature)
    else:
        raise ValueError("Unsupported file format for metadata signing (only JPEG/PNG allowed)")
    
    print(f"Metadata-signed image saved to {output_path}")
