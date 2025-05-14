; This is a self-replicating program with a counter

section .data
self: db "; This is a self-replicating program with a counter%1$c%1$csection .data%1$cself: db %2$c%3$s%2$c,0%1$cfname: db %2$cSully_%%d.s%2$c,0%1$ccompile: db %2$cnasm -f elf64 Sully_%%1$d.s -o Sully_%%1$d.o && gcc -no-pie Sully_%%1$d.o -o Sully_%%1$d%2$c,0%1$crun: db %2$c./Sully_%%1$d%2$c,0%1$cfilepath: times 100 db 0%1$cfname_buf: times 100 db 0%1$crun_buf: times 100 db 0%1$ccomp_buf: times 100 db 0%1$cSRC_FILE db __FILE__, 0%1$c%1$csection .text%1$cglobal main%1$cextern dprintf%1$cextern sprintf%1$cextern system%1$cextern strcmp%1$c%1$cmain:%1$c	push rbp%1$c	mov rbp, rsp%1$c%1$c	mov r12, %4$d%1$c%1$c	lea rdi, [rel filepath]%1$c	lea rsi, [rel fname]%1$c	mov rdx, r12%1$c	call sprintf%1$c%1$c	lea rdi, [rel filepath]%1$c	lea rsi, [rel SRC_FILE]%1$c	call strcmp%1$c	test rax, rax%1$c	jnz .create%1$c	dec r12%1$c%1$c.create:%1$c	lea rdi, [rel fname_buf]%1$c	lea rsi, [rel fname]%1$c	mov rdx, r12%1$c	call sprintf%1$c%1$c	mov rax, 2%1$c	lea rdi, [rel fname_buf]%1$c	mov rsi, 0x241%1$c	mov rdx, 0644o%1$c	syscall%1$c	cmp rax, 0%1$c	jl .exit%1$c%1$c	mov r13, rax%1$c	mov rdi, rax%1$c	lea rsi, [rel self]%1$c	mov rdx, 10%1$c	mov rcx, 34%1$c	lea r8, [rel self]%1$c	mov r9, r12%1$c	call dprintf%1$c%1$c	mov rax, 3%1$c	mov rdi, r13%1$c	syscall%1$c%1$c	lea rdi, [rel comp_buf]%1$c	lea rsi, [rel compile]%1$c	mov rdx, r12%1$c	call sprintf%1$c	lea rdi, [rel comp_buf]%1$c	call system%1$c%1$c	cmp r12, 0%1$c	jle .exit%1$c%1$c	lea rdi, [rel run_buf]%1$c	lea rsi, [rel run]%1$c	mov rdx, r12%1$c	call sprintf%1$c	lea rdi, [rel run_buf]%1$c	call system%1$c%1$c.exit:%1$c	leave%1$c	ret%1$c",0
fname: db "Sully_%d.s",0
compile: db "nasm -f elf64 Sully_%1$d.s -o Sully_%1$d.o && gcc -no-pie Sully_%1$d.o -o Sully_%1$d",0
run: db "./Sully_%1$d",0
filepath: times 100 db 0
fname_buf: times 100 db 0
run_buf: times 100 db 0
comp_buf: times 100 db 0
SRC_FILE db __FILE__, 0

section .text
global main
extern dprintf
extern sprintf
extern system
extern strcmp

main:
	push rbp
	mov rbp, rsp

	mov r12, 5

	lea rdi, [rel filepath]
	lea rsi, [rel fname]
	mov rdx, r12
	call sprintf

	lea rdi, [rel filepath]
	lea rsi, [rel SRC_FILE]
	call strcmp
	test rax, rax
	jnz .create
	dec r12

.create:
	lea rdi, [rel fname_buf]
	lea rsi, [rel fname]
	mov rdx, r12
	call sprintf

	; Check if counter is negative
	cmp r12, 0
	jl .exit

	mov rax, 2
	lea rdi, [rel fname_buf]
	mov rsi, 0x241
	mov rdx, 0644o
	syscall
	cmp rax, 0
	jl .exit

	mov r13, rax
	mov rdi, rax
	lea rsi, [rel self]
	mov rdx, 10
	mov rcx, 34
	lea r8, [rel self]
	mov r9, r12
	call dprintf

	mov rax, 3
	mov rdi, r13
	syscall

	lea rdi, [rel comp_buf]
	lea rsi, [rel compile]
	mov rdx, r12
	call sprintf
	lea rdi, [rel comp_buf]
	call system

	cmp r12, 0
	jle .exit

	lea rdi, [rel run_buf]
	lea rsi, [rel run]
	mov rdx, r12
	call sprintf
	lea rdi, [rel run_buf]
	call system

.exit:
	leave
	ret