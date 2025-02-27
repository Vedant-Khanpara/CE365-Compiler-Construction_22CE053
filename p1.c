#include <stdio.h>
#include <conio.h>

int main() {

    char input[100];
    int i = 0;

    printf("Enter a string: ");
    fgets(input, sizeof(input), stdin);

    // Remove the newline character if it's at the end of the input
    size_t length = strlen(input);
    if (length > 0 && input[length - 1] == '\n') {
        input[length - 1] = '\0';
    }

    while (input[i] == 'a') {
        i++;
    }

    if (input[i] == 'b' && input[i + 1] == 'b' && input[i + 2] == '\0') {
        printf("Valid String\n");
    } else {
        printf("Invalid String\n");
    }

    return 0;
}