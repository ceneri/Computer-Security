
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
                    
                    
                    

//https://stackoverflow.com/questions/5935933/dynamically-create-an-array-of-strings-with-malloc
///****************malloc double digits****************
char** populateTwoCharCombos(void) { 
    
    char **basicCombos;
    int BASIC_COMBO_LEN = 2;
    int numberOfBasicCombos = sizeof(alphabet) * sizeof(alphabet);
    
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
    
    //combos
    int alpha_index[] = {0,0,0,0}; /* Default to 00..0 up to pwlen 0's */
    
    char combo[pwlen+1];
    combo[pwlen] = '\0';
    
    
    /******************************************
    a_index to combo ->
    */
    for (int i = 0; i < pwlen; i++){
        combo[i] = alphabet[alpha_index[i]];
    }
    //printf("Combo: %s\n", combo);
    //**************************************
    
    //printf("Alpha_Index: %d\n", alphabet[i]);
    
    
    for (int char_pos = pwlen-1; char_pos > -1; char_pos--){
        
        for (int i = 0; i < 62; i++){
            
            //get possible combo
            alpha_index[char_pos] = i;
             /******************************************
    a_index to combo ->
    */
    /*for (int i = 0; i < pwlen; i++){
        combo[i] = alphabet[alpha_index[i]];
    }
    printf("Combo: %s\n", combo);*/
    //**************************************
        }
        
    }
    
    
    //https://stackoverflow.com/questions/5935933/dynamically-create-an-array-of-strings-with-malloc
    ///****************malloc double digits****************
    /*int ID_LEN = 2;
    int numberOfBasicCombos = 62*62;
    char **basicCombos;

    basicCombos = malloc(numberOfBasicCombos * sizeof(char*));
    
    for (int i = 0; i < numberOfBasicCombos; i++){
        basicCombos[i] = malloc((ID_LEN+1) * sizeof(char));  
        basicCombos[i][ID_LEN] = '\0';      
    }
    
    int index = 0;
    for (int i = 0; i < 62; i++){
        for (int j = 0; j < 62; j++){
            
            basicCombos[index][0] = alphabet[i];
            basicCombos[index][1] = alphabet[j];
            
            printf("Combo: %s\n", basicCombos[index]);
            
            index++;
        }
    }*/
    
    //*******
    
    char **basicCombos2;
    
    //http://pages.cs.wisc.edu/~remzi/Classes/537/Fall2008/Notes/threads-semaphores.txt
    sem_t s;
    sem_init(&s, 0, 1);
    
    sem_wait(&s);
    basicCombos2 = populateTwoCharCombos();
    sem_post(&s);
    
    /*sem_wait(&s);
    printf("Combo999: %s\n", basicCombos2[3400]);
    sem_post(&s);*/
    
    ///**************rprpprpprprrprpr
    char comboS[4+1];
    comboS[4] = '\0';
    
    int numberOfTwoCharCombos = sizeof(alphabet) * sizeof(alphabet);
    
    sem_wait(&s);
    
    for (int k = 0; k < sizeof(alphabet); k++){
        
        if ( pwlen == 3 ){
            k = sizeof(alphabet);
            *comboS = &comboS + 1;
        } else {
            comboS[0] = alphabet[k];
        }
    
        for (int j = 0; j < sizeof(alphabet); j++){
            
            comboS[1] = alphabet[j];
        
            for (int i = 0; i < numberOfTwoCharCombos; i++){
                comboS[2] = basicCombos2[i][0];
                comboS[3] = basicCombos2[i][1];
                
                bool found = strcmp(cryptPasswd, crypt(comboS, salt)) == 0;
                
                if ( found ){
                    strcpy(passwd, comboS);
                    printf("Password: %s ", passwd);
                    printf("ComboSS: %s \n", comboS);
                    return;
                }
                //printf("ComboSS: %s \n", comboS);
                //printf("Crypt: %s\n", crypt(comboS, salt) );
            }
        }
    }

    sem_post(&s);
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
