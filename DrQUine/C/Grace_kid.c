#include <stdio.h>
/*
	Graceful self-replication
*/
#define FILENAME "Grace_kid.c"
#define CODE "#include <stdio.h>%c/*%c%cGraceful self-replication%c*/%c#define FILENAME %cGrace_kid.c%c%c#define CODE %c%s%c%c#define FT() int main(){FILE *f=fopen(FILENAME,%cw%c);if(f){fprintf(f,CODE,10,10,9,10,10,34,34,10,34,CODE,34,10,34,34,10);fclose(f);}return 0;}%cFT()"
#define FT() int main(){FILE *f=fopen(FILENAME,"w");if(f){fprintf(f,CODE,10,10,9,10,10,34,34,10,34,CODE,34,10,34,34,10);fclose(f);}return 0;}
FT()