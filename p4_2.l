%{
#include <stdio.h>
%}

%%

([cC][hH][aA][rR][uU][sS][aA][tT])    { printf("university"); }
\n                                      { printf("\n"); }
.                                       { printf("%s", yytext); }

%%

int main(void) {
    yylex();
    return 0;
}

int yywrap(void) {
    return 1;
}