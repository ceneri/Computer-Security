/* 
 * Copyright (C) 2018 Cesar Neri - All Rights Reserved.
 * You may not use, distribute, or modify this code without 
 * the written permission of the copyright holder.
 */

#ifndef __P_UTILS__
#define __P_UTILE__ 

/*
 * Returns the number of lines in the file at specific path
 */
int countLinesInFile(char *fname);

/*
 * Returns salt string of an encrypted password string
 */
char* getSalt(char *cryptPasswd);

/*
 * Returns array of salt string corresponding to the encrypted password string of N users
 */
char** getSalts(char **cryptPasswds, int numUsers);

/*
 * Returns an array of all encrypted passwords found in the file located in specific path
 */
char** getCryptPasswds(char *fname, int numUsers) ;

#endif