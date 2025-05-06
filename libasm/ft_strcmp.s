global ft_strcmp
section .text

; int ft_strcmp(const char *s1, const char *s2)
; Arguments:
;   rdi → pointer to s1
;   rsi → pointer to s2
; Returns (in EAX):
;   < 0 if s1 < s2
;   = 0 if s1 == s2
;   > 0 if s1 > s2

ft_strcmp:
    ; Check for NULL pointers
    test    rdi, rdi
    jnz     .check_s2
    test    rsi, rsi
    jnz     .s1_null
    xor     eax, eax              ; both NULL → return 0
    ret

.s1_null:
    mov     eax, -1               ; s1 NULL < s2
    ret

.check_s2:
    test    rsi, rsi
    jnz     .loop                 ; both non-NULL → proceed
    mov     eax, 1                ; s1 > NULL
    ret

; Main loop: compare 8 bytes at a time
.loop:
    mov     rax, [rdi]            ; load 8 bytes from s1
    mov     rcx, [rsi]            ; load 8 bytes from s2
    cmp     rax, rcx
    jne     .diff_block

    ; check for null byte in block
    mov     rdx, rax
    mov     r8,  0x0101010101010101
    mov     r9,  0x8080808080808080
    sub     rdx, r8
    not     rax
    and     rdx, rax
    and     rdx, r9
    jnz     .equal

    add     rdi, 8
    add     rsi, 8
    jmp     .loop

.diff_block:
.byte_cmp:
    mov     al, [rdi]
    mov     cl, [rsi]
    cmp     al, cl
    jne     .return_diff
    test    al, al
    jz      .equal
    inc     rdi
    inc     rsi
    jmp     .byte_cmp

.return_diff:
    movzx   eax, al
    movzx   ecx, cl
    sub     eax, ecx
    ret

.equal:
    xor     eax, eax
    ret
