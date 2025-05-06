global ft_strcpy
section .text

; char *ft_strcpy(char *dst, const char *src)
; rdi = dest, rsi = src
; return rax = original dest pointer

ft_strcpy:
    test    rdi, rdi
    jz      .null_return

    test    rsi, rsi
    jz      .null_return

    mov     rax, rdi                ; Save return pointer (original dst)

.next_byte:
    mov     dl, [rsi]               ; Load byte from src
    mov     [rdi], dl               ; Store byte to dst
    inc     rsi
    inc     rdi
    test    dl, dl                  ; Was it '\0'?
    jnz     .next_byte              ; If not, keep copying
    ret

.null_return:
    xor     rax, rax
    ret
