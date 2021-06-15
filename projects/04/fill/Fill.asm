// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/04/Fill.asm

// Runs an infinite loop that listens to the keyboard input.
// When a key is pressed (any key), the program blackens the screen,
// i.e. writes "black" in every pixel;
// the screen should remain fully black as long as the key is pressed.
// When no key is pressed, the program clears the screen, i.e. writes
// "white" in every pixel;
// the screen should remain fully clear as long as no key is pressed.

(LOOP)
    @KBD
    D=M
    @ON
    D;JGT
    @0
    M=0
    @FILL
    D;JEQ

(ON)
    @0
    M=-1

(FILL)
    @SCREEN
    D=A
    @8191
    D=D+A
    @1
    M=D

    (FILLLOOP)
        @0
        D=M

        @1
        A=M
        M=D

        @1
        MD=M-1

        @SCREEN
        D=D-A
        @FILLLOOP
        D;JGE

@LOOP
D;JMP
