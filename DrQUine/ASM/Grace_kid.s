; This program will print its own source in a file named Grace_kid.s

%define STRING "; This program will print its own source in a file named Grace_kid.s%3$c%3$c%%define STRING %4$c%1$s%4$c%3$c%%define CHILD %4$cGrace_kid.s%4$c%3$c%3$csection .data%3$cfile_name:%3$c%2$cdb CHILD, 0%3$cfile_content:%3$c%2$cdb STRING, 0%3$c%3$csection .text%3$c%2$cglobal main%3$c%2$cextern dprintf%3$c%3$c%%macro start 0%3$cglobal main%3$c%3$cmain:%3$c%2$cpush rbp%3$c%2$cmov rbp, rsp%3$c%2$clea rdi, [rel file_name]%3$c%2$cmov rax, 2%3$c%2$cmov rdx, 0644o%3$c%2$cmov rsi, 0x241%3$c%2$csyscall%3$c%3$c%2$cmov rdi, rax%3$c%2$clea rsi, [rel file_content]%3$c%2$clea rdx, [rel file_content]%3$c%2$cmov rcx, 9%3$c%2$cmov r8, 10%3$c%2$cmov r9, 34%3$c%2$ccall dprintf%3$c%2$cmov rsp, rbp%3$c%2$cpop rbp%3$c%2$cxor eax, eax%3$c%2$cret%3$c%3$c%%endmacro%3$c%3$cstart"
%define CHILD "Grace_kid.s"

section .data
file_name:
	db CHILD, 0
file_content:
	db STRING, 0

section .text
	global main
	extern dprintf

%macro start 0
global main

main:
	push rbp
	mov rbp, rsp
	lea rdi, [rel file_name]
	mov rax, 2
	mov rdx, 0644o
	mov rsi, 0x241
	syscall

	mov rdi, rax
	lea rsi, [rel file_content]
	lea rdx, [rel file_content]
	mov rcx, 9
	mov r8, 10
	mov r9, 34
	call dprintf
	mov rsp, rbp
	pop rbp
	xor eax, eax
	ret

%endmacro

start