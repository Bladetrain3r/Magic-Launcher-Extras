#!/usr/bin/env python3
# MLUpsize.py - A script to upscale images for printing with optional embossing effect.
import argparse
from PIL import Image, ImageFilter
import os

def upscale_and_filter_image(input_path, output_path=None, scale_factor=4, emboss=False):
    img = Image.open(input_path)
    new_size = (img.width * scale_factor, img.height * scale_factor)
    img_upscaled = img.resize(new_size, Image.Resampling.LANCZOS)

    if emboss:
        img_upscaled = img_upscaled.filter(ImageFilter.EMBOSS)

    if not output_path:
        base, ext = os.path.splitext(input_path)
        suffix = "_embossed_upscaled" if emboss else "_upscaled"
        output_path = f"{base}{suffix}{ext}"

    img_upscaled.save(output_path)
    print(f"Saved: {output_path}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Upscale an image for printing, optionally emboss.")
    parser.add_argument("input", help="Path to input image")
    parser.add_argument("-o", "--output", help="Optional path to save result")
    parser.add_argument("-s", "--scale", type=int, default=4, help="Scale factor (default: 4)")
    parser.add_argument("-e", "--emboss", action="store_true", help="Apply emboss filter")
    
    args = parser.parse_args()
    upscale_and_filter_image(args.input, args.output, args.scale, args.emboss)
