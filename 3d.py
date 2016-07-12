#!/usr/bin/python3.5
#coding: utf-8

import sys, codecs
from random import randint
from getch import getch as get_k

try:
    from loc import msg
except ImportError:
    msg = {'no_file': 'No such file or directory: ', 'wrong_arg':'Invalid argument: ', 'v_path': 'Path: ', 'v_grid': 'Grid: ', 'v_pos': 'Position: ', 'v_char': 'Character: ', 'v_stack': '\nStack: ', 'wrong_hex': ' is not a valid hex number\n', 'err_script': 'Error in script: ', 'quit': '\nInterruption.'}

ext = '.x3d'
f_have_ext = False
prompt = '~ '
verbose = False

########### Exceptions ##########

class Error(Exception):
    '''Error in 3D script: '''

class EndOfProgram(Exception):
    '''End Of Program: Stop'''


########### I/O Functions ##########

s_to_g = lambda s: [k.split('\n') for k in s.split('\n\n')]

def get_g(p):
    if p == '-':
        return s_to_g(sys.stdin.read())
    elif ext * int(f_have_ext) in p:
        try:
            return [k.split('\n') for k in codecs.open(p, 'r', 'utf-8').read().split('\n\n')]
        except FileNotFoundError:
            sys.stderr.write(msg['no_file'] + p)
            exit
    else:
        raise Error(msg['wrong_arg'] + p)


    

########## Instructions ##########

D = lambda n, d: [(1 - 2 * int(not bool(n))) for k in range(0, len(d))]

def ivrt(S):
    n1 = S.pop()
    n2 = S.pop()
    S.append(n1)
    S.append(n2)
    
X = lambda x, d: [sum(i) for i in zip(x, d)]

K = lambda g, x: g[x[2]][x[1]][x[0]]


########## Commands dictionary ##########

def C(k, x, d, S, a):
    if   k == '<': d = [-1, 0, 0]                                      #Move: West
    elif k == '>': d = [ 1, 0, 0]                                      #      East
    elif k == '^': d = [ 0,-1, 0]                                      #      North
    elif k == 'v': d = [ 0, 1, 0]                                      #      South
    elif k == 'x': d = [ 0, 0,-1]                                      #      Up
    elif k == 'o': d = [ 0, 0, 1]                                      #      Down
    elif k == '_': d = D(S.pop(), [1, 0, 0])                           # Deflect: N/S
    elif k == '|': d = D(S.pop(), [0, 1, 0])                           #          W/E
    elif k == '.': d = D(S.pop(), [0, 0, 1])                           #          U/D
    elif k == '?': S.append(ord(get_k()))                              #Input and push Unicode number
    elif k == ',': S.pop()                                             #Pop silently
    elif k == '!': print(chr(S.pop()), end = '')                       #Pop and output as Unicode char
    elif k == '&': S.append(S[len(S[1:])])                             #Duplicate top of the stack
    elif k == '$': S.append(S.pop(-2))                                 #Invert top 2 elements of the stack
    elif k == '+': S.append(S.pop(-2) + S.pop())                       #Operation: sum
    elif k == '-': S.append(S.pop(-2) - S.pop())                       #           difference
    elif k == '*': S.append(S.pop(-2) * S.pop())                       #           product
    elif k == '∕': S.append(S.pop(-2)// S.pop())                       #           quotient
    elif k == '%': S.append(S.pop(-2) % S.pop())                       #           remainder
    elif k == '`': S.append(S.pop(-2)** S.pop())                       #           power
    elif k == "'": a = 'k'                                             #Push next char on the grid as: character (hence Unicode-interpreted)
    elif k == '\\':a = 'n'                                             #                               hex number (not case-sensitive)
    elif k == '#': S.append(randint(0, S.pop()))                       #Replace top of the stack with a lower/equal random int
    elif k == '"': C(S.pop(), x, d, S, a)                          #Interpret top of the stack as a command character
    elif k == 'q': print('q' * int(x == [0, 0, 0]), end = ''); a = 'x' #Quine
    elif k == ';': a = 'x'                                             #End of program
    else: pass                                                         #Every other character is a NOP.


########## Initial parameters ##########

x = [0,0,0] #Initial x at (0, 0, 0) North-West-Down corner
d = [0,0,0] #Initial direction is empty.
#First character of the program must be a directional instruction, or else the pointer won't move across the grid

S = []
for o in ('-d', '-p', '-v'):
    if not verbose: verbose = o in sys.argv
    else: sys.argv.remove(o)

try:
    g = get_g(sys.argv[1])
    sys.stderr.write(msg['v_path'] + sys.argv[1] + '\n')
except IndexError:
    g = get_g('-')

if verbose: sys.stderr.write(msg['v_grid'] + repr(g) + '\n') #

a = 'i' # a is always one of (i, k, n, x)


########## Interpreter core ##########

while a != 'x':
    try:
        k = K(g, x)
        if verbose: sys.stderr.write(msg['v_pos'] + repr(x) + msg['v_char'] + repr(k)) #
        if a == 'i':
            C(k, x, d, S, a)
        elif a == 'k':
            S.append(ord(k))
        elif a == 'n':
            try:
                S.append(eval('0x' + k))
            except SyntaxError:
                sys.stderr.write(k + msg['wrong_hex'])
        else: raise ValueError(msg['err_script'] + sys.argv[0])
        x = X(x, d)
    except (KeyboardInterrupt, EOFError): print(msg['quit']); break
    else: if verbose: sys.stderr.write(msg['v_stack'] + repr(S) + '\n') #
#END
