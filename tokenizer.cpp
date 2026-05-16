#include "tokenizer.hpp"
#include <regex>
#include <cctype>

std::vector<Token> tokenize(const std::string& line) {
    std::vector<Token> tokens;
    size_t i = 0;
    
    while (i < line.length()) {
        if (std::isspace(line[i])) {
            i++;
            continue;
        }
        
        // Check for EXIT!
        if (line.substr(i, 5) == "EXIT!") {
            tokens.push_back({TokenType::EXIT, "EXIT!"});
            i += 5;
            continue;
        }
        
        // Operators except hyphen
        if (std::string("+*/%=").find(line[i]) != std::string::npos) {
            tokens.push_back({TokenType::OP, std::string(1, line[i])});
            i++;
            continue;
        }
        
        // Handle hyphen
        if (line[i] == '-') {
            bool is_negative_sign = tokens.empty() || tokens.back().type == TokenType::OP;
            if (is_negative_sign) {
                std::regex neg_num_regex("^-?\\d+(\\.\\d+)?");
                std::smatch match;
                std::string sub = line.substr(i);
                if (std::regex_search(sub, match, neg_num_regex)) {
                    std::string val = match.str();
                    if (val.find('.') != std::string::npos) {
                        tokens.push_back({TokenType::FLOAT, val});
                    } else {
                        tokens.push_back({TokenType::INTEGER, val});
                    }
                    i += val.length();
                    continue;
                }
            }
            tokens.push_back({TokenType::OP, "-"});
            i++;
            continue;
        }
        
        // Float literal
        std::regex float_regex("^\\d+\\.\\d+");
        std::smatch match;
        std::string sub = line.substr(i);
        if (std::regex_search(sub, match, float_regex)) {
            tokens.push_back({TokenType::FLOAT, match.str()});
            i += match.length();
            continue;
        }
        
        // Integer literal
        std::regex int_regex("^\\d+");
        if (std::regex_search(sub, match, int_regex)) {
            tokens.push_back({TokenType::INTEGER, match.str()});
            i += match.length();
            continue;
        }
        
        // Identifier
        std::regex id_regex("^[a-zA-Z][a-zA-Z0-9]*");
        if (std::regex_search(sub, match, id_regex)) {
            tokens.push_back({TokenType::ID, match.str()});
            i += match.length();
            continue;
        }
        
        // Unknown
        tokens.push_back({TokenType::UNKNOWN, std::string(1, line[i])});
        i++;
    }
    return tokens;
}
