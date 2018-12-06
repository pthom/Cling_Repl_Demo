[![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/pthom/Cling_Repl_Demo/master?filepath=examples%2Fnotebooks%2F)

# Read-Eval-Print-Loop in C++ with cling and jupyter notebook / tutorial and advices

## About cling

> [Cling](https://github.com/root-project/cling) is an interactive C++ interpreter, built on top of Clang and LLVM compiler infrastructure. Cling realizes the read-eval-print loop (REPL) concept, in order to leverage rapid application development. Implemented as a small extension to LLVM and Clang, the interpreter reuses their strengths such as the praised concise and expressive compiler diagnostics.

It is based on the Root data analysis framework, and originates from the CERN. Cling is stil under heavy development and might fail (for example a segfault in your program will exit cling REPL). However it is quite useful, and used everyday at the CERN.

## About xeus cling

[Xeus cling](https://github.com/QuantStack/xeus-cling) is a Jupyter kernel for the C++ programming language based on cling.

Read the docs [here](https://xeus-cling.readthedocs.io/en/latest/).

## Advices and Gotchas

The cling and xeus docs are good, but some informations are missing : see the page ["Advices and Gotchas when using cling and jupyter"](examples/notebooks/Advices_And_Gotchas.ipynb) for more details.


----------------

# Interactive C++ REPL session examples

## Interactive C++ REPL session from the console
See the interactive session example and advices here :

[examples/shell_cling/Shell_Functional_REPL.md](examples/shell_cling/Shell_Functional_REPL.md).

## Interactive C++ REPL session inside jupyter notebook

### Intro to jupyter notebook

If you do not know jupyter notebook, take some time to familiarize yourself with the concept here:
* [Official site](http://jupyter.org/)
* [Try in online on the official site](http://jupyter.org/try)
* [Quick introduction to Jupyter Notebook](https://www.youtube.com/watch?v=jZ952vChhuI) (youtube video, 7')

### A session of REPL / C++ with opencv

This demo shows how to load a library (opencv), and how to display images inside jupyter notebook.

Demo links:
* [Online / Read only](examples/notebooks/opencv_example.ipynb)  (will open immediately)
* <a href="https://mybinder.org/v2/gh/pthom/Cling_Repl_Demo/blob/master/examples/notebooks/opencv_example.ipynb/master" target="_blank">Online / runnable REPL</a>  (Requires 1 minute to load : it is recommended to open this link in a separate tab)
* [From you local clone of this repo](http://localhost:8888/tree/examples/notebooks/opencv_example.ipynb) (if you launched jupyter notebook on your computer or on the [docker container](Docker_xeus/Readme.md))

### A session of C++ showing functional programming with REPL

This demo shows an example of a session functional programming in C++ using a Read-Eval-Print-Loop (REPL).
This mode of development is very adapted to functional programming.

Below is an example, using [FunctionalPlus](https://github.com/Dobiasd/FunctionalPlus) (a functional programming library for C++).
FunctionalPlus provides an [API search engine](http://www.editgym.com/fplus-api-search/), similar to haskell's [hoogle](https://www.haskell.org/hoogle/).

Demo links:
* [Online / Read only](examples/notebooks/Functional_REPL.ipynb)  (will open immediately)
* <a href="https://mybinder.org/v2/gh/pthom/Cling_Repl_Demo/blob/master/examples/notebooks/Functional_REPL.ipynb/master" target="_blank">Online / runnable REPL</a>  (Requires 1 minute to load : it is recommended to open this link in a separate tab)
* [From you local clone of this repo](http://localhost:8888/tree/examples/notebooks/Functional_REPL.ipynb) (if you launched jupyter notebook on your computer or on the [docker container](Docker_xeus/Readme.md))


# Installation : how to test these examples on your computer

## Docker : quick test without modifying your machine
If you do not want to modify your machine, you can use the docker image provided inside `Docker_xeus`.

Refer to [Docker_xeus/Readme.md](Docker_xeus/Readme.md).

## Full installation on your machine
Refer to the instructions on the [xeus cling web page](https://github.com/QuantStack/xeus-cling)

## I don't want to install anything!

As mentioned before, these demos are [available online on mybinder.org](https://mybinder.org/v2/gh/pthom/Cling_Repl_Demo/master?filepath=examples%2Fnotebooks%2F)

[![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/pthom/Cling_Repl_Demo/master?filepath=examples%2Fnotebooks%2F)
