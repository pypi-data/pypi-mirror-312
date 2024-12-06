// Functions.h

#ifndef FUNCTIONS_H
#define FUNCTIONS_H

#include <string>

class NumericFunctions
{
public:
    NumericFunctions(double a, double b, const std::string &support);

    double function_1(double x, int m);
    double function_1x(double x, int m);
    double function_1xx(double x, int m);
    double function_2(double y, int n);
    double function_2y(double y, int n);
    double function_2yy(double y, int n);

private:
    double a_;
    double b_;
    std::string support_;
};

#endif // FUNCTIONS_H
