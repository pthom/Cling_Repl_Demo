
#pragma cling add_include_path("../../external/type_name/src/include")
#include <type_name/type_name_clean.hpp>

#include <ostream>
#include <ios>
#include <string>
#include <vector>
#include <map>

struct type_names
{
    std::string type_full;
    std::string type_clean;
};

std::ostream & operator<<(std::ostream & os, const type_names & t) {
    os << "Full : " << t.type_full << "\n" << "Clean: " << t.type_clean << std::endl;
    return os;
}

template<typename T> type_names Typename_DefaultConstructibleType()
{
    const T v;
    type_names result;
    result.type_full = var_type_name_full(v);
    result.type_clean = type_name::demangle_typename(result.type_full);
    return result;
}
