# Read-Eval-Print-Loop in C++ with cling and jupyter notebook / tutorial and advices

## About cling

> [Cling](https://github.com/root-project/cling) is an interactive C++ interpreter, built on top of Clang and LLVM compiler infrastructure. Cling realizes the read-eval-print loop (REPL) concept, in order to leverage rapid application development. Implemented as a small extension to LLVM and Clang, the interpreter reuses their strengths such as the praised concise and expressive compiler diagnostics.

It is based on the Root data analysis framework, and originates from the CERN. Cling is stil under heavy development and might fail (for example a segfault in your program will exit cling REPL). However it is quite useful, and used everyday at the CERN.

## About xeus cling

[Xeus cling](https://github.com/QuantStack/xeus-cling) is a Jupyter kernel for the C++ programming language based on cling.

Read the docs [here](https://xeus-cling.readthedocs.io/en/latest/).

## Advices and Gotchas

The cling and xeus docs are good, but some informations are missing : see the page ["Advices and Gotchas when using cling and jupyter"](examples/notebooks/Advices_And_Gotchas.ipynb) for more details.
