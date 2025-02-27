%option noyywrap

%{
    #include <stdio.h>
    int v = 0, c = 0;
%}

%%

[aeiouAEIOU]    { v++; }        
[a-zA-Z]        { c++; }         
[ \t\n]          ;                
.                ;                 

%%

int main() 
{
    printf("Enter the string: ");
    yylex();                      
    printf("Number of vowels: %d\n", v);
    //printf("Number of alphabetic characters: %d\n", c);   
    return 0;   
}
