#define _XOPEN_SOURCE
#define _GNU_SOURCE
#include <time.h>
#include <stdio.h>
#include <stdlib.h>
#include <stdarg.h>
#include <unistd.h>
#include <string.h>
#include <ctype.h>

#define TIMEFLEN 8
#define TSTAMP_SIZE 1024

void dbg_printf(const char *fname, const int lineno, const char *fmt, ...)
{
    va_list args;
    va_start(args, fmt);
    time_t now = time(NULL);
    struct tm *nowtm = localtime(&now);
    char ts[TSTAMP_SIZE];
    strftime(ts, TSTAMP_SIZE, "%c", nowtm);
    fprintf(stderr, "%s [DEBUG] ", ts);
    fprintf(stderr, "[%s:%d] ", fname, lineno);
    vfprintf(stderr, fmt, args);
    va_end(args);
}

/*
 * A debug macro that compiles out if MDEBUG is not set, and compiles to an
 * fprintf out stderr otherwise.
 */
#ifdef DEBUG
#define mdbgf(...) dbg_printf (__FILE__, __LINE__, __VA_ARGS__)
#else
#define mdbgf(...)
#endif

/*
 * This program is a simple terminal countdown program. Given a number of
 * seconds, it will count down to zero.
 */
const int sleeptime = 1;
int dmenu = 0;
char *event = NULL;
int raw_mode = 0;
char *command = NULL;

void
print_time (unsigned int seconds)
{
    unsigned int hours, minutes;

    if (seconds < 0) {
        return;
    }

    hours = seconds / 3600;
    seconds -= hours * 3600;
    minutes = seconds / 60;
    seconds -= minutes * 60;

    if (! raw_mode) {
        printf("\r");
        printf("                              ");
        printf("\r");
    }
    printf("Time remaining");
    if (event != NULL) {
        printf(" until %s", event);
    }
    printf(": %2d:%02d:%02d", hours, minutes, seconds);
    if (raw_mode) {
        printf("\n");
    }
    fflush(stdout);
}

time_t
parse_until(char *suntil, time_t now, struct tm *p_until_tm) {
    if ((suntil == NULL) || (p_until_tm == NULL)) {
        return -1;
    }
    const char *errmsg = "The format for until must be HH:MM:SS";
    // The expected format is HH:MM:SS
    if (strnlen(suntil, TIMEFLEN) != TIMEFLEN) {
        fprintf(stderr, "%s\n", errmsg);
        return -1;
    } else {
        // Length is good. Is the format right?
        if ((isdigit(suntil[0])) &&
            (isdigit(suntil[1])) &&
            (suntil[2] == ':')   &&
            (isdigit(suntil[3])) &&
            (isdigit(suntil[4])) &&
            (suntil[5] == ':')   &&
            (isdigit(suntil[6])) &&
            (isdigit(suntil[7])))
        {
            mdbgf("parse_until: format looks good\n");
        } else {
            fprintf(stderr, "%s\n", errmsg);
            return -1;
        }
    }
    mdbgf("parse_until: suntil is %s\n", suntil);
    if (strptime(suntil, "%T", p_until_tm) == NULL) {
        fprintf(stderr, "%s\n", errmsg);
        return -1;
    }
    return mktime(p_until_tm) - now;
}

int
parse_args(int argc, char *argv[], time_t now, struct tm *p_until_tm) {
    const char usage[] = "Usage: countdown\n\t[-s <sec> ]\n\t[-m <min>]\n\t[-h <hr>]\n\t[-d (enable dmenu)]\n\t[-e <event description>]\n\t[-u <until time|ie. H:MM:SS]\n\t[-r (raw mode)]\n\t[-c <command>]\n";
    int opt;
    time_t seconds = 0;
    time_t minutes = 0;
    time_t hours = 0;
    time_t from = 0;
    char *suntil = NULL;

    if (argc < 2)
    {
        fprintf(stderr, usage);
        return 0;
    }
    while ((opt = getopt(argc, argv, "rds:m:h:e:u:c:")) != -1) {
        //fprintf(stderr, "opt is %c, optarg is %s\n", opt, optarg);
        switch (opt) {
            case 's':
                seconds = atoi(optarg);
                break;
            case 'm':
                minutes = atoi(optarg);
                break;
            case 'h':
                hours = atoi(optarg);
                break;
            case 'u':
                suntil = optarg;
                break;
            case 'd':
                dmenu = 1;
                break;
            case 'e':
                event = optarg;
                break;
            case 'c':
                command = optarg;
                break;
            case 'r':
                raw_mode = 1;
                break;
            default:
                fprintf(stderr, usage);
                return 0;
        }
    }

    from = seconds + minutes*60 + hours*3600;
    if ((from == 0) && (suntil == NULL)) {
        fprintf(stderr, usage);
        return 0;
    } else if (suntil != NULL) {
        if (from > 0) {
            fprintf(stderr, "ERROR: The until argument is mutually exclusive with the other time options.\n");
            fprintf(stderr, usage);
            return 0;
        } else {
            from = parse_until(suntil, now, p_until_tm);
            mdbgf("parse_until returned a from of %d\n", from);
            if (from < 0) {
                return 0;
            }
        }
    } else if (dmenu && (command != NULL)) {
        fprintf(stderr, "ERROR: The dmenu and command options are mutually exclusive.\n");
        fprintf(stderr, usage);
        return 0;
    }

    mdbgf("from is %ld\n", from);
    mdbgf("raw mode is %d\n", raw_mode);
    mdbgf("dmenu is %d\n", dmenu);
    if (command != NULL) {
        mdbgf("command is '%s'\n", command);
    }

    return from;
}

int
main (int argc, char *argv[])
{
    unsigned int from;
    time_t now = 0;
    struct tm now_tm;
    struct tm until_tm;
    time_t endtime = 0;

    tzset();

    time(&now);
    localtime_r(&now, &now_tm);

    // Copy now into the until. For now we only support same day.
    memcpy(&until_tm, &now_tm, sizeof(struct tm));

    if ((from = parse_args(argc, argv, now, &until_tm)) == 0) {
        exit(1);
    }
    // Compute endtime using requested span.
    endtime = now + from;
    
    mdbgf("now time: %ld\n", now);
    mdbgf("computed endtime: %ld\n", endtime);

    #ifndef DEBUG
    if (! raw_mode) {
        // Clear the screen, works with vt100 terminals.
        puts("\033[2J");
        // And move cursor to home.
        puts("\033[H");
    }
    #endif

    while (now < endtime) {
        // Don't rely on sleep to assume that one second has gone by.
        // Programs get interrupted. Laptops sleep. Etc.
        time(&now);
        from = endtime - now;
        // We could wake up here and print nonsense, so check again.
        if (now >= endtime) {
            mdbgf("mid-loop check failed, from = %d\n", from);
            from = 0;
            break;
        }
        print_time(from);
        sleep(sleeptime);
    }
    mdbgf("broke out of main loop\n");
    print_time(from);
    printf("\n");

    if (dmenu) {
        system("echo -n Ok | dmenu -p \"Countdown at zero\"");
    } else if (command) {
        mdbgf("Executing command: '%s'\n", command);
        system(command);
    } else {
        printf("\a******************** ZERO! ********************\n");
    }

    exit(0);
}
