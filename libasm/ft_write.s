global ft_write
extern __errno_location

%define SYS_write 1

section .text

; ssize_t ft_write(int fd, const void *buf, size_t count)
; Arguments:
;   rdi → fd
;   rsi → buf
;   rdx → count
; Return:
;   rax → number of bytes written, or -1 on error

ft_write:
    mov     rax, SYS_write         ; syscall number for write
    syscall                        ; perform write(fd, buf, count)

    cmp     rax, 0
    jge     .done                  ; if result ≥ 0 → success

    ; Error: syscall returned -errno
    neg     rax                    ; rax = errno (positive)
    mov     r10d, eax              ; save errno (32-bit) in caller-saved register

    call    __errno_location wrt ..plt         ; rax = pointer to errno
    mov     [rax], r10d            ; *errno = saved errno
    mov     rax, -1                ; return -1 to caller

.done:
    ret
