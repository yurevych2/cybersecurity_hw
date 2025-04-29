# Secure image signing and verification (PNG only)

This project implements a system to digitally sign PNG images using RSA 4096-bit encryption, embedding the signature into the PNG metadata while keeping the image viewable and unchanged visually.
If even one pixel is modified, verification will fail.

# Potential applications

While this project is academic in nature, the approach of embedding and verifying digital signatures in image files has real-world relevance in areas such as:
- **Digital forensics** – ensuring that image evidence has not been tampered with.
- **Journalism and media** – certifying that photographs are original and unaltered.
- **Watermarking for copyright** – using hidden metadata signatures to prove ownership.

This technique helps detect unauthorized modifications and supports trust in digital content.


# Project structure
```
project/
│
├── main.py                         # CLI for signing and verifying
├── save_asymmetric_keys.py         # generates RSA keys
├── requirements.txt                # project dependencies
│
├── metadata_version/
│   ├── sign_metadata.py            # signs image and embeds signature into metadata
│   └── verify_metadata.py          # verifies signature from metadata
│
├── private_key.pem                 # generated private key (keep secure)
├── public_key.pem                  # generated public key (shareable)
│
└── example_images/
    ├── horse2.png                  # original image
    ├── horse2_signed.png           # signed image
    └── horse2_signed_edited.png    # edited signed image
```


# Installation

1. Clone or download the repository.
2. Create a virtual environment (recommended but optional):

```sh
python -m venv venv
source venv/bin/activate   # macOS/Linux
venv\Scripts\activate      # windows
```

3. Install dependencies:

```sh
pip install -r requirements.txt
```


# Key Generation

Before signing or verifying, generate RSA keys:

```sh
python save_asymmetric_keys.py
```

This will create ```private_key.pem``` and ```public_key.pem```.


# Usage

1. Sign an Image
```sh
python main.py sign --input original_image.png --output signed_image.png
```

> [!NOTE] 
> If ```--output is not provided```, a default name ```*_signed.png``` is used.

> [!IMPORTANT] 
> The output path must end with .png.

2. Verify an Image

```
python main.py verify --input signed_image.png
```

If the image is authentic and unchanged, you will see ```Signature is valid and matches the image!```. If it is not, you will see ```Signature is invalid```.


# How it works

| Step          | Description |
|---------------|-------------|
| Signing       | SHA-256 hash of the image **pixels** is signed with RSA private key. |
| Embedding     | The signature is saved into PNG **metadata** (tEXt chunk). |
| Verification  | Image metadata is read, metadata is stripped, pixels are hashed again, and the RSA public key verifies the signature. |


# Example workflow

```sh
python save_asymmetric_keys.py
python main.py sign --input example_images/horse1.png
python main.py verify --input example_images/horse1_signed.png
python main.py verify --input example_images/horse1_signed_edited.png
```

You should see a message about successful signing, then ```Signature is valid and matches the image!``` followed by ```Signature is invalid```.


