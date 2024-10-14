from PIL import Image

def drawImageIntoSpriteSheet(cellx, celly, sheetWidth, sheetHeight, sheetXCount, sheetYCount,
                             image, sheetImage, rotation=0, clearCell=False):
    """
    Draws an image into a specified cell of a sprite sheet, with options to rotate the image
    and clear the cell area before drawing.

    Parameters:
    - cellx (int): The x-coordinate (column index) of the cell in the sprite sheet grid.
    - celly (int): The y-coordinate (row index) of the cell in the sprite sheet grid.
    - sheetWidth (int): The total width of the sprite sheet in pixels.
    - sheetHeight (int): The total height of the sprite sheet in pixels.
    - sheetXCount (int): The number of cells horizontally in the sprite sheet.
    - sheetYCount (int): The number of cells vertically in the sprite sheet.
    - image (PIL.Image.Image): The image to draw into the sprite sheet.
    - sheetImage (PIL.Image.Image): The sprite sheet image to update.
    - rotation (float, optional): The angle to rotate the image counter-clockwise, in degrees.
    - clearCell (bool, optional): Whether to clear the cell area before drawing the image.

    Returns:
    - PIL.Image.Image: The updated sprite sheet image.
    """

    # Calculate cell dimensions
    cellWidth = sheetWidth / sheetXCount
    cellHeight = sheetHeight / sheetYCount

    # Calculate the pixel position of the cell within the sprite sheet
    cellLeft = cellx * cellWidth
    cellTop = celly * cellHeight

    # Clear the cell area if requested
    if clearCell:
        left = int(cellLeft)
        top = int(cellTop)
        right = int(cellLeft + cellWidth)
        bottom = int(cellTop + cellHeight)

        # Create a rectangle to clear the cell area
        if sheetImage.mode == 'RGBA':
            # Fill with transparent pixels
            clear_rect = Image.new('RGBA', (int(cellWidth), int(cellHeight)), (0, 0, 0, 0))
        else:
            # Fill with a solid color (e.g., white or black)
            clear_rect = Image.new(sheetImage.mode, (int(cellWidth), int(cellHeight)), 0)

        # Paste the clear rectangle onto the sprite sheet
        sheetImage.paste(clear_rect, (left, top))

    # Rotate the image if a rotation angle is specified
    if rotation != 0:
        # Rotate the image counter-clockwise, expanding the output image to fit the entire rotated image
        image = image.rotate(rotation, expand=True)

    # Get dimensions of the (possibly rotated) image
    imageWidth, imageHeight = image.size

    # Calculate scale to maintain aspect ratio
    scaleX = cellWidth / imageWidth
    scaleY = cellHeight / imageHeight
    scale = min(scaleX, scaleY)

    # Compute new image size
    newWidth = int(imageWidth * scale)
    newHeight = int(imageHeight * scale)

    # Resize the image while maintaining aspect ratio
    resizedImage = image.resize((newWidth, newHeight), Image.LANCZOS)

    # Center the image within the cell
    offsetX = int(cellLeft + (cellWidth - newWidth) / 2)
    offsetY = int(cellTop + (cellHeight - newHeight) / 2)

    # Paste the resized image onto the sprite sheet
    # Handle transparency if the image has an alpha channel
    if resizedImage.mode in ('RGBA', 'LA') or (resizedImage.mode == 'P' and 'transparency' in resizedImage.info):
        sheetImage.paste(resizedImage, (offsetX, offsetY), resizedImage)
    else:
        sheetImage.paste(resizedImage, (offsetX, offsetY))

    return sheetImage

# Load the images
updated_sheet = Image.open('gameSheet2.png').convert('RGBA')
input_image = Image.open('..\\ships_out\\output\\shipsaamXLAnimeMix_v10.safetensors_99.png').convert('RGBA')

# Define sprite sheet parameters
cell_x = 0
cell_y = 0
sheet_width = updated_sheet.width
sheet_height = updated_sheet.height
sheet_x_count = 10
sheet_y_count = 10
rotation_angle = 90   # Rotate the image by 45 degrees counter-clockwise
clear_cell_before = True  # Clear the cell before drawing

# Update the sprite sheet
for cell_x in range(0 , 3):
    updated_sheet = drawImageIntoSpriteSheet(
        cell_x, cell_y, sheet_width, sheet_height,
        sheet_x_count, sheet_y_count, input_image, updated_sheet,
        rotation=rotation_angle, clearCell=clear_cell_before
    )

# Save or display the updated sprite sheet
updated_sheet.save('updated_sprite_sheet.png')