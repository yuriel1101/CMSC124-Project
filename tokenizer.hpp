#ifndef TOKENIZER_HPP
#define TOKENIZER_HPP

#include <string>
#include <vector>

enum class TokenType {
    INTEGER,
    FLOAT,
    ID,
    OP,
    EXIT,
    UNKNOWN
};

struct Token {
    TokenType type;
    std::string value;
};

/**
 * Converts a single line of SNOL code into a list of tokens.
 * Handles identifiers, literals, operators, and keywords.
 */
std::vector<Token> tokenize(const std::string& line);

#endif // TOKENIZER_HPP
