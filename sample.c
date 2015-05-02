#include<stdio.h>
#include<dlfcn.h>
#include<unistd.h>
#include<string.h>

int /*SO*/ p1;
int /*SO*/ p2;


char /*SO*/ pstr1[100];
char pstr2[100];

#include /*SO*/ "evalc_gen.h"

int main()
{
	p1 = 12;	
	strcpy(pstr1, "test string");

	// Eval code
	evalc("p2 = p1 * p1 + 100; pstr1[0] = 'T'");

	printf("p2 : %d\n", p2);
	printf("pstr1 : %s\n", pstr1);

	// Eval code	
	evalc("p1 /= 2; p2 -= 100");
	
	printf("p1 : %d  p2 : %d\n", p1, p2);

	// Eval code	
	evalc("strcpy(pstr1, \"AAAA\");");

	printf("pstr1 : %s\n", pstr1);

}


