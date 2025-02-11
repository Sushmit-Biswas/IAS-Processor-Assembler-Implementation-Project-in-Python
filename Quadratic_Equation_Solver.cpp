#include <iostream>
#include <cmath>
using namespace std;

void roots(int a, int b, int c)
{
    if (a == 0) return;
    int discriminant = b * b - 4 * a * c;
    float sqrt_dis = sqrt(discriminant);
    // x1 and x2 are the roots of our quadratic eqn
    if (discriminant >= 0) {
        cout << "Discriminant is non-negative, so both roots are real.\n";
        cout << "x1 = " << (-b + sqrt_dis) / (2 * a) << "\n"
                  << "x2 = " << (-b - sqrt_dis) / (2 * a) << endl;
    }
    else
        // x1 and x2 are complex numbers   
        cout << "Discriminant is negative, so both roots are complex and not real." << endl;
}

int main()
{
    int a, b, c; // ax^2 + bx + c is the quadratic
    cout << "This program solves quadratic equations of the form: ax^2 + bx + c = 0\n";
    cout << "Enter the coefficients a, b, and c (where a != 0): ";
    cin >> a >> b >> c;
    roots(a, b, c);
    return 0;
}