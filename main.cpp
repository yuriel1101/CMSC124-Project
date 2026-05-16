/*
CMSC 124 C-3L Final Project: SNOL Interpreter
Developers: Lorejo, Nuñal, Villaflores
Description: Serves as the primary entry point for the SNOL interpreter, 
instantiating the interpreter core and initiating the interactive user session.
*/
#include "interpreter.hpp"

int main() {
    SNOLInterpreter interpreter;
    interpreter.start();
    return 0;
}
