
#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>
#include <string.h>
#include <crypt.h>
#include <semaphore.h>

char alphabet[] = {48,49,50,51,52,53,54,55,56,57,
                    65,66,67,68,69,70,71,72,73,74,75,76,77,78,79,80,81,82,83,84,85,86,87,88,89,90,
                    97,98,99,100,101,102,103,104,105,106,107,108,109,110,111,112,113,114,115,116,
                    117,118,119,120,121,122};
                    
  
  
  
 //https://stackoverflow.com/questions/23436669/how-to-free-an-array-of-char-pointer
 void freeArrayElementsOnly(char** array, int count)
{
    int i;

    for ( i = 0; array[i]; i++ )
        free( array[i] );

    //free( array );
}

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

 
                    

//https://stackoverflow.com/questions/5935933/dynamically-create-an-array-of-strings-with-malloc
///****************malloc double digits****************
char** populateTwoCharCombos(int numberOfBasicCombos) { 
    
    char **basicCombos;
    int BASIC_COMBO_LEN = 2;
    
    basicCombos = malloc(numberOfBasicCombos * sizeof(char*));
    
    for (int i = 0; i < numberOfBasicCombos; i++){
        basicCombos[i] = malloc((BASIC_COMBO_LEN+1) * sizeof(char));  
        basicCombos[i][BASIC_COMBO_LEN] = '\0';      
    }
    
    int index = 0;
    for (int i = 0; i < 62; i++){
        for (int j = 0; j < 62; j++){
            
            basicCombos[index][0] = alphabet[i];
            basicCombos[index][1] = alphabet[j];
            
            //printf("Combo2: %s\n", basicCombos[index]);
            
            index++;
        }
    }
    
    return basicCombos;
}  


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

char** getSalts(char **cryptPasswds, int numUsers) { 

     
    char **salts = malloc(numUsers * sizeof (char*));
    for (int i = 0; i < numUsers; i++){
        salts[i] = malloc( 3 * sizeof (char));
        salts[i][2] = '\0';
    }

    for (int i = 0; i < numUsers; i++){
        strncpy(salts[i], cryptPasswds[i], 2);
        salts[i][2] = '\0';
    }
    
    return salts;
}                  
                    

/*
 * Find the plain-text password PASSWD of length PWLEN for the user USERNAME 
 * given the encrypted password CRYPTPASSWD.
 */
void crackSingle(char *username, char *cryptPasswd, int pwlen, char *passwd) {
    
    //Initialize binary semaphore
    //http://pages.cs.wisc.edu/~remzi/Classes/537/Fall2008/Notes/threads-semaphores.txt
    sem_t lock;
    sem_init(&lock, 0, 1);
    
    //Obtain salt from password/user name salt
    char salt[3];
    strncpy(salt, cryptPasswd, 2);
    salt[2] = '\0';
    
    //Account for null at end of string
    char potentialPasswd[5];
    potentialPasswd[4] = '\0';
    
    //Populate Combos
    sem_wait(&lock);
    char **basicCombos;
    int numberOfTwoCharCombos = sizeof(alphabet) * sizeof(alphabet);
    basicCombos = populateTwoCharCombos(numberOfTwoCharCombos);
    sem_post(&lock);
    
    //Indexes depending on password size
    int threeCharIndices[] = {0,1,2,3};
    int fourCharIndices[] = {1,2,3,4};
    
    bool onlyThreeChars = (pwlen == 3);
        
    //Brute Force 
    sem_wait(&lock);
    
    for (int k = 0; k < sizeof(alphabet); k++){
        
        //First character
        potentialPasswd[0] = alphabet[k];
        //Default
        int *charIndices = fourCharIndices;
        
        
        if ( onlyThreeChars ){
            k = sizeof(alphabet);       //Main loop will only run once
            (*potentialPasswd)++;       //Remove first character from string
            
            charIndices = threeCharIndices;     //New indexes
        } 
    
        for (int j = 0; j < sizeof(alphabet); j++){
            
            //Second character
            potentialPasswd[charIndices[0]] = alphabet[j];
        
            for (int i = 0; i < numberOfTwoCharCombos; i++){
                //Third and Fourth characters
                potentialPasswd[charIndices[1]] = basicCombos[i][0];
                potentialPasswd[charIndices[2]] = basicCombos[i][1];
                
                potentialPasswd[charIndices[3]] = '\0';
                
                //Check if password matches
                bool found = strcmp(cryptPasswd, crypt(potentialPasswd, salt)) == 0;
                if ( found ){
                    strcpy(passwd, potentialPasswd);
                    //printf("Password: %s ", passwd);
                    //printf("ComboSS: %s \n", potentialPasswd);
                    return;
                }
            }
        }
    }

    sem_post(&lock);
}

/*
 * Find the plain-text passwords PASSWDS of length PWLEN for the users found
 * in the old-style /etc/passwd format file at pathe FNAME.
 */
void crackMultiple(char *fname, int pwlen, char **passwds) { 

    //Initialize binary semaphore
    //http://pages.cs.wisc.edu/~remzi/Classes/537/Fall2008/Notes/threads-semaphores.txt
    sem_t lock;
    sem_init(&lock, 0, 1);
    
    //numusers
    int numUsers = countLinesInFile(fname);
    
    //Get encrypted passwords
    char **cryptPasswds;
    cryptPasswds = getCryptPasswds(fname, numUsers);
    
    for (int i = 0; i < numUsers; i++){
        printf("Encrypted Password: %s \n", cryptPasswds[i]);
    }
    
    //Get salts
    char **c_salts;
    c_salts = getSalts(cryptPasswds, numUsers);
    
    for (int i = 0; i < numUsers; i++){
        printf("Salts: %s \n", c_salts[i]);
    }
    
    //Empty array of cracked passwords(Later could optimize to stop checking for found ones)
    char **crackedPasswds = malloc(numUsers * sizeof (char*));
    for (int i = 0; i < numUsers; i++){
        crackedPasswds[i] = malloc( 5 * sizeof (char));
        crackedPasswds[i][4] = '\0';
    }
    
    //Account for null at end of string
    char potentialPasswd[5];
    potentialPasswd[4] = '\0';
    
    //Populate Combos
    sem_wait(&lock);
    char **basicCombos;
    int numberOfTwoCharCombos = sizeof(alphabet) * sizeof(alphabet);
    basicCombos = populateTwoCharCombos(numberOfTwoCharCombos);
    sem_post(&lock);
    
    //Indexes depending on password size
    int threeCharIndices[] = {0,1,2,3};
    int fourCharIndices[] = {1,2,3,4};
    
    bool onlyThreeChars = (pwlen == 3);
        
    //Brute Force 
    sem_wait(&lock);
    
    for (int k = 0; k < sizeof(alphabet); k++){
        
        //First character
        potentialPasswd[0] = alphabet[k];
        //Default
        int *charIndices = fourCharIndices;
        
        
        if ( onlyThreeChars ){
            k = sizeof(alphabet);       //Main loop will only run once
            (*potentialPasswd)++;       //Remove first character from string
            
            charIndices = threeCharIndices;     //New indexes
            
            freeArrayElementsOnly(crackedPasswds, numUsers);
            for (int i = 0; i < numUsers; i++){
                crackedPasswds[i] = malloc( 4 * sizeof (char));
                crackedPasswds[i][3] = '\0';
            }
            
        } 
    
        for (int j = 0; j < sizeof(alphabet); j++){
            
            //Second character
            potentialPasswd[charIndices[0]] = alphabet[j];
        
            for (int i = 0; i < numberOfTwoCharCombos; i++){
                //Third and Fourth characters
                potentialPasswd[charIndices[1]] = basicCombos[i][0];
                potentialPasswd[charIndices[2]] = basicCombos[i][1];
                
                potentialPasswd[charIndices[3]] = '\0';
                //printf("ComboSS: %s \n", potentialPasswd);
                
                //Check if password matches
                bool found;
                for (int i = 0; i < numUsers; i++){
                    found = strcmp(cryptPasswds[i], crypt(potentialPasswd, c_salts[i])) == 0;
                    
                    if ( found ){
                        strcpy(passwds[i], potentialPasswd);
                        //printf("Password: %s ", passwd);
                        printf("Password: %s \n", passwds[i]);
                        //return;
                    }
                }
                
                
            }
        }
    }
    
    //(*passwds) = (*crackedPasswds);

    sem_post(&lock);

} 

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
