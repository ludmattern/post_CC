global main
extern printf

section .data
s db "global main%1$cextern printf%1$c%1$csection .data%1$cs db %2$c%3$s%2$c,0%1$c%1$csection .text%1$cmain:%1$c    push rbp%1$c    mov rdi,s%1$c    mov rsi,10%1$c    mov rdx,34%1$c    mov rcx,s%1$c    xor eax,eax%1$c    call printf%1$c    pop rbp%1$c    xor eax,eax%1$c    ret%1$c",0

section .text
main:
    push rbp
    mov rdi,s
    mov rsi,10
    mov rdx,34
    mov rcx,s
    xor eax,eax
    call printf
    pop rbp
    xor eax,eax
    ret