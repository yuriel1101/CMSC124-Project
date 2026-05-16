#include "interpreter.hpp"
#include <regex>
#include <sstream>

SNOLInterpreter::SNOLInterpreter() : running(true) {}

void SNOLInterpreter::print_value(const std::string& label, const Value& val) {
    std::cout << "SNOL> [" << label << "] = ";
    if (val.index() == 0) std::cout << std::get<int>(val);
    else std::cout << std::get<double>(val);
    std::cout << std::endl;
}

void SNOLInterpreter::run_command(const std::string& line) {
    // Check for unknown words
    std::stringstream ss(line);
    std::string word;
    while (ss >> word) {
        auto word_tokens = tokenize(word);
        for (const auto& t : word_tokens) {
            if (t.type == TokenType::UNKNOWN) {
                std::cout << "SNOL> Unknown word [" << word << "]" << std::endl;
                return;
            }
        }
    }

    auto tokens = tokenize(line);
    if (tokens.empty()) return;

    // EXIT!
    if (tokens[0].type == TokenType::EXIT) {
        std::cout << "\nInterpreter is now terminated..." << std::endl;
        running = false;
        return;
    }

    // BEG
    if (tokens[0].type == TokenType::ID && tokens[0].value == "BEG") {
        if (tokens.size() == 2 && tokens[1].type == TokenType::ID) {
            std::string var_name = tokens[1].value;
            if (var_name == "BEG" || var_name == "PRINT") {
                std::cout << "SNOL> Unknown command! What follows the keyword BEG should be a variable" << std::endl;
                return;
            }
            std::cout << "SNOL> Please enter value for [" << var_name << "]:" << std::endl;
            std::cout << "Input: ";
            std::string input_val;
            std::cin >> input_val;
            try {
                if (std::regex_match(input_val, std::regex("^-?\\d+\\.\\d+"))) {
                    symbol_table[var_name] = std::stod(input_val);
                } else if (std::regex_match(input_val, std::regex("^-?\\d+"))) {
                    symbol_table[var_name] = std::stoi(input_val);
                } else {
                    throw std::runtime_error("Invalid format");
                }
            } catch (...) {
                std::cout << "SNOL> Invalid number format [" << input_val << "]" << std::endl;
            }
            return;
        }
        std::cout << "SNOL> Unknown command! What follows the keyword BEG should be a variable" << std::endl;
        return;
    }

    // PRINT
    if (tokens[0].type == TokenType::ID && tokens[0].value == "PRINT") {
        if (tokens.size() == 2) {
            const auto& t = tokens[1];
            if (t.type == TokenType::ID) {
                if (symbol_table.count(t.value)) {
                    print_value(t.value, symbol_table.at(t.value));
                } else {
                    std::cout << "SNOL> Undefined variable [" << t.value << "]" << std::endl;
                }
            } else if (t.type == TokenType::INTEGER) {
                std::cout << "SNOL> [" << t.value << "] = " << t.value << std::endl;
            } else if (t.type == TokenType::FLOAT) {
                std::cout << "SNOL> [" << t.value << "] = " << t.value << std::endl;
            } else {
                std::cout << "SNOL> Unknown command! Does not match any valid command of the language." << std::endl;
            }
            return;
        }
        std::cout << "SNOL> Unknown command! Does not match any valid command of the language." << std::endl;
        return;
    }

    // Assignment
    if (tokens[0].type == TokenType::ID && tokens.size() >= 3 && tokens[1].type == TokenType::OP && tokens[1].value == "=") {
        std::string var_name = tokens[0].value;
        if (var_name == "BEG" || var_name == "PRINT") {
            std::cout << "SNOL> Unknown command!" << std::endl;
            return;
        }
        std::vector<Token> expr_tokens(tokens.begin() + 2, tokens.end());
        if (is_valid_expression_syntax(expr_tokens)) {
            try {
                symbol_table[var_name] = evaluate_expression(expr_tokens, symbol_table);
            } catch (const std::exception& e) {
                std::string msg = e.what();
                if (msg.find("Incompatible") != std::string::npos || msg.find("Undefined") != std::string::npos || msg.find("Modulo operation") != std::string::npos) {
                    std::cout << "SNOL> " << msg << std::endl;
                } else {
                    std::cout << "SNOL> Unknown command! Does not match any valid command of the language." << std::endl;
                }
            }
        } else {
            std::cout << "SNOL> Unknown command! Does not match any valid command of the language." << std::endl;
        }
        return;
    }

    // Standalone expression
    if (is_valid_expression_syntax(tokens)) {
        if (tokens.size() == 1 && tokens[0].type == TokenType::ID) {
            if (!symbol_table.count(tokens[0].value) && tokens[0].value != "BEG" && tokens[0].value != "PRINT") {
                std::cout << "SNOL> Unknown word [" << tokens[0].value << "]" << std::endl;
                return;
            }
        }
        try {
            evaluate_expression(tokens, symbol_table);
        } catch (const std::exception& e) {
            std::string msg = e.what();
             if (msg.find("Incompatible") != std::string::npos || msg.find("Undefined") != std::string::npos || msg.find("Modulo operation") != std::string::npos) {
                std::cout << "SNOL> " << msg << std::endl;
            } else {
                std::cout << "SNOL> Unknown command! Does not match any valid command of the language." << std::endl;
            }
        }
        return;
    }

    std::cout << "SNOL> Unknown command! Does not match any valid command of the language." << std::endl;
}

void SNOLInterpreter::start() {
    std::cout << "The SNOL environment is now active, you may proceed with giving your commands.\n" << std::endl;
    std::string line;
    while (running) {
        std::cout << "Command: ";
        if (!std::getline(std::cin, line)) break;
        if (line.empty()) continue;
        run_command(line);
    }
}
