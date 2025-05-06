global ft_strlen
section .text

; size_t ft_strlen(const char *s)
;  - arg1 in RDI
;  - return value in RAX

ft_strlen:
    test    rdi, rdi
    jz      .zero               ; if s == NULL → return 0

    mov     rcx, rdi            ; save the starting address of the string

    ; load 64-bit constants into registers
    mov     r8,  0x0101010101010101   ; mask for subtraction
    mov     r9,  0x8080808080808080   ; mask to isolate high bits

.loop:
    mov     rax, [rdi]          ; load 8 bytes from the string
    mov     rdx, rax            ; copy for later bit manipulation

    sub     rax, r8             ; subtract 1 from each byte
    not     rdx                 ; invert original bytes
    and     rax, rdx            ; combine results to detect 0 bytes
    and     rax, r9             ; isolate high bits to detect '\0'
    jnz     .found              ; if any high bit is set → found '\0'

    add     rdi, 8              ; no '\0' in this block → move forward
    jmp     .loop

.found:
    bsf     rdx, rax            ; find first set bit (bit index)
    shr     rdx, 3              ; convert to byte index (divide by 8)
    lea     rax, [rdi + rdx]    ; address of the null terminator
    sub     rax, rcx            ; length = (end - start)
    ret

.zero:
    xor     rax, rax            ; return 0
    ret
