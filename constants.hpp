#ifndef CONSTANTS_HPP
#define CONSTANTS_HPP

#include <string>
#include <vector>

// Regex patterns for lexical analysis
const std::string IDENTIFIER_REGEX = "[a-zA-Z][a-zA-Z0-9]*";
const std::string FLOAT_REGEX = "[-]?\\d+\\.\\d+";
const std::string INTEGER_REGEX = "[-]?\\d+";

// Valid SNOL operators
const std::vector<std::string> OPERATORS = {"+", "-", "*", "/", "%", "="};

// Reserved keywords in the SNOL language
const std::vector<std::string> KEYWORDS = {"BEG", "PRINT", "EXIT!"};

#endif // CONSTANTS_HPP
