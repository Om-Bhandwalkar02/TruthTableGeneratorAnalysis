import itertools
import pandas as pd
from sympy import symbols, simplify_logic, sympify
import re

def advanced_truth_table(user_expression):
    try:
        replacements = {'∧': '&', '∨': '|', '¬': '~', '→': '>>', '↔': '<<'}
        sympy_expression = user_expression
        for old, new in replacements.items():
            sympy_expression = sympy_expression.replace(old, new)

        variables = sorted(set(re.findall(r'\b[a-zA-Z]+\b', sympy_expression)), key=lambda x: x.lower())
        var_symbols = {var: symbols(var) for var in variables}
        expr = sympify(sympy_expression, locals=var_symbols)

        n = len(variables)
        combinations = list(itertools.product([True, False], repeat=n))

        table = []
        for combo in combinations:
            env = {var: val for var, val in zip(var_symbols.values(), combo)}
            result = bool(expr.subs(env))
            table.append(list(combo) + [result])

        df = pd.DataFrame(table, columns=variables + [user_expression])

        is_tautology = all(row[-1] for row in table)
        is_contradiction = not any(row[-1] for row in table)
        is_contingency = not is_tautology and not is_contradiction

        simplified_expr = str(simplify_logic(expr))
        simplified_expr = (simplified_expr.replace("&", "∧")
                                          .replace("|", "∨")
                                          .replace("~", "¬")
                                          .replace(">>", "→")
                                          .replace("<<", "↔"))

        return {
            "truth_table": df,
            "tautology": is_tautology,
            "contradiction": is_contradiction,
            "contingency": is_contingency,
            "simplified": simplified_expr,
            "error": None
        }
    except Exception as e:
        return {"error": str(e)}

def terminal_app():
    print("Welcome to the Truth Table Generator!")
    while True:
        expression = input("\nEnter a logical expression (e.g., '(p ∧ q) → ¬r') or 'exit' to quit: ")
        if expression.lower() == 'exit':
            break

        result = advanced_truth_table(expression)
        if result["error"]:
            print(f"Error: {result['error']}")
        else:
            print("\nTruth Table:")
            print(result["truth_table"].to_string(index=False))
            print(f"\nTautology: {result['tautology']}")
            print(f"Contradiction: {result['contradiction']}")
            print(f"Contingency: {result['contingency']}")
            print(f"Simplified Expression: {result['simplified']}")

if __name__ == "__main__":
    terminal_app()