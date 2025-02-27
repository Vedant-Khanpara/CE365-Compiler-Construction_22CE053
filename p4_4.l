%{
    #include <stdio.h>
    #include <string.h>
    
    int d = 0, l = 0, lc = 0, uc = 0, ss = 0, ec = 0;
%}

%%

[0-9]       { d++; l++; } 
[a-z]       { lc++; l++; } 
[A-Z]       { uc++; l++; } 
[*;,#$@]    { ss++; l++; } 
\n          { 
                if(d > 0 && lc > 0 && uc > 0 && ss > 0 && l >= 9 && l <= 15 && ec == 0) 
                    printf("Valid\n"); 
                else 
                    printf("Invalid\n");
                d = l = lc = uc = ss = ec = 0;  
            }
.           { ec++; } 

%%

int yywrap() { return 1; } 

int main() {
    char input[100];
    
    printf("Enter a Password: ");
    fgets(input, sizeof(input), stdin); 
    
    yy_scan_string(input);  
    yylex();  
    
    return 0;
}