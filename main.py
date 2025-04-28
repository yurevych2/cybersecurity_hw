import argparse
import os
import sys
from PIL import Image

from metadata_version.sign_metadata import sign_metadata
from metadata_version.verify_metadata import verify_metadata

def check_image_type(image_path):
    try:
        img = Image.open(image_path)
        format = img.format
        if format != "PNG":
            raise ValueError(f"Unsupported image format: {format}. Only PNG is allowed.")
        return format
    except Exception as e:
        raise ValueError(f"Cannot open image: {e}")

def main():
    parser = argparse.ArgumentParser(description="Image RSA Signer and Verifier (PNG Only)")
    parser.add_argument("action", choices=["sign", "verify"], help="Action to perform: sign or verify")
    parser.add_argument("--input", required=True, help="Path to input PNG image")
    parser.add_argument("--output", required=False, help="Path to output PNG image (only for signing)")

    args = parser.parse_args()

    if not os.path.exists(args.input):
        print(f"Error: Input file '{args.input}' does not exist.")
        sys.exit(1)

    try:
        check_image_type(args.input)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

    if args.action == "sign":
        if not args.output:
            base, ext = os.path.splitext(args.input)
            args.output = base + "_signed.png"
        else:
            if not args.output.lower().endswith(".png"):
                print("Error: Output file must have a .png extension.")
                sys.exit(1)

        sign_metadata(args.input, args.output)

    elif args.action == "verify":
        verify_metadata(args.input)

if __name__ == "__main__":
    main()
