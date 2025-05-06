global ft_read
extern __errno_location

%define SYS_read 0

section .text

; ssize_t ft_read(int fd, void *buf, size_t count)
; Arguments:
;   rdi → fd
;   rsi → buf
;   rdx → count
; Return:
;   rax → number of bytes read, or -1 on error

ft_read:
    mov     rax, SYS_read          ; syscall number for read
    syscall                        ; perform read(fd, buf, count)

    cmp     rax, 0
    jge     .done                  ; success

    neg     rax                    ; rax = positive errno
    mov     r10d, eax              ; store errno in temp reg

    call    __errno_location wrt ..plt          ; get &errno
    mov     [rax], r10d            ; set errno
    mov     rax, -1                ; return -1 on failure

.done:
    ret
