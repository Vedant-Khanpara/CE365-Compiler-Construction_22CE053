%{
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

typedef struct {
    char name[100];
    int count;
} Symbol;

Symbol symbol_table[1000];
int symbol_count = 0;

typedef struct {
    char lexeme[100];
    int line;
} Error;

Error errors[100];
int error_count = 0;

int line_no = 1;

void add_to_symbol_table(char *name) {
    int i;

    for (i = 0; i < symbol_count; i++) {
        if (strcmp(symbol_table[i].name, name) == 0) {
            symbol_table[i].count++;
            return;
        }
    }

    strcpy(symbol_table[symbol_count].name, name);
    symbol_table[symbol_count].count = 1;
    symbol_count++;
}

void add_error(char *lexeme, int line) {
    strcpy(errors[error_count].lexeme, lexeme);
    errors[error_count].line = line;
    error_count++;
}

%}

DIGIT       [0-9]
LETTER      [a-zA-Z]
ID          {LETTER}({LETTER}|{DIGIT}|_)*
INTEGER     {DIGIT}+
FLOAT       {DIGIT}+\.{DIGIT}+([eE][+-]?{DIGIT}+)?
CHAR        \'([^\'\\\n]|\\[\'\"\\nrtbf0])\'
STRING      \"([^\"\\\n]|\\[\'\"\\nrtbf0])*\"
WHITESPACE  [ \t]+
INVALID_ID  {DIGIT}+{LETTER}+({LETTER}|{DIGIT}|_)*

%%

"/*"([^*]|"*"[^/])*"*/"    { /* Skip multi-line comments */ }
"//".*                      { /* Skip single-line comments */ }

\n                          { line_no++; }
{WHITESPACE}                { /* Skip whitespace */ }

"auto"|"break"|"case"|"char"|"const"|"continue"|"default"|"do"|"double"|"else"|"enum"|"extern"|"float"|"for"|"goto"|"if"|"int"|"long"|"register"|"return"|"short"|"signed"|"sizeof"|"static"|"struct"|"switch"|"typedef"|"union"|"unsigned"|"void"|"volatile"|"while" { 
    printf("Keyword: %s\n", yytext);
}

{ID} {
    printf("Identifier: %s\n", yytext);
    add_to_symbol_table(yytext);
}

{INTEGER}|{FLOAT}|{CHAR} {
    printf("Constant: %s\n", yytext);
}

{STRING} {
    printf("String: %s\n", yytext);
}

"["|"]"|"("|")"|"{"|"}"|";"|","|":" {
    printf("Punctuation: %s\n", yytext);
}

"+"|"-"|"*"|"/"|"%"|"++"|"--"|"=="|"!="|">"|"<"|">="|"<="|"&&"|"||"|"!"|"&"|"|"|"^"|"~"|"<<"|">>"|"="|"+="|"-="|"*="|"/="|"%="|"&="|"|="|"^="|"<<="|">>=" {
    printf("Operator: %s\n", yytext);
}

{INVALID_ID} {
    add_error(yytext, line_no);
    printf("Error: Invalid identifier '%s' at line %d\n", yytext, line_no);
}

. {
    add_error(yytext, line_no);
    printf("Error: Unrecognized character '%s' at line %d\n", yytext, line_no);
}

%%

int yywrap() {
    return 1;
}

int main(int argc, char **argv) {
    FILE *file;
    int i;
    
    if (argc < 2) {
        printf("Usage: %s <input_file>\n", argv[0]);
        return 1;
    }
    
    file = fopen(argv[1], "r");
    if (!file) {
        printf("Could not open %s\n", argv[1]);
        return 1;
    }
    
    yyin = file;
    
    printf("TOKENS\n");
    yylex();
    
    printf("\nLEXICAL ERRORS\n");
    if (error_count == 0) {
        printf("No lexical errors detected.\n");
    } else {
        for (i = 0; i < error_count; i++) {
            printf("Line %d : %s invalid lexeme\n", errors[i].line, errors[i].lexeme);
        }
    }
    
    printf("\nSYMBOL TABLE ENTRIES\n");
    for (i = 0; i < symbol_count; i++) {
        printf("%d) %s\n", i+1, symbol_table[i].name);
    }
    
    fclose(file);
    return 0;
}
