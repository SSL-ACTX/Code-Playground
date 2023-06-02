#include <cstdio>
#include <cstdlib>
#include <iostream>
#include <string>

void adbConnect() {
  const std::string ip_prefix = "192.168.0.";
  const int start_address = 100;
  const int end_address = 110;

  for (int i = start_address; i <= end_address; i++) {
    std::string ip_address = ip_prefix + std::to_string(i);
    std::string adb_command = "adb connect " + ip_address;
    system(adb_command.c_str());
  }
}

void adbLogcat() {
  FILE *outfile = fopen("log.txt", "w");
  FILE *fp = popen("adb logcat", "r");
  char buffer[4096];

  while (fgets(buffer, sizeof(buffer), fp)) {
    fprintf(outfile, "%s", buffer);
  }

  pclose(fp);
  fclose(outfile);
}

void adbDumpsys() {
  int choice;

  while (true) {
    system("cls");
    std::cout << "\n\t\t\t==== Dumpsys ====\n";
    std::cout << "\n\t1. Full";
    std::cout << "\n\t2. Battery";
    std::cout << "\n\t3. Option 3";
    std::cout << "\n\t4. Return to Main Menu";
    std::cout << "\n\n\tChoice: ";
    std::cin >> choice;

    switch (choice) {
    case 1:
      std::cout << "\nFull Dumpsys\n";
      system("adb shell dumpsys");
      break;
    case 2:
      std::cout << "\nDumpsys Battery\n";
      system("adb shell dumpsys battery");
      break;
    case 3:
      std::cout << "\nOption 3\n";
      break;
    case 4:
      std::cout << "Returning to Main Menu...\n";
      return;
    default:
      std::cout << "Invalid choice. Please try again.\n";
      break;
    }
  }
}

void adbInstall() {
  std::cout << "\n\t=== ADB Install ===\n";
  const std::string adb_install_cmd = "adb install ";
  std::string app_name;

  std::cout << "\n\tEnter app name: ";
  std::cin >> app_name;

  std::string cmd = adb_install_cmd + "\"" + app_name + ".apk\"";
  system(cmd.c_str());
}

void adbReboot() {
  int choice;

  while (true) {
    system("cls");
    std::cout << "\n\t\t\t==== ADB Reboot ====\n";
    std::cout << "\n\t[1] Reboot";
    std::cout << "\n\t[2] Power Off";
    std::cout << "\n\t[3] Recovery";
    std::cout << "\n\t[4] Bootloader";
    std::cout << "\n\t[5] Return";
    std::cout << "\n\n\tChoice: ";
    std::cin >> choice;

    switch (choice) {
    case 1:
      std::cout << "\nRebooting...\n";
      system("adb reboot");
      break;
    case 2:
      std::cout << "\nShutting down...\n";
      system("adb shell reboot -p");
      break;
    case 3:
      std::cout << "\nRebooting to Recovery...\n";
      system("adb reboot recovery");
      break;
    case 4:
      std::cout << "\nRebooting to Bootloader...\n";
      system("adb reboot bootloader");
      break;
    case 5:
      return;
    default:
      std::cout << "Invalid choice. Please try again.\n";
      break;
    }
  }
}

int main() {
  std::string choice;

  while (true) {
    system("cls");
    std::cout << "\n\t\t\t=== Main Menu ===\n";
    std::cout << "\n\t[1] ADB Connect     [6] ADB Reboot";
    std::cout << "\n\t[2] ADB Logcat      [7] Device Info's";
    std::cout << "\n\t[3] ADB Dumpsys     [8] Device Settings";
    std::cout << "\n\t[4] ADB Install     [9] ADB Push/Pull";
    std::cout << "\n\t[5] ADB Root Mode   [10] File Manager\n";
    std::cout << "\n\t[X] Exit\n";
    std::cout << "\n\tChoice: ";
    std::cin >> choice;

    if (choice == "1") {
      system("cls");
      adbConnect();
    } else if (choice == "2") {
      system("cls");
      adbLogcat();
    } else if (choice == "3") {
      adbDumpsys();
    } else if (choice == "4") {
      adbInstall();
    } else if (choice == "5") {
      system("adb root");
    } else if (choice == "6") {
      system("cls");
      adbReboot();
    } else if (choice == "X" || choice == "x") {
      break;
    } else {
      std::cout << "Invalid choice. Please try again." << std::endl;
    }
  }

  return 0;
}
