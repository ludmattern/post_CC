; This comment is outside of any function

global main
extern printf

section .data
fmt db "; This comment is outside of any function%1$c%1$cglobal main%1$cextern printf%1$c%1$csection .data%1$cfmt db %2$c%3$s%2$c, 0%1$c%1$csection .text%1$c%1$cprint_colleen:%1$c	push rbp%1$c	mov rdi, fmt%1$c	mov rsi, 10%1$c	mov rdx, 34%1$c	mov rcx, fmt%1$c	call printf%1$c	pop rbp%1$c	ret%1$c%1$cmain:%1$c	push rbp%1$c	; inside main comment%1$c	call print_colleen%1$c	pop rbp%1$c	xor eax, eax%1$c	ret%1$c", 0

section .text

print_colleen:
	push rbp
	mov rdi, fmt
	mov rsi, 10
	mov rdx, 34
	mov rcx, fmt
	call printf
	pop rbp
	ret

main:
	push rbp
	; inside main comment
	call print_colleen
	pop rbp
	xor eax, eax
	ret
