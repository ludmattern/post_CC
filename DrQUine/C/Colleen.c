/*
	Quine Colleen for Dr_Quine project
*/
#include <stdio.h>
void helper();
int main(){
/*
	inside main comment
*/
	char*a="/*%c%cQuine Colleen for Dr_Quine project%c*/%c#include <stdio.h>%cvoid helper();%cint main(){%c/*%c%cinside main comment%c*/%c%cchar*a=%c%s%c;%c%cprintf(a,10,9,10,10,10,10,10,10,9,10,10,9,34,a,34,10,9,10,9,10,10,10,10);%c%chelper();%c}%cvoid helper(){}%c";
	printf(a,10,9,10,10,10,10,10,10,9,10,10,9,34,a,34,10,9,10,9,10,10,10,10);
	helper();
}
void helper(){}
