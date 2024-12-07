// plate_bending.cpp

#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <vector>
#include <cmath> // Für pow und trigonometrische Funktionen
#include "Functions.h"

namespace py = pybind11;

std::vector<double> create_discretized_list(double start, double end, int num_intervals)
{
    std::vector<double> list;
    double step = (end - start) / num_intervals;
    for (int i = 0; i <= num_intervals; ++i)
    {
        list.push_back(start + i * step);
    }
    return list;
}

std::vector<std::vector<double>> assemble_stiffness_matrix(
    double D_11, double D_22, double D_12, double D_66,
    int reihen, int n_inte, double a, double b, const std::string &support)
{
    NumericFunctions nf(a, b, support);

    std::vector<double> list_a = create_discretized_list(0.0, a, n_inte);
    std::vector<double> list_b = create_discretized_list(0.0, b, n_inte);

    int matrix_size = reihen * reihen;
    std::vector<std::vector<double>> matrix(matrix_size, std::vector<double>(matrix_size, 0.0));

    // Generierung der Steifigkeitsmatrix
    for (int m = 1; m <= reihen; ++m)
    {
        for (int n = 1; n <= reihen; ++n)
        {
            for (int p = 1; p <= reihen; ++p)
            {
                for (int q = 1; q <= reihen; ++q)
                {
                    double lambda_x22_pm = NumericalIntegration::integrate_product(
                        [&nf](double x, int p)
                        { return nf.function_1xx(x, p); },
                        [&nf](double x, int m)
                        { return nf.function_1xx(x, m); },
                        list_a, p, m);

                    double lambda_x22_mp = NumericalIntegration::integrate_product(
                        [&nf](double x, int m)
                        { return nf.function_1xx(x, m); },
                        [&nf](double x, int p)
                        { return nf.function_1xx(x, p); },
                        list_a, m, p);

                    double lambda_y00_nq = NumericalIntegration::integrate_product(
                        [&nf](double y, int n)
                        { return nf.function_2(y, n); },
                        [&nf](double y, int q)
                        { return nf.function_2(y, q); },
                        list_b, n, q);

                    double lambda_y00_qn = NumericalIntegration::integrate_product(
                        [&nf](double y, int q)
                        { return nf.function_2(y, q); },
                        [&nf](double y, int n)
                        { return nf.function_2(y, n); },
                        list_b, q, n);

                    double lambda_x00_mp = NumericalIntegration::integrate_product(
                        [&nf](double x, int m)
                        { return nf.function_1(x, m); },
                        [&nf](double x, int p)
                        { return nf.function_1(x, p); },
                        list_a, m, p);

                    double lambda_x00_pm = NumericalIntegration::integrate_product(
                        [&nf](double x, int p)
                        { return nf.function_1(x, p); },
                        [&nf](double x, int m)
                        { return nf.function_1(x, m); },
                        list_a, p, m);

                    double lambda_y22_nq = NumericalIntegration::integrate_product(
                        [&nf](double y, int n)
                        { return nf.function_2yy(y, n); },
                        [&nf](double y, int q)
                        { return nf.function_2yy(y, q); },
                        list_b, n, q);

                    double lambda_y22_qn = NumericalIntegration::integrate_product(
                        [&nf](double y, int q)
                        { return nf.function_2yy(y, q); },
                        [&nf](double y, int n)
                        { return nf.function_2yy(y, n); },
                        list_b, q, n);

                    double lambda_x20_mp = NumericalIntegration::integrate_product(
                        [&nf](double x, int m)
                        { return nf.function_1xx(x, m); },
                        [&nf](double x, int p)
                        { return nf.function_1(x, p); },
                        list_a, m, p);

                    double lambda_x20_pm = NumericalIntegration::integrate_product(
                        [&nf](double x, int p)
                        { return nf.function_1xx(x, p); },
                        [&nf](double x, int m)
                        { return nf.function_1(x, m); },
                        list_a, p, m);

                    double lambda_y02_nq = NumericalIntegration::integrate_product(
                        [&nf](double y, int n)
                        { return nf.function_2(y, n); },
                        [&nf](double y, int q)
                        { return nf.function_2yy(y, q); },
                        list_b, n, q);

                    double lambda_y02_qn = NumericalIntegration::integrate_product(
                        [&nf](double y, int q)
                        { return nf.function_2(y, q); },
                        [&nf](double y, int n)
                        { return nf.function_2yy(y, n); },
                        list_b, q, n);

                    double lambda_x11_mp = NumericalIntegration::integrate_product(
                        [&nf](double x, int m)
                        { return nf.function_1x(x, m); },
                        [&nf](double x, int p)
                        { return nf.function_1x(x, p); },
                        list_a, m, p);

                    double lambda_x11_pm = NumericalIntegration::integrate_product(
                        [&nf](double x, int p)
                        { return nf.function_1x(x, p); },
                        [&nf](double x, int m)
                        { return nf.function_1x(x, m); },
                        list_a, p, m);

                    double lambda_y11_nq = NumericalIntegration::integrate_product(
                        [&nf](double y, int n)
                        { return nf.function_2y(y, n); },
                        [&nf](double y, int q)
                        { return nf.function_2y(y, q); },
                        list_b, n, q);

                    double lambda_y11_qn = NumericalIntegration::integrate_product(
                        [&nf](double y, int q)
                        { return nf.function_2y(y, q); },
                        [&nf](double y, int n)
                        { return nf.function_2y(y, n); },
                        list_b, q, n);

                    double value = 0.0;

                    if (m == p)
                    {
                        value =
                            0.5 * D_11 * (lambda_x22_mp * lambda_y00_nq + lambda_x22_pm * lambda_y00_qn) +
                            0.5 * D_22 * (lambda_x00_mp * lambda_y22_nq + lambda_x00_pm * lambda_y22_qn) +
                            D_12 * (lambda_x20_mp * lambda_y02_nq + lambda_x20_pm * lambda_y02_qn) +
                            2 * D_66 * (lambda_x11_pm * lambda_y11_nq + lambda_x11_mp * lambda_y11_nq);
                    }
                    else
                    {
                        value =
                            0.5 * D_11 * (lambda_x22_mp * lambda_y00_nq + lambda_x22_pm * lambda_y00_qn) +
                            0.5 * D_22 * (lambda_x00_mp * lambda_y22_nq + lambda_x00_pm * lambda_y22_qn) +
                            D_12 * (lambda_x20_mp * lambda_y02_nq + lambda_x20_pm * lambda_y02_qn) +
                            2 * D_66 * (lambda_x11_mp * lambda_y11_nq + lambda_x11_pm * lambda_y11_qn);
                    }

                    if (std::abs(value) < 1e-9)
                    {
                        value = 0.0;
                    }

                    int row = n - 1 + reihen * (m - 1);
                    int col = q - 1 + reihen * (p - 1);
                    matrix[row][col] = value;
                }
            }
        }
    }

    return matrix;
}

PYBIND11_MODULE(plate_bending_cpp, m)
{
    m.doc() = "pybind11 Modul zur Assemblierung der Steifigkeitsmatrix für Plattenbiegung";

    m.def("assemble_stiffness_matrix", &assemble_stiffness_matrix,
          "Assemblierung der Steifigkeitsmatrix",
          py::arg("D_11"), py::arg("D_22"), py::arg("D_12"), py::arg("D_66"),
          py::arg("reihen"), py::arg("n_inte"), py::arg("a"), py::arg("b"), py::arg("support"));
}
