#include <stdio.h>
#include <stdlib.h>

void print_art() {
     printf("\033[1;36m");
    printf("  _____ ______ __  __  ____   _____ \n");
    printf(" / ____|  ____|  \\/  |/ __ \\ / ____|\n");
    printf("| |  __| |__  | \\  / | |  | | (___  \n");
    printf("| | |_ |  __| | |\\/| | |  | |\\___ \\ \n");
    printf("| |__| | |____| |  | | |__| |____) |\n");
    printf(" \\_____|______|_|  |_|\\____/|_____/ \n");
    printf("\033[0m\n");

    printf("\033[1;33m");
    printf("           /\\_____/\\\n");
    printf("          /  _____  \\\n");
    printf("         |  |     |  |\n");
    printf("\033[0m");
    printf("\033[1;37m");
    printf("           (.o   o.)\n");
    printf("           (   >   )\n");
    printf("          / '-...-' \\\n");
    printf("         /   |   |   \\\n");
    printf("        (    |   |    )\n");
    printf("         \\   '---'   /\n");
    printf("          '-._____.-'\n");
    printf("           |       |\n");
    printf("          /|       |\\\n");
    printf("         (_|       |_)\n");
    printf("\033[0m");

    printf("\033[1;32m");
    printf("   --- GemOS | Fedora Based | v0.1 ---\n");
    printf("\033[0m");

    return 0;
}

void optimize() {
    
}

void toggle_ai() {
    printf("gemai basliyor");
    system("cd /home/deniz && python3 m.py");
}

int main() {
    int secim;
    while (1){    
    print_art();
    printf("'1'e bas ve optimize et\n");
    printf("'2'e bas ve GemAI'i ac\n");
    printf("'0' a bas ve cik\n");
    printf("\nSecim: ");
    scanf("%d", &secim);
switch (secim){
case 1 : optimize(); break;
case 2 : toggle_ai(); break;
case 0 : exit(0); break;
default : printf("yanlis giriş");
}
}
    return 0;
}