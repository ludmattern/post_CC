global ft_strdup
extern ft_strlen
extern ft_strcpy
extern malloc

section .text

; char *ft_strdup(const char *s)
; rdi → input string
; return rax → duplicated string or NULL

ft_strdup:
    test    rdi, rdi        ; if s == NULL
    je      .null           ;   return NULL

    push    rdi             ; save s for later
    call    ft_strlen       ; rax = strlen(s)
    inc     rax             ; rax = length + 1
    mov     rdi, rax        ; argument for malloc
    call    malloc wrt ..plt
    pop     rsi             ; restore s

    test    rax, rax        ; if malloc returned NULL
    je      .null           ;   return NULL

    mov     rdi, rax        ; dest = malloc’d buffer
    call    ft_strcpy       ; strcpy(dest, s)
    ret

.null:
    xor     rax, rax        ; rax = NULL
    ret
