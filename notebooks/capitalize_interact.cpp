#include <fplus/fplus.hpp>

std::string capitalize_first_letter(const std::string & word) {
    auto result = fplus::to_lower_case(word);
    result[0] = toupper(result[0]);
    return result;
}

int main()
{
  auto apply_by_words = [](auto f) {
    return fplus::fwd::compose(
        fplus::fwd::split(' ', false),
        fplus::fwd::transform(f),
        fplus::fwd::join(std::string(" "))
    );
   };
  auto apply_by_lines = [](auto f) {
      return fplus::fwd::compose(
          fplus::fwd::split_lines(false),
          fplus::fwd::transform(f),
          fplus::fwd::join(std::string("\n"))
      );
  };

  auto cap_words = apply_by_words(capitalize_first_letter);
  auto cap_text = apply_by_lines(cap_words);
  auto prog = fplus::interact(cap_text);

  prog();
}