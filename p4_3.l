%{
#include <stdio.h>
int char_count = 0;
int word_count = 0;
int line_count = 0;
%}

%%

\n           { line_count++; char_count++; }
[ \t]+       { char_count += yyleng; }
[^ \t\n]+   { word_count++; char_count += yyleng; }

%%

int main(void) {
    printf("Enter a string: ");
    yylex();
    printf("Characters : %d\n", char_count);
    printf("Words : %d\n", word_count);
    printf("Line : %d\n", line_count);
    return 0;
}

int yywrap(void) {
    return 1;
}
