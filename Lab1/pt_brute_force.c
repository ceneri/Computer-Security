#define _GNU_SOURCE
#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>
#include <string.h>
#include <crypt.h>
#include <semaphore.h>
#include <pthread.h>
#include <unistd.h>
#include <sys/types.h>
#include <signal.h>
#include <time.h>

#include "pt_brute_force.h"
#include "p_utils.h"


int threeCharIndexes[] = {0,1,2,3};
int fourCharIndexes[] = {1,2,3,4}; 
char alphabet[] = {48,49,50,51,52,53,54,55,56,57,
                    65,66,67,68,69,70,71,72,73,74,75,76,77,78,79,80,81,82,83,84,85,86,87,88,89,90,
                    97,98,99,100,101,102,103,104,105,106,107,108,109,110,111,112,113,114,115,116,
                    117,118,119,120,121,122}; 

/**
 * Returns BASICCOMBOS array of all possible password strings combinations of
 * 2 characters. Takes as input the number of possible combinations NUMBEROFBASICCOMBINATIONS
 * 
 * https://stackoverflow.com/questions/5935933/dynamically-create-an-array-of-strings-with-malloc
 */
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
            index++;
        }
    }
    
    return basicCombos;
}                      
 
/**
 * Function called by crackSingle to run a multi threaded brute force search for a single password.
 * From single_thread_data ARGUMENT obtains multiple arguments
 * 
 * https://stackoverflow.com/questions/1352749/multiple-arguments-to-function-called-by-pthread-create
 */
 void *brute_force_single_func( void *arguments){
    
    //Argument struct
    struct single_thread_data *args;
    args = (struct single_thread_data*) arguments;

    //Get encrypted password and salt
    char *cryptPasswd = args->cryptPasswd;
    char *salt = getSalt(cryptPasswd);
    
    //Allocate string used as combination
    char potentialPasswd[5];
    potentialPasswd[4] = '\0';
    
    //string and pointer used by crypt_r()
    //https://stackoverflow.com/questions/9335777/crypt-r-example
    char *enc = malloc (sizeof(char)*14);
    enc[13] = '\0';
    struct crypt_data data[1] = {0};
    
    //Populate all possible combinations of 2 characters 
    char **basicCombos;
    int numberOfTwoCharCombos = sizeof(alphabet) * sizeof(alphabet);
    basicCombos = populateTwoCharCombos(numberOfTwoCharCombos);
    
    bool found;
    bool onlyThreeChars = (args->pwlen == 3); 
    
    //Default indexes
    int *charIndices = fourCharIndexes;

    for ( int k = args->start_indx; k < args->end_indx && (*args->done) == 0; k++){

        potentialPasswd[0] = alphabet[k];
        //printf("K: %c\n", potentialPasswd[0]);
        
        if ( onlyThreeChars ){
            k = sizeof(alphabet);               //Main loop will only run once
            (*potentialPasswd)++;               //Remove first character from string           
            charIndices = threeCharIndexes;     //New indexes
        } 
        
        for (int j = 0; j < sizeof(alphabet) && (*args->done) == 0; j++){

            //Second character
            potentialPasswd[charIndices[0]] = alphabet[j];
        
            for (int i = 0; i < numberOfTwoCharCombos && (*args->done) == 0; i++){
                //Third and Fourth characters
                potentialPasswd[charIndices[1]] = basicCombos[i][0];
                potentialPasswd[charIndices[2]] = basicCombos[i][1];
                
                //Check for solution
                enc = crypt_r(potentialPasswd, salt, (void *)&data);
                found = (strcmp(cryptPasswd, enc) == 0);
                
                //If found save password and set DONE to one (Will stop every thread)
                if ( found ){
                    sem_wait(&args->t_lock);
                    strcpy(args->passwd, potentialPasswd);
                    (*args->done) = 1;
                    //https://www.geeksforgeeks.org/pthread_self-c-example/
                    //printf("Thread %ld found Password: %s\n", pthread_self(), args->passwd);
                    sem_post(&args->t_lock);                       
                }
                
            }
        }       
        
    }

    return NULL;
} 

/**
 * Function called by crackSpeedy to run a multi threaded brute force search for multiple password.
 * From multiple_thread_data ARGUMENT obtains multiple arguments
 * 
 * https://stackoverflow.com/questions/1352749/multiple-arguments-to-function-called-by-pthread-create
 */
void *brute_force_multiple_func( void *arguments){
    
    //Argument struct
    struct multiple_thread_data *args;
    args = (struct multiple_thread_data*) arguments;
    
    //Create its own copy of encrypted passwords
    sem_wait(&args->t_lock);
    char **cryptPasswds;
    cryptPasswds = getCryptPasswds(args->fname, args->numUsers);
    sem_post(&args->t_lock);
    
    //Create array of corresponding salts
    char **c_salts;
    c_salts = getSalts(cryptPasswds, args->numUsers);
    
    //Allocate string used as combination
    char potentialPasswd[5];
    potentialPasswd[4] = '\0';
    
    //string and pointer used by crypt_r()
    //https://stackoverflow.com/questions/9335777/crypt-r-example
    char *enc = malloc (sizeof(char)*14);
    enc[13] = '\0';
    struct crypt_data data[1] = {0};
    
    //Populate all possible combinations of 2 characters 
    char **basicCombos;
    int numberOfTwoCharCombos = sizeof(alphabet) * sizeof(alphabet);
    basicCombos = populateTwoCharCombos(numberOfTwoCharCombos);
    
    bool found;
    bool onlyThreeChars = (args->pwlen == 3);
    
    //Default indexes
    int *charIndices = fourCharIndexes; 

    for ( int k = args->start_indx; k < args->end_indx; k++){
        
        potentialPasswd[0] = alphabet[k];
        //printf("K: %c\n", potentialPasswd[0]);
        
        if ( onlyThreeChars ){
            k = sizeof(alphabet);               //Main loop will only run once
            (*potentialPasswd)++;               //Remove first character from string
            charIndices = threeCharIndexes;     //New indexes
        } 
        
        for (int j = 0; j < sizeof(alphabet); j++){
            
            //Second character
            potentialPasswd[charIndices[0]] = alphabet[j];
        
            for (int i = 0; i < numberOfTwoCharCombos; i++){
                //Third and Fourth characters
                potentialPasswd[charIndices[1]] = basicCombos[i][0];
                potentialPasswd[charIndices[2]] = basicCombos[i][1];
                
                for (int i = 0; i < args->numUsers && (*args->done) == 0; i++){
                    
                    //Check for matching encrypted password
                    enc = crypt_r(potentialPasswd, c_salts[i], (void *)&data);
                    found = (strcmp(cryptPasswds[i], enc) == 0);
                    
                    if ( found ){
                        sem_wait(&args->t_lock);
                        strcpy(args->passwds[i], potentialPasswd);
                        //https://www.geeksforgeeks.org/pthread_self-c-example/
                        //printf("Thread %ld found Password: %s\n", pthread_self(), args->passwds[i]);                  
                        sem_post(&args->t_lock);                       
                    }
                }
                
                
            }
        }
        
    }

    return NULL;
}

void *brute_force_stealthy_func( void *arguments){
    return NULL;
}

