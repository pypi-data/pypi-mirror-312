// Functions.cpp

#include "Functions.h"
#include <cmath>

#ifndef M_PI
#define M_PI 3.14159265358979323846
#endif

NumericFunctions::NumericFunctions(double a, double b, const std::string &support)
    : a_(a), b_(b), support_(support)
{
}

double NumericFunctions::function_1(double x, int m)
{
    if (support_ == "hhhh")
    {
        return std::sin(x * M_PI / a_ * m);
    }
    // Weitere Fälle bei Bedarf implementieren
    else
    {
        return 0.0;
    }
}

double NumericFunctions::function_1x(double x, int m)
{
    if (support_ == "hhhh")
    {
        return std::cos(x * M_PI / a_ * m) * M_PI / a_ * m;
    }
    else
    {
        return 0.0;
    }
}

double NumericFunctions::function_1xx(double x, int m)
{
    if (support_ == "hhhh")
    {
        return -std::sin(x * M_PI / a_ * m) * std::pow(M_PI / a_ * m, 2);
    }
    else
    {
        return 0.0;
    }
}

double NumericFunctions::function_2(double y, int n)
{
    if (support_ == "hhhh")
    {
        return std::sin(y * M_PI / b_ * n);
    }
    else
    {
        return 0.0;
    }
}

double NumericFunctions::function_2y(double y, int n)
{
    if (support_ == "hhhh")
    {
        return std::cos(y * M_PI / b_ * n) * M_PI / b_ * n;
    }
    else
    {
        return 0.0;
    }
}

double NumericFunctions::function_2yy(double y, int n)
{
    if (support_ == "hhhh")
    {
        return -std::sin(y * M_PI / b_ * n) * std::pow(M_PI / b_ * n, 2);
    }
    else
    {
        return 0.0;
    }
}
