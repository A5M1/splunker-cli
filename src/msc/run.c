#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>

bool is_venv_exists() {
    FILE* file = fopen("myenv", "r");
    if (file) {
        fclose(file);
        return true;
    }
    return false;
}

void create_virtual_env() {
    system("init.exe");
}

void activate_venv_and_run_script() {
    system("myenv\\Scripts\\activate");
    system("python src\\script.py");
}

int main() {
    if (!is_venv_exists()) {
        create_virtual_env();
    }
    activate_venv_and_run_script();

    return 0;
}
