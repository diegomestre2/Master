/*
 ============================================================================
 Name        : TraceGenerator.c
 Author      : Diego Gomes Tomé
 Version     : 1.0
 Copyright   : Your copyright notice
 Description : Generates the dynamic and memory input files to Sinuca, Ansi-style
 ============================================================================
 */


#include <stdio.h>
#include <stdlib.h>


static char *const pathMem = "/Users/diegogomestome/Desktop/output_trace.out.tid0.mem.out";
static char *const pathDyn = "/Users/diegogomestome/Desktop/output_trace.out.tid0.dyn.out";
static char *const pathResult = "/Users/diegogomestome/Desktop/result.txt";
FILE *outFile;

int main(int argc, char *argv[]) {

    FILE *fileDyn, *fileMem, *fileRes;
    int i, j, k, lineitemSize;
    lineitemSize = 6001214;
    int addressR = 1024 * 1024 * 1024;
    int addressW = 1024 * 1024 * 1024 + 6001214;
    int size = 4;
    char* result = NULL;
    char linha[1000];


    if ((NULL == (fileDyn = fopen(pathDyn, "w+")) || NULL == (fileMem = fopen(pathMem, "w+")) ||
         NULL == (fileRes = fopen(pathResult, "r+")))) {
        perror("Erro: fopen");
        exit(EXIT_FAILURE);
    }
    while (!feof(fileRes)) {
        // Lê uma linha (inclusive com o '\n')
        result = fgets(linha, 1000, fileRes); // o 'fgets' lê até 99 caracteres ou até o '\n'
    }
    for (i = 0; i <= lineitemSize; i++) {

        if (i < 909455) {
            fprintf(fileDyn, "%s", "1\n2\n");
            fprintf(fileMem, "%s %d %s %d %s", "R 4", addressR, "1\nW 4", addressW, "2\n");
            addressR += size;
            addressW += size;
        } else {
            fprintf(fileDyn, "%s", "1\n3\n");
            fprintf(fileMem, "%s %d %s", "R 4", addressR, "1\n");
            addressR += size;
        }
    }

    for (i = 0; i <= 909455; i++) {

        if (i < 248078) {
            fprintf(fileDyn, "%s", "4\n5\n");
            fprintf(fileMem, "%s %d %s %d %s %d %s %d %s %d %s",
                    "R 4", addressR, "4\nR 4", addressR + size, "4\nR 4", addressR + size * 2, "4\nR 4",
                    addressR + size * 3, "5\nW 4", addressW, "5\n");
            addressR += size * 4;
            addressW += size;
        } else {
            fprintf(fileDyn, "%s", "4\n6\n");
            fprintf(fileMem, "%s %d %s %d %s %d %s",
                    "R 4", addressR, "4\nR 4", addressR + size, "4\nR 4", addressR + size * 2, "4\n");
            addressR += size * 3;
        }
    }

    for (i = 0; i <= 248078; i++) {

        if (i < 114161) {
            fprintf(fileDyn, "%s", "8\n9\n");
            fprintf(fileMem, "%s %d %s %d %s %d %s %d %s %d %s", "R 4", addressR, "8\nR 4", addressR + size, "8\nR 4",
                    addressR + size * 2, "8\nR 4", addressR + size * 3, "9\nW 4", addressW, "9\n");
            addressR += size * 4;
            addressW += size;
        } else {
            fprintf(fileDyn, "%s", "8\n7\n");
            fprintf(fileMem, "%s %d %s %d %s %d %s", "R 4", addressR, "8\nR 4", addressR + size, "8\nR 4",
                    addressR + size * 2, "8\n");
            addressR += size * 3;
        }
    }
}