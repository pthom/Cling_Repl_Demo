# Using fplus in a functional REPL via cling

mybinder.org !!!

# About cling

> Cling is an interactive C++ interpreter, built on top of Clang and LLVM compiler infrastructure. Cling realizes the read-eval-print loop (REPL) concept, in order to leverage rapid application development. Implemented as a small extension to LLVM and Clang, the interpreter reuses their strengths such as the praised concise and expressive compiler diagnostics.

It is based on the Root data analysis framework, and originates from the CERN.

See https://github.com/root-project/cling and https://cdn.rawgit.com/root-project/cling/master/www/index.html

cling is a mix of `clang` + REPL. Thus, it accepts the standard clang argument (`-L`, `--std=c++14`, `-I`, etc)

cling is stil under heavy development and might fail (for example a segfault in your program will exit cling REPL). However it is quite usable, and used everydauy at the CERN.


# Installation

## Linux

Nightly build are available here: https://root.cern.ch/download/cling/

Download them and add to your path.

## Mac

````bash
brew install cling
````

# Interactive session example

If you are using cling in the provided Docker container, see [Docker_cling/Readme.md](Docker_cling/Readme.md).

Launch `cling` with C++14 support (required by fplus).

````bash
cling --std=c++14
````

Then, enter these command one by in the cling interpreter (the first line will load the file [init.cpp](init.cpp))

````cpp

// this will load the file init.cpp :
// - set some include and library paths
// - load opencv libraries
// - include opencv main files
// - include fplus
.L init.cpp

// this will load an image, and show it immediately
cv::Mat lena = cv::imread("lena.jpg");
cv::imshow("lena", lena); cv::waitKey(100);

// let's try some image manipulation
cv::Mat blur;
cv::blur(lena, blur, cv::Size(15, 15));
cv::imshow("blur", blur); cv::waitKey(100);


//
// Now, onto some functional REPL
//

// Plutot s'inspirer de /dvp/Katas/snake_cpp/src/main/count_words.cpp

// If you do not end your line with a ";", cling will output the result
// of the last computation
fplus::read_text_file("if.txt") // no ";"
// Oops:
// --> input_line_8:1:76: error: no template named 'basic_string'; did you mean 'std::basic_string'?
//    extern "C" void __cling_Destruct_0x7fee164382c0(void* obj){((std::function<basic_string<char> ()>*)obj)->~function();}
//
// There is an error inside cling: it require to add "using namespace std;"

// Let add it and try again
using namespace std;
fplus::read_text_file("if.txt") // no ";"
//-> (std::function<std::string ()>) @0x8ed4050

// Ha, ha ! fplus::read_text_file did not return a string !
// It would have taken me quite a while to figure this out
// during a normal C++ coding session. Here, I can avoid the error immediately .
//
// The reason for this is that fplus is a functional library,
// so that fplus::read_text_file(filename) does not perform the side effect :
// instead it returns a function which you need to invoke
// in order to perform the side effect.
auto poem = fplus::read_text_file("if.txt")();

poem
// -> (std::basic_string<char, std::char_traits<char>, std::allocator<char> > &)
//"If you can keep your head when all about you
// Are losing theirs and blaming it on you,
//If you can trust yourself when all men doubt you,
//...


// Let's try to split some lines
const auto lines = fplus::split_lines(poem, false);
// input_line_5:2:21: error: no matching function for call to 'split_lines'
//  const auto lines = fplus::split_lines(input, false);
//                     ^~~~~~~~~~~~~~~~~~
// fplus_include/fplus/string_tools.hpp:74:14: note: candidate function not viable:
// no known conversion from 'std::string' (aka 'basic_string<char, char_traits<char>,
// allocator<char> >') to 'bool' for 1st argument
// ContainerOut split_lines(bool allowEmpty, const String& str)

// ooops, I was wrong in the argument order; but I got an immediate feedback
// (no need to wait for the compilation)
// Let's correct this:
const auto lines = fplus::split_lines(false, poem);

// Let's see those lines:
lines
// (std::vector<std::basic_string<char, std::char_traits<char>, std::allocator<char> >,
//std::allocator<std::basic_string<char, std::char_traits<char>, std::allocator<char> > > > &)
//{ "If you can keep your head when all about you", " Are losing theirs and blaming it on you,",
// etc...


// Note: inside cling, *always* put the function body opening brace
// at the end of the declaration line !
// Otherwise, you might get weird errors messages
std::string capitalize_first_letter(const std::string & word) {
    auto result = fplus::to_lower_case(word);
    result[0] = toupper(result[0]);
    return result;
}

// Let's continue :
// apply_by_words is a higher order function that will
// transform a function f into another function
// that will appply f word by word
auto apply_by_words = [](auto f) {
    return fplus::fwd::compose(
        fplus::fwd::split(' ', false),
        fplus::fwd::transform(f),
        fplus::fwd::join(std::string(" "))
    );
 };

// Now let's instantiate apply_by_words with capitalize_first_letter
auto cap_words = apply_by_words(capitalize_first_letter);
cap_words
// -> (fplus::fwd::internal::compose_helper<(lambda), fplus::fwd::internal::compose_helper<(lambda), (lambda)> > &) @0x7f674dea1018

// And let's try it
cap_words(lines[0])
// It works !
// -> (std::basic_string<char, std::char_traits<char>, std::allocator<char> >)
// "If You Can Keep Your Head When All About You"


// Let's continue
auto apply_by_lines = [](auto f) {
    return fplus::fwd::compose(
        fplus::fwd::split_lines(false),
        fplus::fwd::transform(f),
        fplus::fwd::join(std::string("\n"))
    );
 };

auto cap_text = apply_by_lines(cap_words);

// And now let's apply this to the complete poem
cap_text(poem)
// -> (std::basic_string<char, std::char_traits<char>, std::allocator<char> >)
// "If You Can Keep Your Head When All About You
// Are Losing Theirs And Blaming It On You
// If You Can Trust Yourself When All Men Doubt You
// ...
````


# Advices

## You can test this in a docker container

If you do not want to install cling on your machine, or if you are not running under linux,
you can use the docker image provided inside `repl_cling/Docker_cling_`.

Refer to [Docker_cling/Readme.md](Docker_cling/Readme.md)

## Mac OS

On Mac OS, if opencv is not installed in a standard path, you can fill `DYLD_LIBRARY_PATH`

````bash
ln -s /path/to/your/opencv/install opencv-install
export DYLD_LIBRARY_PATH=$(pwd)/opencv-install/lib  # this is MacOS specific
````

Also, use `init.mac.cpp` instead of `init.cpp`
