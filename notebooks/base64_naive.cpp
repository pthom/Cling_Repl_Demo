#include <string>

static const std::string base64_chars =
"ABCDEFGHIJKLMNOPQRSTUVWXYZ"
"abcdefghijklmnopqrstuvwxyz"
"0123456789+/";

std::string base64_encode(unsigned char const* bytes_to_encode, unsigned int in_len)
{
	std::string ret;

	int i = 0;
	int j = 0;
	unsigned char char_array_3[3];
	unsigned char char_array_4[4];

	while (in_len--) {

		char_array_3[i++] = *(bytes_to_encode++);
		if (i == 3) {

			char_array_4[0] = (char_array_3[0] & 0xfc) >> 2;
			char_array_4[1] = ((char_array_3[0] & 0x03) << 4) + ((char_array_3[1] & 0xf0) >> 4);
			char_array_4[2] = ((char_array_3[1] & 0x0f) << 2) + ((char_array_3[2] & 0xc0) >> 6);
			char_array_4[3] = char_array_3[2] & 0x3f;

			for (i = 0; (i <4); i++) {
				ret += base64_chars[char_array_4[i]];
			}
			i = 0;
		}
	}

	if (i) {
		for (j = i; j < 3; j++) {

			char_array_3[j] = '\0';
		}
		char_array_4[0] = (char_array_3[0] & 0xfc) >> 2;
		char_array_4[1] = ((char_array_3[0] & 0x03) << 4) + ((char_array_3[1] & 0xf0) >> 4);
		char_array_4[2] = ((char_array_3[1] & 0x0f) << 2) + ((char_array_3[2] & 0xc0) >> 6);
		char_array_4[3] = char_array_3[2] & 0x3f;

		for (j = 0; (j < i + 1); j++) {

			ret += base64_chars[char_array_4[j]];
		}
		while ((i++ < 3)) {

			ret += '=';
		}
	}
	return ret;
}




/////// Test code below

#include <chrono>
#include <vector>
#include <fstream>
#include <iostream>



// takes a void function (or lambda), executes it
// and return its execution time in ms
template<typename Fn> double benchmark_function(Fn f, int nb_runs)
{
    typedef std::chrono::high_resolution_clock clock;
    typedef std::chrono::duration<double, std::ratio<1>> second;
    std::chrono::time_point<clock> beg_ = clock::now();

    for(int i = 0; i < nb_runs; i++)
      f();

    return std::chrono::duration_cast<second>
        (clock::now() - beg_).count() / static_cast<double>(nb_runs) * 1000.;
}


std::vector<unsigned char> read_binary_file(const char *file)
{
    std::ifstream ifd(file, std::ios::binary | std::ios::ate);
    auto size = ifd.tellg();
    ifd.seekg(0, std::ios::beg);
    std::vector<char> buffer;
    buffer.resize(size); // << resize not reserve
    ifd.read(buffer.data(), size);

    std::vector<unsigned char> r;
    for(auto c: buffer)
        r.push_back( static_cast<unsigned char>(c) );
    return r;
}


#ifndef NO_MAIN
int main()
{
	auto buf = read_binary_file("data/lena.png");

  auto naive_base64_encode = [&]() {
    base64_encode(buf.data(), buf.size());
  };

  std::cout << "naive_base64_encode : "
    << benchmark_function(naive_base64_encode, 100) << "ms"
    << std::endl;
}
#endif
