import json
import random
import re

operations = [
    r"\sqrt{{{}}}",
    r"\sum_{{i=0}}^\infty {{{}}}",
    # r"\binom{{{}}}{{{}}}",
    r"{} + {}",
    r"{} - {}",
    r"{} \times {}",
    r"\frac{{{}}}{{{}}}",
]

components = []


def random_component():
    random_choice = random.random()

    if random_choice < 0.2:
        random_choice = random.random()
        # wrap the random component in parentheses
        random_binary_operation = random.choice(["{} + {}", "{} - {}", "{} \\times {}"])
        res = random_binary_operation.format(random_component(), random_component())
        if random_choice < 0.3:
            return "({})".format(res)
        else:
            return res
    else:
        return random.choice(components)


"""Generate a random mathematical expression."""


def generate_random_expr(num_operations=3):
    cur_expr = random_component()

    for _ in range(num_operations):
        operation = random.choice(operations)

        operand_count = operation.count("{}")

        if operand_count == 1:
            cur_expr = operation.format(cur_expr)
        elif operand_count == 2:
            new_component = random_component()
            cur_expr = operation.format(cur_expr, new_component)

    return cur_expr


"""
Generate a natural language description of a mathematical expression using the following rules:
\\sqrt{n} -> "square root of (the quantity) n"
\\frac{a}{b} -> "fraction with numerator (the quantity) a and denominator (the quantity) b"
\\sum_{i = 0}^\\infty f(i) -> "sum from i equals 0 to infinity of (the quantity) f(i)"
\\binom{a}{b} -> "binomial coefficient with upper index (the quantity) a and lower index (the quantity) b"

Append “followed by” if character immediately after } is not another brace.
"""


def natural_language(expr):
    i = 0
    res = ""
    while i < len(expr):
        if expr[i] == "f" and i - 1 >= 0 and expr[i - 1] == "\\":
            res += " fraction with numerator (the quantity) "
            i += 5
            continue
        if expr[i] == "s" and i + 1 < len(expr) and expr[i + 1] == "u":
            res += " sum from i equals 0 to infinity of (the quantity) "
            i += 17
            continue
        if expr[i] == "s" and i + 1 < len(expr) and expr[i + 1] == "q":
            res += " square root of (the quantity) "
            i += 5
            continue
        if expr[i] == "}" and i + 1 < len(expr) and expr[i + 1] == "{":
            res += " and denominator (the quantity) "

        if expr[i] == "+":
            res += " plus "
            i += 1
            continue
        if expr[i] == "-":
            res += " minus "
            i += 1
            continue

        if expr[i] == "(":
            res += " opening parenthesis "
            i += 1
            continue

        if expr[i] == ")":
            res += " closing parenthesis "
            i += 1
            continue

        # find first non-whitespace character after }
        if expr[i] == "}":
            j = i + 1
            while j < len(expr) and expr[j] == " ":
                j += 1
            if j < len(expr) and (expr[j] != "{" and expr[j] != "}"):
                res += " followed by "

        if expr[i] == "\\" or expr[i] == "{" or expr[i] == "}":
            i += 1
            continue

        res += expr[i]
        i += 1

    return res


with open("components.txt", "r") as file:
    components = [line.strip() for line in file]
# temp = generate_random_expr(3)
# print(temp)
# print(natural_language(temp.replace('\\', '\\\\')))

with open("gemini-training.jsonl", "w") as file:
    for i in range(200):
        # for non-gemini models
        # template = {}
        # template["input_text"] = generate_random_expr(random.randint(3, 4))
        # template["output_text"] = re.sub(r"\s+", " ", natural_language(template["input_text"]))
        # file.write(json.dumps(template) + "\n")

        contents = []
        contents.append(
            {
                "role": "user",
                "parts": [{"text": generate_random_expr(random.randint(3, 4))}],
            }
        )
        translation = re.sub(r"\s+", " ", natural_language(contents[-1]["parts"][0]["text"]))
        contents.append({"role": "model", "parts": [{"text": translation}]})

        res = {"contents": contents}
        file.write(json.dumps(res) + "\n")

        print(f"finished {i}")
