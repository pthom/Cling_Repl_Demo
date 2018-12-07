
#pragma cling add_include_path("../../external/type_name/src/include")
#pragma cling add_include_path("../../external/FunctionalPlus/include")
#include <type_name/type_name_clean.hpp>
#include <fplus/fplus.hpp>

struct extract_parenthesis_content_at_end_result
{
    std::string remaining;
    std::string parenthesis_content;
    bool success;
};

extract_parenthesis_content_at_end_result extract_parenthesis_content_at_end(const std::string & str)
{
    extract_parenthesis_content_at_end_result result;

    extract_parenthesis_content_at_end_result error; error.success = false;

    std::string s = str;

    while (s.back() != ')')
    {
        s.pop_back();
        if (s.empty())
            return error;
    }

    std::vector<char> content;
    int nb_parenthesis = 1;
    content.push_back(')');
    s.pop_back();
    while (nb_parenthesis > 0)
    {
        char c = s.back();
        content.push_back(c);
        if (c == ')')
            nb_parenthesis ++;
        if (c == '(')
            nb_parenthesis --;
        s.pop_back();
        if (s.empty())
            return error;
    }
    std::reverse(content.begin(), content.end());
    for (auto c : content)
        result.parenthesis_content += c;
    result.remaining = s;
    result.success = true;
    return result;
}

// http://www.cplusplus.com/forum/general/223816/ pour wrapper une lambda dans une std::function
// marchera pas avec lambda polymorphique...


std::string _mem_fn_to_lambda_type(const std::string & mem_fn_type)
{
    std::string lambda_full_type = mem_fn_type;
    // Suppress mem_fn< at the start
    size_t idx1 = lambda_full_type.find('<');
    if (idx1 ==  std::string::npos)
        return "Error, can not find first '<' in lambda_full_type: " + lambda_full_type;
    lambda_full_type = lambda_full_type.substr(idx1 + 1);

    // Suppress all after the last ')'
    size_t idx2 = lambda_full_type.rfind(')');
    if (idx1 ==  std::string::npos)
        return "Error, can not find last '>' in lambda_full_type: " + lambda_full_type;
    lambda_full_type = lambda_full_type.substr(0, idx2 + 1);

    // lambda params are at the end between parenthesis
    auto params_r = extract_parenthesis_content_at_end(lambda_full_type);
    std::string params = params_r.parenthesis_content;

    // garbage between the parentheses before (lambda anonymous name)
    auto garbage_r = extract_parenthesis_content_at_end(params_r.remaining);

    std::string return_type = garbage_r.remaining;

    // std::cout << "params= " << params << '\n';
    // std::cout << "return_type= " << return_type << '\n';
    return std::string("lambda: ") + params + " -> " + return_type;
}


template <typename LambdaFunction>
std::string type_lambda(LambdaFunction fn)
{
    // auto f = [&c](int a, int b) -> double { return a + b + c; };
    // MSVC : class std::_Mem_fn<double (__thiscall <lambda_1d102738ade82cc35233c841173ca72c>::*)(int,int)const >
    // clang: std::__1::__mem_fn<double (type_name::_DOCTEST_ANON_FUNC_2()::$_1::*)(int, int) const>
    // MSVC : double (__thiscall <lambda_1d102738ade82cc35233c841173ca72c>::*)(int,int)const

    //auto f = [](int a, int b)  { return std::pair<int, int>(a, b); };
    //clang: std::__1::__mem_fn<std::__1::pair<int, int> (type_name::_DOCTEST_ANON_FUNC_2()::$_1::*)(int, int) const>
    //clang: std::__1::pair<int, int> (type_name::_DOCTEST_ANON_FUNC_2()::$_1::*)(int, int) const

    //clang: std::__1::pair<int, int> (type_name::_DOCTEST_ANON_FUNC_2()::$_1::*)(int, int) const

    // algo :
    // 1.
    // au debut : aller jusqu'au premier < (et le supprimer)
    // a la fin : aller jusqu'a la premiere ")" (et la garder)
    //
    //
    // 2. Aller jusqu'a la premiere parenthese, tout

    auto as_mem_fn = std::mem_fn( & decltype(fn)::operator() );
     // ajouter un param template ici
    // auto as_mem_fn = std::mem_fn( & decltype(fn)::operator<Args...>() );

    std::string mem_fn_type = var_type_name_full(as_mem_fn);
    return _mem_fn_to_lambda_type(mem_fn_type);
}

template <typename LambdaFunction, typename... Args>
std::string type_lambda_polymorphic(LambdaFunction fn)
{
    auto as_mem_fn = std::mem_fn( & LambdaFunction::template operator()<Args...> );
    std::string mem_fn_type = var_type_name_full(as_mem_fn);
    return _mem_fn_to_lambda_type(mem_fn_type);
}

// std::string make_type_lambda_polymorphic()
// auto make_type_lambda_polymorphic = [](auto f) {

// }


    auto f = [](int & a, int & b)  { return std::pair<int, double>(a + b, cos(a + b)); };

void test_lambdas()
{
    // int c = 5;
    // auto f = [&c](int a, int b) -> double { return a + b + c; };
    //auto f = [](int a, int b)  { return std::pair<int, int>(a, b); };

    //auto f = [](int & a, int & b)  { return std::pair<int, double>(a + b, cos(a + b)); };
    std::cout << type_lambda(f) << "\n";

    auto my_square = [](int a) { return a * a;};
    auto my_double = [](int a) { return a * 2; };
    auto ff = fplus::fwd::compose(my_square, my_double);
    auto as_mem_fn = std::mem_fn( & decltype(ff)::operator()<int> );
    std::cout << var_type_name_full(as_mem_fn) << '\n';

    std::cout << '\n';
    std::cout << type_lambda_polymorphic<decltype(ff), int>(ff);
}