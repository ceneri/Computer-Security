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
#include "pt_brute_force.h"
#include "p_utils.h"          
                        
                 
/**
 * Find the plain-text password PASSWD of length PWLEN for the user USERNAME 
 * given the encrypted password CRYPTPASSWD.
 */
void crackSingle(char *username, char *cryptPasswd, int pwlen, char *passwd) {
    
    bool done = 0;
    
    //http://pages.cs.wisc.edu/~remzi/Classes/537/Fall2008/Notes/threads-semaphores.txt
    sem_t write_lock;
    sem_init(&write_lock, 0, 1);
    
    int THREADS = /*6;*/ 12;
    
    //char six_thread_indexes[] = {0,11,22,32,42,52,62};
    char twelve_thread_indexes[] = {0,6,12,17,22,27,32,37,42,47,52,57,62};
    
    //Arrays of POSIX threads and their argument structs
    //http://cs.umw.edu/~finlayson/class/fall16/cpsc425/notes/04-pthreads.html
    pthread_t threads[THREADS];
    struct single_thread_data t_arguments[THREADS];
    
    //Create all the required threads, using the appropriate search indexes for each one
    int thread_i = 0;
    for (int a = 0; a < THREADS; a++) {
        t_arguments[a].pwlen = pwlen;
        t_arguments[a].passwd = passwd;
        t_arguments[a].cryptPasswd = cryptPasswd;
        t_arguments[a].start_indx = twelve_thread_indexes[thread_i];
        t_arguments[a].end_indx = twelve_thread_indexes[++thread_i];
        t_arguments[a].done = &done;
    }
        
    //Create threads
    for (int t = 0; t < THREADS; t++) {
        //https://stackoverflow.com/questions/9914049/difficulty-passing-struct-through-pthread-create
        (void) pthread_create(&threads[t], NULL, brute_force_single_func, (void *)&t_arguments[t]);  
    }

    //Wait for all thread to finish
    for (int t = 0; t < THREADS; t++) {
        (void) pthread_join((pthread_t)threads[t], NULL);
    }
}

/**
 * Find the plain-text passwords PASSWDS of length PWLEN for the users found
 * in the old-style /etc/passwd format file at pathe FNAME.
 */
void crackMultiple(char *fname, int pwlen, char **passwds) { 

    //Calls crackSpeedy for faster execution
    crackSpeedy(fname, pwlen, passwds);
} 

/**
 * Find the plain-text passwords PASSWDS of length PWLEN for the users found
 * in the old-style /etc/passwd format file at pathe FNAME in less than 15 min (Using POSIX threads).
 */
void crackSpeedy(char *fname, int pwlen, char **passwds) { 

    bool done = 0;
    
    //Count the number of users
    int numUsers = countLinesInFile(fname);
    
    //http://pages.cs.wisc.edu/~remzi/Classes/537/Fall2008/Notes/threads-semaphores.txt
    sem_t write_lock;
    sem_init(&write_lock, 0, 1);
    
    int THREADS = /*6;*/ 12;
    
    //char six_thread_indexes[] = {0,11,22,32,42,52,62};
    char twelve_thread_indexes[] = {0,6,12,17,22,27,32,37,42,47,52,57,62};

    //Arrays of POSIX threads and their argument structs
    //http://cs.umw.edu/~finlayson/class/fall16/cpsc425/notes/04-pthreads.html
    pthread_t threads[THREADS];
    struct multiple_thread_data t_arguments[THREADS];
    
    int thread_i = 0;
    for (int a = 0; a < THREADS; a++) {
        t_arguments[a].fname = fname;
        t_arguments[a].pwlen = pwlen;
        t_arguments[a].passwds = passwds;
        t_arguments[a].numUsers = numUsers;
        t_arguments[a].t_lock = write_lock; 
        t_arguments[a].start_indx = twelve_thread_indexes[thread_i];
        t_arguments[a].end_indx = twelve_thread_indexes[++thread_i];
        t_arguments[a].done = &done;
    }
        
    //Create threads
    for (int t = 0; t < THREADS; t++) {
        //https://stackoverflow.com/questions/9914049/difficulty-passing-struct-through-pthread-create
        (void) pthread_create(&threads[t], NULL, brute_force_multiple_func, (void *)&t_arguments[t]);  
    }

    //Wait for all thread to finish
    for (int t = 0; t < THREADS; t++) {
        (void) pthread_join((pthread_t)threads[t], NULL);
    }

}


/*
 * Find the plain-text password PASSWD of length PWLEN for the user USERNAME 
 * given the encrypted password CRYPTPASSWD without using more than MAXCPU
 * percent of any processor.
 */
void crackStealthy(char *username, char *cryptPasswd, int pwlen, char *passwd, int maxCpu) {

}