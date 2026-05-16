#include "interpreter.hpp"

/**
 * Main entry point for the SNOL C++ implementation.
 * Provides a portable executable after compilation.
 */
int main() {
    SNOLInterpreter interpreter;
    interpreter.start();
    return 0;
}
