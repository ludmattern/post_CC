global main
extern printf

section .data
    fmt db "%s", 0

    source db \
"global main",10,\
"extern printf",10,10,\
"section .data",10,\
"    fmt db \"%s\", 0",10,10,\
"    source db \\",10,\
"PLACEHOLDER",10,\
"section .text",10,\
"main:",10,\
"    lea rdi, [rel fmt]",10,\
"    lea rsi, [rel source]",10,\
"    xor eax, eax",10,\
"    call printf",10,\
"    mov eax, 0",10,\
"    ret",10,0

section .text
main:
    lea rdi, [rel fmt]       ; format string "%s"
    lea rsi, [rel source]    ; address of the quoted source
    xor eax, eax             ; rax = 0 for printf (variadic)
    call printf

    mov eax, 0
    ret
