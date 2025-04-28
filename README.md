# Secure image signing and verification (PNG only)

This project implements a system to digitally sign PNG images using RSA 4096-bit encryption, embedding the signature into the PNG metadata while keeping the image viewable and unchanged visually.
If even one pixel is modified, verification will fail.

# Project structure
```
project/
│
├── main.py                         # CLI for signing and verifying
├── save_asymmetric_keys.py         # generate RSA keys
├── requirements.txt                # project dependencies
│
├── metadata_version/
│   ├── sign_metadata.py            # sign image and embed signature into metadata
│   └── verify_metadata.py          # verify signature from metadata
│
├── private_key.pem                 # generated private key (keep secure)
├── public_key.pem                  # generated public key (shareable)
│
└── example_images/
    ├── horse2.png                  # origina image
    ├── horse2_signed.png           # signed image
    └── horse2_signed_edited.png    # edited signed image
```

# Installation
Clone or download the repository.

(Recommended) Create a virtual environment:

```sh
python -m venv venv
source venv/bin/activate   # macOS/Linux
venv\Scripts\activate      # Windows
```

Install dependencies:

sh
pip install -r requirements.txt


# Key Generation
Before signing or verifying, generate RSA keys:

```sh
python save_asymmetric_keys.py
```

This will create ```private_key.pem``` and ```public_key.pem```.

# Usage

Sign an Image
```sh
python main.py sign --input original_image.png --output signed_image.png
```

If ```--output is not provided```, a default name ```*_signed.png``` is used.

> [!IMPORTANT] 
> The output path must end with .png.

Verify an Image
```
python main.py verify --input signed_image.png
```
If the image is authentic and unchanged, you will see ```Signature is valid and matches the image!``` if it is not, you will see ```Signature is invalid.```

# How it works

| Step          | Description |
|---------------|-------------|
| Signing       | SHA-256 hash of the image **pixels** is signed with RSA private key. |
| Embedding     | The signature is saved into PNG **metadata** (tEXt chunk). |
| Verification  | Image metadata is read, metadata is stripped, pixels are hashed again, and RSA public key verifies the signature. |


# Example workflow
```sh
python save_asymmetric_keys.py
python main.py sign --input example_images/horse1.png
python main.py verify --input example_images/horse1_signed.png
```

You should see a success message if the image is intact!
