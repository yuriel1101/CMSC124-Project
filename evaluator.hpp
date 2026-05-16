/*
CMSC 124 C-3L Final Project: SNOL Interpreter
Description: Header file for the evaluator module, defining the Value type variant 
and function signatures for mathematical expression evaluation and syntax validation.
*/
#ifndef EVALUATOR_HPP
#define EVALUATOR_HPP

#include "tokenizer.hpp"
#include <map>
#include <string>
#include <variant>
#include <stdexcept>

// SNOL supports both integers and floating point numbers
typedef std::variant<int, double> Value;

/**
 * Evaluates a mathematical expression given as a list of tokens.
 * Uses the symbol table to resolve variable values.
 */
Value evaluate_expression(const std::vector<Token>& tokens, const std::map<std::string, Value>& symbol_table);

/**
 * Validates if the sequence of tokens follows correct expression syntax.
 */
bool is_valid_expression_syntax(const std::vector<Token>& tokens);

#endif // EVALUATOR_HPP
