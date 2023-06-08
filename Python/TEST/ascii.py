# Image to ASCII Converter
from PIL import Image

ASCII_CHARS = '@%#*+=-:. '

def scale_image(image, new_width=120): # Adjustable :)
    (original_width, original_height) = image.size
    aspect_ratio = original_height/float(original_width)
    new_height = int(aspect_ratio * new_width/2)
    new_image = image.resize((new_width, new_height))
    return new_image

def convert_grayscale(image):
    return image.convert('L')

def map_pixels_to_ascii(image, range_width=25):
    pixels = image.getdata()
    ascii_str = ''
    for pixel_value in pixels:
        ascii_str += ASCII_CHARS[pixel_value//(range_width+1)]
    return ascii_str

def convert_image_to_ascii(image):
    image = scale_image(image)
    image = convert_grayscale(image)
    ascii_str = map_pixels_to_ascii(image)
    img_width = image.width
    ascii_str_len = len(ascii_str)
    ascii_img = ''
    for i in range(0, ascii_str_len, img_width):
        ascii_img += ascii_str[i:i+img_width] + '\n'
    return ascii_img

def save_ascii_art_to_file(ascii_art, file_path):
    with open(file_path, 'w') as f:
        f.write(ascii_art)

def main():
    image_path = 'image.jpg'
    image = Image.open(image_path)

    ascii_art = convert_image_to_ascii(image)

    output_file = 'ascii_art.txt'
    save_ascii_art_to_file(ascii_art, output_file)
    print(f"ASCII art saved to {output_file}")

if __name__ == '__main__':
    main()
