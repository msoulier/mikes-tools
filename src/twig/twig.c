// vim: ts=4 sw=4 et ai:
#include <stdio.h>
#include <stdlib.h>
#include <sys/types.h>
#include <dirent.h>
#include <assert.h>
#include <string.h>
#include <unistd.h>
#include <sys/stat.h>
#include <errno.h>

int soption, doption, aoption;

int
compare(const void *a, const void *b)
{
    /* Both are pointers to characters. */
    char * const *string1;
    char * const *string2;

    string1 = a; string2 = b;

    return strcmp(*string1, *string2);
}

void 
listdir(char *dir, int level)
{
    DIR *directory;
    struct dirent *entry;
    struct stat filestat;
    char **dirlist, *fullpath, errormsg[256]; 
    char linkpath[1024], linkfullpath[1024];
    int listsize = 10;
    int i, j, nfiles, isdir, islnk, linkexists, linksize;

    /* Initially, the size of the array is 10. */
    dirlist = malloc(sizeof(char *) * listsize);
    assert( dirlist != NULL );
    /* Malloc a string for the full path. Needs to be the size of dir, plus
     * enough to hold the maximum file size permitted on Unix.
     */
    fullpath = malloc((sizeof(char *) * strlen(dir)) + 257);
    assert( fullpath != NULL );

    if ((directory = opendir(dir)) == NULL) {
        sprintf(errormsg, "ERROR: Can't open directory %s: %s\n",
                dir, strerror(errno));
        fprintf(stderr, "\n%s\n", errormsg);
        return;
    }
    /* Make an array to sort. */
    i = 0;
    while ((entry = readdir(directory)) != NULL) {
        if ((entry->d_name)[0] == '.') {
            // If the aoption is set, we want to follow dotfiles, but not ..
            if (aoption) {
                if (strlen(entry->d_name) > 1) {
                    if ((entry->d_name)[1] == '.') {
                        // It's .., skip it
                        continue;
                    }
                    // else we want to drop through and continue
                } else {
                    // it's . - skip it
                    continue;
                }
                // otherwise we want to follow it
            } else {
                continue;
            }
        }
        /* Double the size of the array if we go over. */
        if (i >= listsize) {
            listsize *= 2;
            dirlist = realloc(dirlist, sizeof(char *) * listsize);
        }
        dirlist[i] = malloc(sizeof(char) * (strlen(entry->d_name) + 1));
        strcpy(dirlist[i], entry->d_name);
        i++;
    }
    nfiles = i;
    /* Sort the array. */
    qsort(dirlist, nfiles, sizeof *dirlist, compare);

    /* Print out the files. */
    for (i = 0; i < nfiles; ++i) {
        /* Compose the full path to the file. */
        strcpy(fullpath, dir);
        /* Put a / on the end of the path if there isn't already one there. */
        if (fullpath[strlen(fullpath) - 1] != '/') {
            strcat(fullpath, "/");
        }
        strcat(fullpath, dirlist[i]);
        /* Stat the file. */
        if (lstat(fullpath, &filestat) != 0) {
            sprintf(errormsg, "ERROR: Cannot stat %s: %s",
                    fullpath, strerror(errno));
            fprintf(stderr, "\n%s\n", errormsg);
            continue;
        }
        isdir = 0;
        islnk = 0;
        linkexists = 0;
        /* Is this a directory? */
        if (S_ISDIR(filestat.st_mode)) {
            isdir = 1;
        } else if (S_ISLNK(filestat.st_mode)) {
            islnk = 1;
            if ((linksize = readlink(fullpath, linkpath, sizeof(linkpath))) < 0) {
                sprintf(errormsg, "ERROR: Could not resolve link %s: %s",
                        fullpath, strerror(errno));
                fprintf(stderr, "\n%s\n", errormsg);
                linkpath[0] = '\0';
            } else {
                /* Null terminate the link. */
                linkpath[linksize] = '\0';
                /* Is it an absolute path? */
                if (linkpath[0] == '/')
                    strcpy(linkfullpath, linkpath);
                /* Relative path starting with a .? */
                else if ((linkpath[0] == '.') &&
                         (linkpath[1] != '.') &&
                         (linkpath[1] == '/'))
                {
                    /* relative path like ./file */
                    strcpy(linkfullpath, dir);
                    strcat(linkfullpath, "/");
                    strcat(linkfullpath, linkpath + 2);
                }
                /* Normal relative link. */
                else
                {
                    strcpy(linkfullpath, dir);
                    strcat(linkfullpath, "/");
                    strcat(linkfullpath, linkpath);
                }
                /* Does it exist? */
                if (!access(linkfullpath, F_OK))
                    linkexists = 1;
            }
        }
        /* Now, if the directory option is set, and this is not a directory,
         * then we don't want to print it.
         */
        if (doption && !isdir) {
            continue;
        }
        /* Print out the header for the file. */
        for (j = 0; j < level; ++j) {
            printf("|    ");
        }
        /* Print out the last indent. */
        if (i == nfiles - 1) {
            printf("`-- ");
        } else {
            printf("|-- ");
        }
        /* Now, if the size option was used, print the size. */
        if (soption) {
            printf("[%9d] ", (int)filestat.st_size);
        }
        /* The filename... */
        printf("%s", dirlist[i]);
        /* If it's a link, print out the target. */
        if ((islnk) && (linkpath[0] != '\0'))
        {
            printf(" -> ");
            if (linkexists) {
                printf("%s", linkpath);
            }
            else {
                printf("(%s)", linkpath);
            }
        }
        printf("\n");
        if (isdir) {
            listdir(fullpath, level + 1);
        }
    }

    /* Clean up after ourselves. */
    closedir(directory);
    for (i = 0; i < nfiles; i++)
        free(dirlist[i]);
    free(dirlist);
    free(fullpath);
}

void
usage()
{
    fprintf(stderr, "Usage: twig [options] [path]\n");
    fprintf(stderr, "   Options:\n");
    fprintf(stderr, "       -h print help\n");
    fprintf(stderr, "       -a show dotfiles\n");
    fprintf(stderr, "       -d only show directories\n");
    fprintf(stderr, "       -s print file sizes\n");
    exit(1);
}

int 
main(int argc, char *argv[])
{
    char dir[1024], argchar;
    int i;

    aoption = doption = soption = 0;

    /* Parse arguments. */
    i = 0;
    while ((argchar = getopt(argc, argv, "asdh")) >= 0)
    {
        i++;
        switch (argchar)
        {
            case 'a': aoption = 1;
                      break;
            case 'd': doption = 1;
                      break;
            case 's': soption = 1;
                      break;
            case 'h': usage();
                      break;
            default:  usage();
        }
    }
    argc -= i;
    argv += i;
    if (argc <= 0)
        usage();
    else if (argc == 1)
        strcpy(dir, ".");
    else if (argc == 2)
        strcpy(dir, argv[1]);
    else
        usage();

    puts(dir);
    listdir(dir, 0);

    exit(0);
}
