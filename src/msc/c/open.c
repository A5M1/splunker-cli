#include <windows.h>
#include <stdio.h>

int main(int argc) {
  // Open the current directory in Windows Explorer
  ShellExecute(0, NULL, "explorer.exe", ".", NULL, SW_SHOWNORMAL);

  return 0;
}
