%option noyywrap

%{
    #include <stdio.h>
    int v = 0, c = 0;
%}

%%

[aeiouAEIOU]    { v++; }         // Increment vowel count
[a-zA-Z]        { c++; }         // Increment character count (ignoring digits, special chars)
[ \t\n]          ;                // Ignore spaces, tabs, and newlines
.                ;                // Ignore other characters

%%

int main() 
{
    printf("Enter the string: ");
    yylex();                      // Invoke lexer to process input
    printf("Number of vowels: %d\n", v);
    //printf("Number of alphabetic characters: %d\n", c);  // Uncomment if needed
    return 0;  // Return 0 to indicate successful execution
}
