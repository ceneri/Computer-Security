/* 
 * Copyright (C) 2018 Cesar Neri - All Rights Reserved.
 * You may not use, distribute, or modify this code without 
 * the written permission of the copyright holder.
 */

#ifndef __PT_BRUTE_FORCE__
#define __PT_BRUTE_FORCE__

 /*
 * Used to pass arguments to thread brute_force_single_func function 
 * 
 * https://stackoverflow.com/questions/1352749/multiple-arguments-to-function-called-by-pthread-create
 * https://courses.engr.illinois.edu/cs241/fa2010/ppt/10-pthread-examples.pdf
 */
struct single_thread_data{
    int pwlen;
    int start_indx;
    int end_indx;
    char *cryptPasswd;
    char *passwd;
    bool *done;
    sem_t t_lock; 
};

/*
 * Used to pass arguments to thread brute_force_multiple_func function 
 * 
 * https://stackoverflow.com/questions/1352749/multiple-arguments-to-function-called-by-pthread-create
 * https://courses.engr.illinois.edu/cs241/fa2010/ppt/10-pthread-examples.pdf
 */
struct multiple_thread_data {
    int pwlen;
    int numUsers;
    int start_indx;
    int end_indx;
    char *fname;
    char **passwds;
    char **cryptPasswds;
    int *unlocked_passwords;
    bool *done;
    sem_t t_lock;   
}; 

/*
 * Returns array of all possible password strings combinations of 2 characters. 
 */
char** populateTwoCharCombos(int numberOfBasicCombos);

/*
 * Function called by crackSingle to run a single threaded brute force search for a single password.
 */
void *brute_force_single_func( void *arguments);

/*
 * Function called by crackSpeedy to run a single threaded brute force search for a multiple passwords.
 */
void *brute_force_multiple_func( void *arguments);

/*
 * Function called by crackStealthy to run a single threaded brute force search for a single password.
 */
void *brute_force_stealthy_func( void *arguments);

#endif