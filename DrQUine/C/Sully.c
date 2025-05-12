#define _GNU_SOURCE
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <fcntl.h>
#include <unistd.h>

/*
	Sully - Self-reproducing program with counter
*/

#define MYNAME strrchr("/" __FILE__, '/') + 1

int i = 5;

int main(void)
{
	char *filename;
	char *check_filename;
	char *compile_cmd;
	char *execute_cmd;
	int fd;

	if (i < 0)
		return 0;

	asprintf(&check_filename, "Sully_%d.c", i);
	if (strcmp(MYNAME, check_filename) == 0)
		i--;
	free(check_filename);

	asprintf(&filename, "Sully_%d.c", i);

	fd = open(filename, O_WRONLY | O_CREAT | O_TRUNC, 0644);
	if (fd < 0)
	{
		free(filename);
		return 1;
	}

	char *source = "#define _GNU_SOURCE%1$c#include <stdio.h>%1$c#include <stdlib.h>%1$c#include <string.h>%1$c#include <fcntl.h>%1$c#include <unistd.h>%1$c%1$c/*%1$c	Sully - Self-reproducing program with counter%1$c*/%1$c%1$c#define MYNAME strrchr(%2$c/%2$c __FILE__, '/') + 1%1$c%1$cint i = %3$d;%1$c%1$cint main(void)%1$c{%1$c	char *filename;%1$c	char *check_filename;%1$c	char *compile_cmd;%1$c	char *execute_cmd;%1$c	int fd;%1$c%1$c	if (i < 0)%1$c		return 0;%1$c%1$c	asprintf(&check_filename, %2$cSully_%%d.c%2$c, i);%1$c	if (strcmp(MYNAME, check_filename) == 0)%1$c		i--;%1$c	free(check_filename);%1$c%1$c	asprintf(&filename, %2$cSully_%%d.c%2$c, i);%1$c%1$c	fd = open(filename, O_WRONLY | O_CREAT | O_TRUNC, 0644);%1$c	if (fd < 0)%1$c	{%1$c		free(filename);%1$c		return 1;%1$c	}%1$c%1$c	char *source = %2$c%4$s%2$c;%1$c%1$c	dprintf(fd, source, 10, 34, i, source);%1$c	close(fd);%1$c	free(filename);%1$c%1$c	asprintf(&compile_cmd, %2$cgcc -Wall -Wextra -Werror Sully_%%d.c -o Sully_%%d%2$c, i, i);%1$c	system(compile_cmd);%1$c	free(compile_cmd);%1$c%1$c	if (i > 0)%1$c	{%1$c		asprintf(&execute_cmd, %2$c./Sully_%%d%2$c, i);%1$c		system(execute_cmd);%1$c		free(execute_cmd);%1$c	}%1$c%1$c	return 0;%1$c}";

	dprintf(fd, source, 10, 34, i, source);
	close(fd);
	free(filename);

	asprintf(&compile_cmd, "gcc -Wall -Wextra -Werror Sully_%d.c -o Sully_%d", i, i);
	system(compile_cmd);
	free(compile_cmd);

	if (i > 0)
	{
		asprintf(&execute_cmd, "./Sully_%d", i);
		system(execute_cmd);
		free(execute_cmd);
	}

	return 0;
}