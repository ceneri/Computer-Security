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

#include "crack.h"


char alphabet[] = {48,49,50,51,52,53,54,55,56,57,
                    65,66,67,68,69,70,71,72,73,74,75,76,77,78,79,80,81,82,83,84,85,86,87,88,89,90,
                    97,98,99,100,101,102,103,104,105,106,107,108,109,110,111,112,113,114,115,116,
                    117,118,119,120,121,122};

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
 
 
 //https://stackoverflow.com/questions/1352749/multiple-arguments-to-function-called-by-pthread-create
//https://courses.engr.illinois.edu/cs241/fa2010/ppt/10-pthread-examples.pdf
struct single_thread_data{
    int pwlen;
    int start_indx;
    int end_indx;
    char *cryptPasswd;
    char *passwd;
    bool *done;
    sem_t t_lock; 
};
 
char* getSalt(char *cryptPasswd){
    char *t_salt = malloc(sizeof(char)*3);
    strncpy(t_salt, cryptPasswd, 2);
    t_salt[2] = '\0';
    
    return t_salt;
}
 
void *brute_force_single_func( void *arguments){
    
    struct single_thread_data *args;
    args = (struct single_thread_data*) arguments;

    char *cryptPasswd = args->cryptPasswd;
    char *salt = getSalt(cryptPasswd);
    
    char potentialPasswd[5];
    potentialPasswd[4] = '\0';
    
    //https://stackoverflow.com/questions/9335777/crypt-r-example
    char *enc = malloc (sizeof(char)*14);
    enc[13] = '\0';
    struct crypt_data data[1] = {0};
    
    //maybe they could share em
    char **basicCombos;
    int numberOfTwoCharCombos = sizeof(alphabet) * sizeof(alphabet);
    basicCombos = populateTwoCharCombos(numberOfTwoCharCombos);
    
    //Indexes depending on password size
    int threeCharIndices[] = {0,1,2,3};
    int fourCharIndices[] = {1,2,3,4};
    
    bool found;
    bool onlyThreeChars = (args->pwlen == 3); 
    
    int *charIndices = fourCharIndices;

    for ( int k = args->start_indx; k < args->end_indx && (*args->done) == 0; k++){

        potentialPasswd[0] = alphabet[k];
        printf("K: %c\n", potentialPasswd[0]);
        
        if ( onlyThreeChars ){
            k = sizeof(alphabet);       //Main loop will only run once
            (*potentialPasswd)++;       //Remove first character from string           
            charIndices = threeCharIndices;     //New indexes
        } 
        
        for (int j = 0; j < sizeof(alphabet) && (*args->done) == 0; j++){

            //second character
            potentialPasswd[charIndices[0]] = alphabet[j];
        
            for (int i = 0; i < numberOfTwoCharCombos && (*args->done) == 0; i++){
                //Third and Fourth characters
                potentialPasswd[charIndices[1]] = basicCombos[i][0];
                potentialPasswd[charIndices[2]] = basicCombos[i][1];
                
                enc = crypt_r(potentialPasswd, salt, (void *)&data);
                found = (strcmp(cryptPasswd, enc) == 0);
                
                if ( found ){
                    sem_wait(&args->t_lock);
                    strcpy(args->passwd, potentialPasswd);
                    (*args->done) = 1;
                    //https://www.geeksforgeeks.org/pthread_self-c-example/
                    //printf("Thread %ld found a password: %s\n", pthread_self(), args->passwd);
                    //printf("Password: %s \n", args->passwd);
                    sem_post(&args->t_lock);                       
                }
                
            }
        }
        
        
        
    }

    return NULL;
} 

/*
 * Find the plain-text password PASSWD of length PWLEN for the user USERNAME 
 * given the encrypted password CRYPTPASSWD.
 */
void crackSingle(char *username, char *cryptPasswd, int pwlen, char *passwd) {
    
    int THREADS = /*4 6;*/ 12;
    //char four_thread_indexes[] = {0,16,32,47,62};
    //char six_thread_indexes[] = {0,11,22,32,42,52,62};
    char twelve_thread_indexes[] = {0,6,12,17,22,27,32,37,42,47,52,57,62};
    
    //http://pages.cs.wisc.edu/~remzi/Classes/537/Fall2008/Notes/threads-semaphores.txt
    sem_t write_lock;
    sem_init(&write_lock, 0, 1);
    
    bool done = 0;

    //http://cs.umw.edu/~finlayson/class/fall16/cpsc425/notes/04-pthreads.html
    pthread_t threads[THREADS];
    struct single_thread_data t_arguments[THREADS];
    
    int thread_i = 0;
    for (int a = 0; a < THREADS; a++) {
        t_arguments[a].pwlen = pwlen;
        t_arguments[a].passwd = passwd;
        t_arguments[a].cryptPasswd = cryptPasswd;
        t_arguments[a].start_indx = twelve_thread_indexes[thread_i];
        t_arguments[a].end_indx = twelve_thread_indexes[++thread_i];
        t_arguments[a].done = &done;
    }
        
    for (int t = 0; t < THREADS; t++) {
        //https://stackoverflow.com/questions/9914049/difficulty-passing-struct-through-pthread-create
        (void) pthread_create(&threads[t], NULL, brute_force_single_func, (void *)&t_arguments[t]);  
    }

    for (int t = 0; t < THREADS; t++) {
        (void) pthread_join((pthread_t)threads[t], NULL);
    }
}

/*
 * Find the plain-text passwords PASSWDS of length PWLEN for the users found
 * in the old-style /etc/passwd format file at pathe FNAME.
 */
void crackMultiple(char *fname, int pwlen, char **passwds) { 

    crackSpeedy(fname, pwlen, passwds);
    
    //Initialize binary semaphore
    //http://pages.cs.wisc.edu/~remzi/Classes/537/Fall2008/Notes/threads-semaphores.txt
    /*sem_t lock;
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

    sem_post(&lock);*/

} 


//https://stackoverflow.com/questions/1352749/multiple-arguments-to-function-called-by-pthread-create
//https://courses.engr.illinois.edu/cs241/fa2010/ppt/10-pthread-examples.pdf
struct thread_data {
    int start_indx;
    int end_indx;
    char *fname;
    int pwlen;
    char **passwds;
    char **cryptPasswds;
    int numUsers;
    sem_t t_lock;
    int *unlocked_passwords;
    bool done;
    
};

//https://stackoverflow.com/questions/1352749/multiple-arguments-to-function-called-by-pthread-create
void *brute_force_func( void *arguments){
    
    struct thread_data *args;
    args = (struct thread_data*) arguments;
    
    sem_wait(&args->t_lock);
    char **cryptPasswds;
    cryptPasswds = getCryptPasswds(args->fname, args->numUsers);
    sem_post(&args->t_lock);
    
    char **c_salts;
    c_salts = getSalts(cryptPasswds, args->numUsers);
    
    char **basicCombos;
    int numberOfTwoCharCombos = sizeof(alphabet) * sizeof(alphabet);
    basicCombos = populateTwoCharCombos(numberOfTwoCharCombos);
    
    //Indexes depending on password size
    int threeCharIndices[] = {0,1,2,3};
    int fourCharIndices[] = {1,2,3,4};
    
    bool onlyThreeChars = (args->pwlen == 3); 

    char potentialPasswd[5];
    potentialPasswd[4] = '\0';    
    
    //https://stackoverflow.com/questions/9335777/crypt-r-example
    char *enc = malloc (sizeof(char)*14);
    enc[13] = '\0';
    struct crypt_data data[1] = {0};

    for ( int k = args->start_indx; k < args->end_indx; k++){
        

        potentialPasswd[0] = alphabet[k];
        int *charIndices = fourCharIndices;
        //printf("K: %c\n", potentialPasswd[0]);
        
        if ( onlyThreeChars ){
            k = sizeof(alphabet);       //Main loop will only run once
            (*potentialPasswd)++;       //Remove first character from string
            
            charIndices = threeCharIndices;     //New indexes
        } 
        
        for (int j = 0; j < sizeof(alphabet); j++){
            
            //second character
            potentialPasswd[charIndices[0]] = alphabet[j];
        
            for (int i = 0; i < numberOfTwoCharCombos; i++){
                //Third and Fourth characters
                potentialPasswd[charIndices[1]] = basicCombos[i][0];
                potentialPasswd[charIndices[2]] = basicCombos[i][1];
                
                potentialPasswd[charIndices[3]] = '\0';
                
                bool found;
                for (int i = 0; i < args->numUsers; i++){
                    
                    enc = crypt_r(potentialPasswd, c_salts[i], (void *)&data);
                    found = (strcmp(cryptPasswds[i], enc) == 0);
                    
                    if ( found ){
                        sem_wait(&args->t_lock);
                        strcpy(args->passwds[i], potentialPasswd);
                        //https://www.geeksforgeeks.org/pthread_self-c-example/
                        //printf("Thread %ld found a password: %s\n", pthread_self(), args->passwds[i]);
                        //printf("Password: %s \n", args->passwds[i]);
                        sem_post(&args->t_lock);                       
                    }
                }
                
                
            }
        }
        
        
        
    }

    return NULL;
}

/*
 * Find the plain-text passwords PASSWDS of length PWLEN for the users found
 * in the old-style /etc/passwd format file at pathe FNAME.
 */
void crackSpeedy(char *fname, int pwlen, char **passwds) { 

    int THREADS = /*6;*/ 12;
    
    //char six_thread_indexes[] = {0,11,22,32,42,52,62};
    char twelve_thread_indexes[] = {0,6,12,17,22,27,32,37,42,47,52,57,62};
    
    //http://pages.cs.wisc.edu/~remzi/Classes/537/Fall2008/Notes/threads-semaphores.txt
    sem_t write_lock;
    sem_init(&write_lock, 0, 1);
    
    int numUsers = countLinesInFile(fname);
    
    //int unlocked_passwords = 0;

    //http://cs.umw.edu/~finlayson/class/fall16/cpsc425/notes/04-pthreads.html
    pthread_t threads[THREADS];
    struct thread_data t_arguments[THREADS];
    
    int thread_i = 0;
    for (int a = 0; a < THREADS; a++) {
        t_arguments[a].fname = fname;
        t_arguments[a].pwlen = pwlen;
        t_arguments[a].passwds = passwds;
        t_arguments[a].numUsers = numUsers;
        t_arguments[a].t_lock = write_lock; 
        t_arguments[a].start_indx = twelve_thread_indexes[thread_i];
        t_arguments[a].end_indx = twelve_thread_indexes[++thread_i];
        //t_arguments[a].unlocked_passwords = &unlocked_passwords;
    }
        
    for (int t = 0; t < THREADS; t++) {
        //https://stackoverflow.com/questions/9914049/difficulty-passing-struct-through-pthread-create
        (void) pthread_create(&threads[t], NULL, brute_force_func, (void *)&t_arguments[t]);  
    }

    for (int t = 0; t < THREADS; t++) {
        (void) pthread_join((pthread_t)threads[t], NULL);
    }

}









void *brute_force_stealthy_func( void *arguments){
    
    /*long CPU = .01;
    
    struct timeval tv1, tv2;
    gettimeofday(&tv1, NULL);
    unsigned long ms;    
    
    struct thread_data2 *args;
    args = (struct thread_data2*) arguments;

    char *cryptPasswd = args->cryptPasswd;
    //char *username = args->username;
    
    //get a helper getSalts() calls getSalt()
    //Obtain salt from password/user name salt
    char salt[3];
    strncpy(salt, cryptPasswd, 2);
    salt[2] = '\0';
    
    //maybe they could share em
    char **basicCombos;
    int numberOfTwoCharCombos = sizeof(alphabet) * sizeof(alphabet);
    basicCombos = populateTwoCharCombos(numberOfTwoCharCombos);
    
    //Indexes depending on password size
    int threeCharIndices[] = {0,1,2,3};
    int fourCharIndices[] = {1,2,3,4};
    
    bool onlyThreeChars = (args->pwlen == 3); 

    char potentialPasswd[5];
    potentialPasswd[4] = '\0';    
    
    //https://stackoverflow.com/questions/9335777/crypt-r-example
    char *enc = malloc (sizeof(char)*14);
    enc[13] = '\0';
    struct crypt_data data[1] = {0};
    
    bool found;
   

    for ( int k = args->start_indx; k < args->end_indx && (*args->done) == 0; k++){

        potentialPasswd[0] = alphabet[k];
        int *charIndices = fourCharIndices;
        printf("K: %c\n", potentialPasswd[0]);
        
        if ( onlyThreeChars ){
            k = sizeof(alphabet);       //Main loop will only run once
            (*potentialPasswd)++;       //Remove first character from string
            
            charIndices = threeCharIndices;     //New indexes
        } 
        
        gettimeofday(&tv2, NULL); 
        ms = (tv2.tv_sec-tv1.tv_sec)*1000000+(tv2.tv_usec-tv1.tv_usec); 
        sleep(ms*CPU);
        //gettimeofday(&tv1, NULL);
        
        for (int j = 0; j < sizeof(alphabet) && (*args->done) == 0; j++){
            
            
            
            //second character
            potentialPasswd[charIndices[0]] = alphabet[j];
        
            for (int i = 0; i < numberOfTwoCharCombos && (*args->done) == 0; i++){
                //Third and Fourth characters
                potentialPasswd[charIndices[1]] = basicCombos[i][0];
                potentialPasswd[charIndices[2]] = basicCombos[i][1];
                
                potentialPasswd[charIndices[3]] = '\0';
                

                    
                enc = crypt_r(potentialPasswd, salt, (void *)&data);
                found = (strcmp(cryptPasswd, enc) == 0);
                
                if ( found ){
                    sem_wait(&args->t_lock);
                    strcpy(args->passwd, potentialPasswd);
                    (*args->done) = 1;
                    //https://www.geeksforgeeks.org/pthread_self-c-example/
                    printf("Thread %ld found a password: %s\n", pthread_self(), args->passwd);
                    printf("Password: %s \n", args->passwd);
                    sem_post(&args->t_lock);                       
                }
                
            }
        }
        
        
        
    }
*/
    return NULL;
}

/*
 * Find the plain-text password PASSWD of length PWLEN for the user USERNAME 
 * given the encrypted password CRYPTPASSWD withoiut using more than MAXCPU
 * percent of any processor.
 */
void crackStealthy(char *username, char *cryptPasswd, int pwlen, char *passwd, int maxCpu) { 
   // int THREADS = 4/*6; 12*/;
    
   /* char four_thread_indexes[] = {0,16,32,47,62};
    //char six_thread_indexes[] = {0,11,22,32,42,52,62};
    //char twelve_thread_indexes[] = {0,6,12,17,22,27,32,37,42,47,52,57,62};
    
    //http://pages.cs.wisc.edu/~remzi/Classes/537/Fall2008/Notes/threads-semaphores.txt
    sem_t write_lock;
    sem_init(&write_lock, 0, 1);
    
    //int numUsers = countLinesInFile(fname);
    
    bool done = 0;
    
    //int unlocked_passwords = 0;

    //http://cs.umw.edu/~finlayson/class/fall16/cpsc425/notes/04-pthreads.html
    pthread_t threads[THREADS];
    struct thread_data2 t_arguments[THREADS];
    
    int thread_i = 0;
    for (int a = 0; a < THREADS; a++) {
        //t_arguments[a].username = username;
        t_arguments[a].pwlen = pwlen;
        t_arguments[a].passwd = passwd;
        t_arguments[a].cryptPasswd = cryptPasswd;
        t_arguments[a].t_lock = write_lock; 
        t_arguments[a].start_indx = four_thread_indexes[thread_i];
        t_arguments[a].end_indx = four_thread_indexes[++thread_i];
        t_arguments[a].done = &done;
        //t_arguments[a].unlocked_passwords = &unlocked_passwords;
    }
        
    for (int t = 0; t < THREADS; t++) {
        //https://stackoverflow.com/questions/9914049/difficulty-passing-struct-through-pthread-create
        (void) pthread_create(&threads[t], NULL, brute_force_single_func, (void *)&t_arguments[t]);  
    }

    for (int t = 0; t < THREADS; t++) {
        (void) pthread_join((pthread_t)threads[t], NULL);
    }*/
}