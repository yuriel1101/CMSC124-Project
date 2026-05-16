#ifndef INTERPRETER_HPP
#define INTERPRETER_HPP

#include "evaluator.hpp"
#include <iostream>

class SNOLInterpreter {
public:
    SNOLInterpreter();
    /**
     * Starts the interactive shell for SNOL.
     */
    void start();

private:
    std::map<std::string, Value> symbol_table;
    bool running;

    /**
     * Executes a single line of input.
     */
    void run_command(const std::string& line);
    
    /**
     * Helper to print a Value to the console.
     */
    void print_value(const std::string& label, const Value& val);
};

#endif // INTERPRETER_HPP
