#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#include "p_utils.h"


/**
 * Returns the number of lines in the file at path
 * FNAME if it exists and can be read, -1 otherwise.
 * 
 * https://stackoverflow.com/questions/12733105
 */
int countLinesInFile(char *fname) {
    FILE *fp = fopen(fname, "r");
    int lines = -1;
    if (fp) {
        lines = 0;
        while (!feof(fp)) {
            if (fgetc(fp) == '\n') {
                lines++;
            }   
        }
        fclose(fp);
    }
    return lines;
} 

/**
 * Returns T_SALT substring made of the first two characters in CRYPTPASSWD
 */
char* getSalt(char *cryptPasswd){
    char *t_salt = malloc(sizeof(char)*3);
    strncpy(t_salt, cryptPasswd, 2);
    t_salt[2] = '\0';
    
    return t_salt;
}

/**
 * Returns SALTS array of salt strings, taken from encrypted passwords found in CRYPTPASSWDS, given
 * NUMUSERS
 */
char** getSalts(char **cryptPasswds, int numUsers) {  
    char **salts = malloc(numUsers * sizeof (char*));
    for (int i = 0; i < numUsers; i++){
        salts[i] = getSalt(cryptPasswds[i]);
    }
    
    return salts;
}

/**
 * Returns an array of all encrypted passwords found in the file located in
 * FNAME path file
 * 
 * https://stackoverflow.com/questions/5935933/dynamically-create-an-array-of-strings-with-malloc
 */
char** getCryptPasswds(char *fname, int numUsers) { 
   
    char **cPasswords = malloc(numUsers * sizeof (char*));
    for (int i = 0; i < numUsers; i++){
        cPasswords[i] = malloc( 14 * sizeof (char));
        cPasswords[i][13] = '\0';
    }

    char line[64];
    FILE *fin = fopen(fname, "r");
    for (int i = 0; fgets(line, 64, fin) != NULL; i++) {
        strtok(line, ":");
        sprintf(cPasswords[i], "%s", strtok(strtok(NULL, ":"), "\n"));
        //printf("Password: %s \n", cPasswords[i]);
        if ((int) strlen(cPasswords[i]) != 13) {
            printf("Password: %s \n", cPasswords[i]);
            printf("No: %d \n", (int) strlen(cPasswords[i]));
            printf("ERROR\n");
            exit(-1);
        }
    }
    fclose(fin);
    
    return cPasswords;
}