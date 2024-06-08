#include <stdio.h>
#include <stdlib.h>

int main() {

    if (system("python -m venv myenv") != 0) {
        fprintf(stderr, "Failed to create virtual environment.\n");
        return 1;
    }

    if (system("call myenv\\Scripts\\activate") != 0) {
        fprintf(stderr, "Failed to activate virtual environment.\n");
        return 1;
    }

    if (system("python.exe -m pip install --upgrade pip") != 0) {
        fprintf(stderr, "Failed to upgrade pip.\n");
        return 1;
    }

    const char* install_cmd = "pip install demucs ffmpeg-python torch==2.3.1+cu118 torchvision torchaudio --extra-index-url https://download.pytorch.org/whl/cu118";
    if (system(install_cmd) != 0) {
        fprintf(stderr, "Failed to install packages.\n");
        return 1;
    }

    printf("Environment setup complete. Press any key to continue...\n");
    getchar();

    return 0;
}

