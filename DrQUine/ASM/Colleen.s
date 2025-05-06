; Quine Colleen for Dr_Quine project in NASM x86_64 assembly
global _start

section .data
quine_data:
    db "; Quine Colleen for Dr_Quine project in NASM x86_64 assembly",10
    db 0
quine_length equ $ - quine_data

section .text
_start:
    mov     rax, 1
    mov     rdi, 1
    lea     rsi, [rel quine_data]
    mov     rdx, quine_length
    syscall
    mov     rax, 60
    xor     rdi, rdi
    syscall