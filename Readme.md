# Using fplus in a functional REPL via cling

# About cling

> Cling is an interactive C++ interpreter, built on top of Clang and LLVM compiler infrastructure. Cling realizes the read-eval-print loop (REPL) concept, in order to leverage rapid application development. Implemented as a small extension to LLVM and Clang, the interpreter reuses their strengths such as the praised concise and expressive compiler diagnostics.

It is based on the Root data analysis framework, and originates from the CERN.

See https://github.com/root-project/cling and https://cdn.rawgit.com/root-project/cling/master/www/index.html

cling is a mix of `clang` + REPL. Thus, it accepts the standard clang argument (`-L`, `--std=c++14`, `-I`, etc)

cling is stil under heavy development and might fail (for example a segfault in your program will exit cling REPL). However it is quite usable, and used everydauy at the CERN.

# Advices and Gotchas



# Interactive session examples

## In a shell / console only

See the interactive session example and avdvices at [examples/shell_cling/Readme.md](examples/shell_cling/Readme.md).

## In jupyter notebook

See the interactive session example and avdvices at [examples/shell_cling/Readme.md](examples/shell_cling/Readme.md).

## In a shell, displaying image via opencv


# Installation

## No installation (!) : Test it online on mybinder.org
Head on to http://mybinder.org/

## Docker : quick test without modifying your machine

If you do not want to install cling on your machine, or if you are not running under linux, you can use the docker image provided inside `Docker_xeus`.

Refer to [Docker_xeus/Readme.md](Docker_xeus/Readme.md).

## Linux
Nightly build are available here: https://root.cern.ch/download/cling/
Download them and add to your path.

## Mac
````bash
brew install cling
````
