# Example of an interactive shell session with cling

This example, uses [FunctionalPlus](https://github.com/Dobiasd/FunctionalPlus) (a functional programming library for C++).

Launch `cling` with C++14 support (required by fplus).

````bash
cling --std=c++14
````

Then, enter these command line by line in the cling interpreter:

````cpp
// If you are using this on your machine, enter this
#pragma cling add_include_path("path/to/this/repo/external/FunctionalPlus/include")
// If you are using this on the provided Docker container, enter this
#pragma cling add_include_path("/sources_docker/external/FunctionalPlus/include")
#include <fplus/fplus.hpp>

// If you do not end your line with a ";", cling will output the result
// of the last computation
fplus::read_text_file("notebooks/data/if.txt") // no ";"
// Oops:
// --> input_line_8:1:76: error: no template named 'basic_string'; did you mean 'std::basic_string'?
//    extern "C" void __cling_Destruct_0x7fee164382c0(void* obj){((std::function<basic_string<char> ()>*)obj)->~function();}
//
// There is an error inside cling: it require to add "using namespace std;"

// Let add it and try again
using namespace std;
fplus::read_text_file("notebooks/data/if.txt") // no ";"
//-> (std::function<std::string ()>) @0x8ed4050

// Ha, ha ! fplus::read_text_file did not return a string !
// It would have taken me quite a while to figure this out
// during a normal C++ coding session. Here, I can avoid the error immediately .
//
// The reason for this is that fplus is a functional library,
// so that fplus::read_text_file(filename) does not perform the side effect :
// instead it returns a function which you need to invoke
// in order to perform the side effect.
auto poem = fplus::read_text_file("notebooks/data/if.txt")();

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
