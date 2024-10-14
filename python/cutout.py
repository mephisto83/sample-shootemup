import os
from PIL import Image, ImageOps

def apply_mask_to_images_in_folder(image_folder: str, output_folder: str, threshold: int = 128):
    """
    Apply a mask to all images in a folder if the corresponding mask image exists,
    crop the result to the content based on a threshold, center the content, and save the result to an output folder.
    
    :param image_folder: Path to the folder containing the images and masks.
    :param output_folder: Path to the folder where the result images should be saved.
    :param threshold: The alpha threshold for determining transparency when cropping.
    """
    # Ensure the output folder exists
    os.makedirs(output_folder, exist_ok=True)

    # Iterate over all files in the image folder
    for file_name in os.listdir(image_folder):
        if not file_name.endswith(".png") or "_mask.png" in file_name:
            # Skip non-PNG files or mask files themselves
            continue

        # Construct the corresponding mask file name
        mask_file_name = file_name.replace(".png", "_mask.png")
        
        # Full paths to the image and mask
        image_path = os.path.join(image_folder, file_name)
        mask_path = os.path.join(image_folder, mask_file_name)
        
        # Check if the corresponding mask exists
        if os.path.exists(mask_path):
            try:
                # Open the image and mask
                image = Image.open(image_path)
                mask = Image.open(mask_path)
                
                # Apply the mask, crop and center, and save the result
                output_path = os.path.join(output_folder, file_name)
                apply_mask_crop_and_save(image_path, mask, output_path, threshold)
                
                print(f"Processed {file_name} with mask {mask_file_name}")
            except Exception as e:
                print(f"Failed to process {file_name}: {e}")
        else:
            print(f"Skipping {file_name} as no corresponding mask was found.")

def apply_mask_crop_and_save(image_path: str, mask_image: Image.Image, output_path: str, threshold: int):
    """
    Apply a mask to an image, crop to content based on a threshold, center it, and save the result as a PNG.
    
    :param image_path: Path to the original image.
    :param mask_image: A PIL Image object used as a mask.
    :param output_path: Path where the result image should be saved.
    :param threshold: The alpha threshold for determining transparency when cropping.
    """
    # Open the input image
    image = Image.open(image_path).convert("RGBA")
    
    # Ensure the mask is in the right mode
    mask_image = mask_image.convert("L")  # Convert mask to grayscale (if not already)

    # Apply the mask to the image
    image.putalpha(mask_image)

    # Threshold the alpha channel
    alpha = image.split()[-1]  # Get the alpha channel
    # Apply threshold to make semi-transparent areas either fully transparent or fully opaque
    thresholded_alpha = alpha.point(lambda p: 255 if p >= threshold else 0)
    image.putalpha(thresholded_alpha)

    # Crop the image to content (non-transparent areas based on the threshold)
    bbox = image.getbbox()  # Get the bounding box of non-transparent pixels
    if bbox:
        cropped_image = image.crop(bbox)
    else:
        cropped_image = image  # If there's no content, just keep the image as is

    # Create a blank canvas of the same size as the original image and center the cropped content
    centered_image = Image.new("RGBA", image.size, (0, 0, 0, 0))  # Blank transparent canvas
    offset = (
        (image.size[0] - cropped_image.size[0]) // 2,  # Center horizontally
        (image.size[1] - cropped_image.size[1]) // 2   # Center vertically
    )
    centered_image.paste(cropped_image, offset)

    # Save the centered, cropped image as PNG
    centered_image.save(output_path, format="PNG")

# Example usage:
# Example usage:
image_folder = "D:\\dev\\ComfyUI\\custom_nodes\\sample-shootemup\\ships_out"
output_folder = os.path.join(image_folder, "output")
threshold = 253  # Adjust the threshold as needed
apply_mask_to_images_in_folder(image_folder, output_folder, threshold)
