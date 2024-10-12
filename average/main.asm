%macro pushd 0
   push rax
   push rbx
   push rcx
   push rdx
%endmacro

%macro popd 0
   pop rdx
   pop rcx
   pop rbx
   pop rax
%endmacro

%macro print 2
   pushd
   mov rax, 1
   mov rdi, 1
   mov rsi, %1
   mov rdx, %2
   syscall
   popd
%endmacro

%macro dprint 0
   pushd
   mov rbx, 0
   mov rcx, 10
   %%divide:
       xor rdx, rdx
       div rcx
       print result, 1

       push rdx
       inc rbx
       cmp rax, 0
       jne %%divide

   %%digit:
       pop rax
       add rax, '0'
       mov [result], rax
       print result, 1
       dec rbx
       cmp rbx, 0
       jg %%digit
   popd
%endmacro


section .text
global _start

_start:
    mov ecx, len_x
    xor eax, eax
    xor ebx, ebx

sum_x_loop:
    add al, [x + ebx]
    inc ebx
    loop sum_x_loop

    mov ecx, len_y
    xor ebx, ebx
    xor edx, edx

sum_y_loop:
    add dl, [y + ebx]
    inc ebx
    loop sum_y_loop

    cmp al, dl
    jg al_greater

    mov byte [minus], '-'
    print minus, 1
    sub dl, al
    mov [diff], dl

    jmp calculate_mean

al_greater:
    sub al, dl
    mov [diff], al

calculate_mean:
    mov ecx, len_x
    xor ebx, ebx
    mov bl, len_x
    xor edx, edx
    mov al, [diff]
    idiv bl
    mov [mean], al

    mov rax, [mean]
    dprint
    print newline, nlen

    mov eax, 1
    xor ebx, ebx 
    int 0x80

section .data
    x db 5, 3, 2, 6, 1, 7, 4
    y db 0, 10, 1, 9, 2, 8, 5
    len_x equ 7
    len_y equ 7
    sum_x db 0
    sum_y db 0
    diff db 0
    mean db 0

    result dq 0
    newline db 0xA, 0xD 
    nlen equ $ - newline

section .bss
    minus resb 1
