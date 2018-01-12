
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <crypt.h>

/*
 * Find the plain-text password PASSWD of length PWLEN for the user USERNAME 
 * given the encrypted password CRYPTPASSWD.
 */
void crackSingle(char *username, char *cryptPasswd, int pwlen, char *passwd) {
    printf("Squidward: %s\n", cryptPasswd);
    
    //Get salt
    char salt[3];
    strncpy(salt, cryptPasswd, 2);
    salt[2] = '\0';
    
    printf("Salty Salt: %s\n", salt );
    printf("Squidward: %s\n", cryptPasswd);
    
    int alphabet[62];
    //Create Array of chars
    for (int i = 48; i < 123; i++){
        if ( i == 58 )  i = 65;
        if ( i == 91 )  i = 97;
        
        alphabet[i] = i;
        printf("Salty Salt: %c\n", alphabet[i]);
    }
    
    //combos
    char combo[pwlen+1];
    combo[pwlen] = '\0';
    
    for (int char_pos = 0; char_pos < pwlen; char_pos++){
        
    }
    
    
    
}

/*
 * Find the plain-text passwords PASSWDS of length PWLEN for the users found
 * in the old-style /etc/passwd format file at pathe FNAME.
 */
void crackMultiple(char *fname, int pwlen, char **passwds) { } 

/*
 * Find the plain-text passwords PASSWDS of length PWLEN for the users found
 * in the old-style /etc/passwd format file at pathe FNAME.
 */
void crackSpeedy(char *fname, int pwlen, char **passwds) { }

/*
 * Find the plain-text password PASSWD of length PWLEN for the user USERNAME 
 * given the encrypted password CRYPTPASSWD withoiut using more than MAXCPU
 * percent of any processor.
 */
void crackStealthy(char *username, char *cryptPasswd, int pwlen, char *passwd, int maxCpu) { }
