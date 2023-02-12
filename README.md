# simplecompiler
A simple compiler written in python
(https://echozulu.hashnode.dev/creating-my-own-compiler-part-1)

## Goal
A basic compiler for data models in a protobuf-like way, but not for messages.
The resulting output files could be used for internal database and/or adapters to industrial protocols, for example.

## Overview
A basic compiler has the following parts:
- Lexer converts the input source file into tokens.
- Parser performs syntax analysis converting tokens into an abstract syntax tree
- Emitter generate the target code (e.g. assembly, other high-level-languages, databases, etc.)
