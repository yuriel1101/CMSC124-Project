#include "evaluator.hpp"
#include <stack>
#include <cmath>

int get_precedence(const std::string& op) {
    if (op == "*" || op == "/" || op == "%") return 2;
    if (op == "+" || op == "-") return 1;
    return 0;
}

Value apply_op(Value left, const std::string& op, Value right) {
    // Check if types are consistent (SNOL requirement)
    if (left.index() != right.index()) {
        throw std::runtime_error("Incompatible types");
    }

    if (left.index() == 0) { // Integer operations
        int l = std::get<int>(left);
        int r = std::get<int>(right);
        if (op == "+") return l + r;
        if (op == "-") return l - r;
        if (op == "*") return l * r;
        if (op == "/") {
            if (r == 0) throw std::runtime_error("Division by zero!");
            return l / r;
        }
        if (op == "%") {
            if (r == 0) throw std::runtime_error("Modulo by zero!");
            return l % r;
        }
    } else { // Floating point operations
        double l = std::get<double>(left);
        double r = std::get<double>(right);
        if (op == "+") return l + r;
        if (op == "-") return l - r;
        if (op == "*") return l * r;
        if (op == "/") {
            if (r == 0) throw std::runtime_error("Division by zero!");
            return l / r;
        }
        if (op == "%") {
            throw std::runtime_error("Modulo operation is only allowed for integer type!");
        }
    }
    throw std::runtime_error("Unknown operator");
}

Value evaluate_expression(const std::vector<Token>& tokens, const std::map<std::string, Value>& symbol_table) {
    if (tokens.empty()) throw std::runtime_error("Empty expression");

    std::stack<Value> values;
    std::stack<std::string> ops;
    bool expect_term = true;

    auto process_top_op = [&]() {
        Value r = values.top(); values.pop();
        Value l = values.top(); values.pop();
        std::string o = ops.top(); ops.pop();
        values.push(apply_op(l, o, r));
    };

    for (const auto& token : tokens) {
        if (expect_term) {
            if (token.type == TokenType::INTEGER) {
                values.push(std::stoi(token.value));
                expect_term = false;
            } else if (token.type == TokenType::FLOAT) {
                values.push(std::stod(token.value));
                expect_term = false;
            } else if (token.type == TokenType::ID) {
                if (token.value == "BEG" || token.value == "PRINT") {
                    throw std::runtime_error("Keyword in expression");
                }
                if (symbol_table.count(token.value)) {
                    values.push(symbol_table.at(token.value));
                } else {
                    throw std::runtime_error("Undefined variable [" + token.value + "]");
                }
                expect_term = false;
            } else {
                throw std::runtime_error("Expected term");
            }
        } else {
            if (token.type == TokenType::OP && token.value != "=") {
                while (!ops.empty() && get_precedence(ops.top()) >= get_precedence(token.value)) {
                    process_top_op();
                }
                ops.push(token.value);
                expect_term = true;
            } else {
                throw std::runtime_error("Expected operator");
            }
        }
    }

    if (expect_term) throw std::runtime_error("Trailing operator");

    while (!ops.empty()) {
        process_top_op();
    }

    return values.top();
}

bool is_valid_expression_syntax(const std::vector<Token>& tokens) {
    if (tokens.empty()) return false;
    bool expect_term = true;
    for (const auto& token : tokens) {
        if (expect_term) {
            if (token.type == TokenType::INTEGER || token.type == TokenType::FLOAT || token.type == TokenType::ID) {
                if (token.value == "BEG" || token.value == "PRINT") return false;
                expect_term = false;
            } else return false;
        } else {
            if (token.type == TokenType::OP && token.value != "=") {
                expect_term = true;
            } else return false;
        }
    }
    return !expect_term;
}
