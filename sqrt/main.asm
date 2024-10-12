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
    mov rax, [num]
    shr rax, 1
    mov [x1], rax

    mov rax, [num]
    mov rbx, [x1]
    xor rdx, rdx
    div rbx
    add rax, [x1]
    shr rax, 1
    mov [x2], rax

while_loop:
    mov rax, [x1]
    sub rax, [x2]
    cmp rax, 1
    jl end_while

    mov rax, [x2]
    mov [x1], rax

    mov rax, [num]
    mov rbx, [x1]
    xor rdx, rdx
    div rbx
    add rax, [x1]
    shr rax, 1
    mov [x2], rax

    jmp while_loop

end_while:
    mov rax, [x2]

    dprint
    print newline, nlen

    mov rax, 60
    xor rdi, rdi
    syscall

section .data
    num dq 144
    result dq 0
    newline db 0xA, 0xD
    nlen equ $ - newline

section .bss
    x1 resq 1
    x2 resq 1
