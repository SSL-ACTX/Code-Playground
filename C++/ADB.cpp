#include <iostream>
#include <cstdlib>
#include <string>
#include <cstring>
using namespace std;

void adbcon()
{
    const string ip_prefix = "192.168.0.";
    const int start_address = 100; 
    const int end_address = 110;
    for (int i = start_address; i <= end_address; i++)
    {
        string ip_address = ip_prefix + to_string(i);
        string adb_command = "adb connect " + ip_address;
        system(adb_command.c_str());
    }
}

void adblogc()
{
    FILE* outfile = fopen("log.txt", "w");
    FILE* fp = popen("adb logcat", "r");
    char buffer[4096];
    while (fgets(buffer, sizeof(buffer), fp))
    {
        fprintf(outfile, "%s", buffer);
    }
    pclose(fp);
    fclose(outfile);
}

void smdsys()
{
    int choice;
    while (true)
    {
        system("cls");
        cout << "\n\t\t\t==== Dumpsys ====\n";
        cout << "\n\t1. Full";
        cout << "\n\t2. Battery";
        cout << "\n\t3. Option 3";
        cout << "\n\t4. Return to Main Menu";
        cout << "\n\n\tChoice: ";
        cin >> choice;

        switch (choice)
        {
        case 1:
            cout << "\nFull Dumpsys\n";
            system("adb shell dumpsys");
            break;
        case 2:
            cout << "\nDumpsys Battery\n";
            system("adb shell dumpsys battery");
            break;
        case 3:
            cout << "\nOption 3\n";
            break;
        case 4:
            cout << "Returning to Main Menu...\n";
            return;
        default:
            cout << "Invalid choice. Please try again.\n";
            break;
        }
    }
}

void install()
{
    cout << "\n\t=== ADB Install ===\n";
    const char* adb_install_cmd = "adb install ";
    char app_name[256];

    cout << "\n\tEnter app name: ";
    cin >> app_name;

    size_t cmd_size = strlen(adb_install_cmd) + strlen(app_name) + 12;
    char* cmd = (char*)malloc(cmd_size);
    sprintf(cmd, "%s\"%s.apk\"", adb_install_cmd, app_name);
    system(cmd);
    free(cmd);
}
void reb()
{
    int choice;
    while (true)
    {
        system("cls");
        cout << "\n\t\t\t==== ADB Reboot ====\n";
        cout << "\n\t[1] Reboot";
        cout << "\n\t[2] Power Off";
        cout << "\n\t[3] Recovery";
        cout << "\n\t[4] Bootloader";
        cout << "\n\t[5] Return";
        cout << "\n\n\tChoice: ";
        cin >> choice;

        switch (choice)
        {
        case 1:
            cout << "\nRebooting...\n";
            system("adb reboot");
            break;
        case 2:
            cout << "\nShutting down...\n";
            system("adb shell reboot -p");
            break;
        case 3:
            cout << "\nRebooting to Recovery...\n";
            system("adb reboot recovery");
            break;
        case 4:
            cout << "\nRebooting to Bootloader...\n";
            system("adb reboot bootloader");
            break;
        case 5:
            return;
        default:
            cout << "Invalid choice. Please try again.\n";
            break;
        }
    }
}

int main()
{
    string choice;
    while (true)
    {
        system("cls");
        cout << "\n\t\t\t=== Main Menu ===\n";
        cout << "\n\t[1] ADB Connect     [6] ADB Reboot";
        cout << "\n\t[2] ADB Logcat      [7] Device Info's";
        cout << "\n\t[3] ADB Dumpsys     [8] Device Settings";
        cout << "\n\t[4] ADB Install     [9] ADB Push/Pull";
        cout << "\n\t[5] ADB Root Mode   [10] File Manager\n";
        cout << "\n\t[X] Exit\n";
        cout << "\n\tChoice: ";
        getline(cin, choice);
        if (choice == "1")
        {
            system("cls");
            adbcon();
        }
        else if (choice == "2")
        {
            system("cls");
            adblogc();
        }
        else if (choice == "3")
        {
            smdsys();
        }
        else if (choice == "4")
        {
            install();
        }
        else if (choice == "5")
        {
            system("adb root");
        }
        else if (choice == "6")
        {
            system("cls");
            reb();
        }
        else if (choice == "X" || choice == "x")
        {
            break;
        }
        else
        {
            cout << "Invalid choice. Please try again." << endl;
        }
    }

    return 0;
}
