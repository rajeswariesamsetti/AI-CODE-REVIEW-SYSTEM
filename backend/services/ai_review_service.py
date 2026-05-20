import ast
import re

def analyze_code(code, language=None):
    issues = []
    score = 10

    if not code or not str(code).strip():
        return ["Please provide some code to review."], 0

    # Non-python languages
    if language in ["javascript", "js", "c", "cpp", "java"]:
        return analyze_non_python(code, language)

    try:
        tree = ast.parse(code)

        has_functions = False
        loop_vars = set()
        short_vars = set()

        for node in ast.walk(tree):

            if isinstance(node, ast.FunctionDef):
                has_functions = True

            # detect loop variables
            if isinstance(node, ast.For):
                if isinstance(node.target, ast.Name):
                    loop_vars.add(node.target.id)

            # detect variable assignments
            if isinstance(node, ast.Assign):
                for target in node.targets:
                    if isinstance(target, ast.Name):
                        name = target.id
                        if len(name) == 1 and name not in loop_vars and name not in ['i','j','_']:
                            short_vars.add(name)

            # detect function calls
            if isinstance(node, ast.Call):

                if hasattr(node.func, "id"):

                    # security checks
                    if node.func.id in ["eval", "exec"]:
                        issues.append(
                            f"Security Warning: use of '{node.func.id}' on line {node.lineno} is dangerous."
                        )
                        score -= 3

                    # detect debug prints only
                    if node.func.id == "print":
                        if node.args:
                            arg = node.args[0]
                            if isinstance(arg, ast.Constant):
                                text = str(arg.value).lower()
                                if any(w in text for w in ["debug", "temp", "test", "checking"]):
                                    issues.append(
                                        f"Debug print detected on line {node.lineno}"
                                    )
                                    score -= 1

        # variable naming suggestion
        if short_vars:
            vars_str = "', '".join(sorted(short_vars))
            issues.append(f"Suggestion: Use meaningful variable names instead of '{vars_str}'")
            score -= 1

        # suggest functions only if script is large
        if not has_functions and len(code.splitlines()) > 15:
            issues.append("Suggestion: Consider organizing the code into functions.")
            score -= 1

        # large code warning
        if len(code) > 2000:
            issues.append("Suggestion: Code is very long. Break it into smaller modules.")
            score -= 1

        score = max(score, 0)

    except SyntaxError as e:
        issues.append(f"Syntax Error: {e.msg}")
        score = 3

    except Exception as e:
        issues.append(f"Analysis failed: {str(e)}")
        score = 0

    return issues, score


def analyze_non_python(code, language):
    issues = []
    score = 10

    # short variable detection
    short_vars = set(re.findall(r'\b([a-zA-Z])\s*=', code))
    filtered = [v for v in short_vars if v not in ['i','j']]

    if filtered:
        vars_str = "', '".join(sorted(filtered))
        issues.append(f"Suggestion: Use meaningful variable names instead of '{vars_str}'")
        score -= 1

    if language in ["javascript", "js"]:
        if "eval(" in code:
            issues.append("Security Warning: use of 'eval' is dangerous.")
            score -= 3
        if "console.log" in code:
            issues.append("Suggestion: Remove debug console.log statements.")
            score -= 1

    elif language == "java":
        if "System.out.println" in code and "debug" in code.lower():
            issues.append("Debug print detected. Use proper logging.")
            score -= 1

    elif language in ["c", "cpp"]:
        if "gets(" in code:
            issues.append("Security Warning: 'gets' can cause buffer overflow. Use 'fgets'.")
            score -= 3

    if len(code) > 2000:
        issues.append("Suggestion: Break large code into smaller functions.")
        score -= 1

    score = max(score, 0)
    return issues, score