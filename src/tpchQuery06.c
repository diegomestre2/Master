/*
 ============================================================================
 Name        : TPCH_Query6.c
 Author      : Diego Gomes Tomé
 Version     : 1.0
 Copyright   : Your copyright notice
 Description : Process query 6 TPC-H, Ansi-style
 ============================================================================
 */


#include <stdio.h>
#include <stdlib.h>
#include <string.h>

static char *const pathOut = "/Users/diegogomestome/Desktop/resultQ06.txt";
static char *const pathIn = "/Users/diegogomestome/git/tpch/data1/lineitem.tbl";
FILE *outFile;

int main(int argc, char *argv[]) {

    FILE *fileInput;
    int *p_shipdate, *shipdateMatchedList, *discountMatchedList, *p_quantity,*quantityMatchedList;
    double *p_discount;
    char linha[1000];
    char *result = NULL, *token = NULL, *year = NULL;
    int n = 6001218, i = 0, j = 0, k = 0,l = 0,count = 0;

    p_shipdate = malloc(n * sizeof(int));
    p_discount = malloc(n * sizeof(double));
    p_quantity = malloc(n * sizeof(int));
    shipdateMatchedList = malloc(n * sizeof(int));
    discountMatchedList = malloc(n * sizeof(int));
    quantityMatchedList = malloc(n * sizeof(int));

    if ((NULL == (fileInput = fopen(pathIn, "r")) || NULL == (outFile = fopen(pathOut, "w+")))) {
        perror("Erro: fopen");
        exit(EXIT_FAILURE);
    }

    while (!feof(fileInput)) {
        // Lê uma linha (inclusive com o '\n')
        result = fgets(linha, 1000, fileInput); // o 'fgets' lê até 99 caracteres ou até o '\n'
        token = strtok(result, "|");
        for (j = 0; j < 10; j++) {
            token = strtok(NULL, "|");
            if (j == 3 && i != 6001215)
                p_quantity[i] = atoi(token);
            if (j == 5 && i != 6001215)
                p_discount[i] = atof(token);
            if (j == 9 && i != 6001215) {
                year = strtok(token, "-");
                p_shipdate[i] = atoi(year);
            }
        }
        i++;
    }
    printf("carreguei os dados\n");
    fclose(fileInput);

    asm volatile ("nop");
    asm volatile ("nop");
    asm volatile ("nop");
    asm volatile ("nop");
    asm volatile ("nop");
    for (i = 0, j = 0; i < n; i++) {
        if (p_shipdate[i] <= 1994 && p_shipdate[i] > 1993) {

            shipdateMatchedList[j] = i;
            j++;
            count++;
        }
    }
    asm volatile ("nop");
    asm volatile ("nop");
    asm volatile ("nop");
    asm volatile ("nop");
    asm volatile ("nop");
    asm volatile ("nop");
    printf("Matches primeiro laço: %d \n",count);
    count = 0;
    for (i = 0, k = 0; i <= j; i++) {

        if (p_discount[shipdateMatchedList[i]] <= 0.07
            && p_discount[shipdateMatchedList[i]] >= 0.05) {
            count++;
            discountMatchedList[k] = shipdateMatchedList[i];
            k++;
        }
    }
    asm volatile ("nop");
    asm volatile ("nop");
    asm volatile ("nop");
    asm volatile ("nop");
    asm volatile ("nop");
    asm volatile ("nop");
    asm volatile ("nop");
    printf("Matches segundo laço: %d \n",count);
    count = 0;
    for (i = 0,l=0; i <= k; i++) {
        if (p_quantity[discountMatchedList[i]] < 24) {
            quantityMatchedList[l] = discountMatchedList[i];
            l++;
            count++;
        }
    }
    printf("Matches terceiro laço: %d \n",count);
    asm volatile ("nop");
    asm volatile ("nop");
    asm volatile ("nop");
    asm volatile ("nop");
    asm volatile ("nop");
    fclose(outFile);
    printf("Done");

    return EXIT_SUCCESS;
}
