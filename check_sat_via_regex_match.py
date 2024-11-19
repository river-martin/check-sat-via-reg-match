import re


def construct_pattern(num_vars: int, clauses: list[list[int]]) -> str:
    r"""
    Construct a regex pattern that verifies whether a given assignment satisfies a given CNF formula.

    Deterministic capture groups are used to capture the values assigned to the variables,
    and back-references used to reference the assigned values in the sub-expressions corresponding to clauses.

    :param num_vars: Number of variables in the CNF formula
    :param clauses: List of clauses in the CNF formula

    :return: A regex pattern that matches a string of the form "XYZ...;FT,FT,FT,..."

    # Example

    Given the clauses:

    ```
    [
        (x1 ∨ x2 ∨ ¬x3),
        (x1 ∨ ¬x2 ∨ x3),
        (¬x1 ∨ ¬x2 ∨ x3),
        (¬x1 ∨ ¬x2 ∨ ¬x3)
    ]
    ```

    We construct the pattern:

    ```
    /
        ^( (F|T) (F|T) (F|T) );    # Capture values assigned to x1, x2, x3
        (?=FT,FT,FT,FT$)            # Ensure that only valid input strings can be accepted
        (?: F\1 | F\2 | \3T ),     # Match FT if the assigned values satisfy clause 1
        (?: F\1 | \2T | F\3 ),     # Match FT if the assigned values satisfy clause 2
        (?: \1T | \2T | F\3 ),     # Match FT if the assigned values satisfy clause 3
        (?: \1T | \2T | \3T )      # Match FT if the assigned values satisfy clause 4
    /x
    ```

    This matches strings of the form "XYZ;FT,FT,FT,FT" where X, Y, Z are either F or T,
    and specify the values assigned to x1, x2, x3, respectively.
    """
    clause_patterns = []
    for clause in clauses:
        terms = []
        for literal in clause:
            if literal < 0:
                # Will match 'FT' if the negated literal is set to F
                terms.append(rf"\{abs(literal)}T")
            else:
                # Will match 'FT' if the non-negated literal is set to T
                terms.append(rf"F\{literal}")
        clause_patterns.append(rf"(?:{'|'.join(terms)})")
        pattern = rf'^{"(F|T)" * num_vars};' + f"(?={','.join('FT' for i in range(len(clause_patterns)))})"+ ",".join(clause_patterns)
    return pattern


def check_sat(assignment: str, regex: re.Pattern, num_clauses: int) -> bool:
    """Checks whether the given assignment satisfies the CNF formula.

    :param assignment: A string of the form f"{X}{Y}{Z}", where X, Y, Z are either 'F' or 'T'.
    :param regex: A compiled regex pattern constructed using `construct_pattern`
    :param num_clauses: Number of clauses in the CNF formula

    :return: `True` if the given assignment satisfies the CNF formula, `False` otherwise.
    """
    test_string = rf"{assignment};" + ",".join(["FT"] * num_clauses)
    return regex.match(test_string) is not None


def int_to_binary_string(i: int, num_bits: int) -> str:
    """Convert an integer to a binary string of a fixed length

    :param i: Integer to convert
    :param num_bits: Number of bits in the binary string to return

    :return: Binary representation of `i`
    """
    return format(i, f"0{num_bits}b")


def enumerate_assignments(num_vars: int):
    """
    Enumerate all possible 2^n assignments of True/False to n variables

    :param num_vars: Number of variables in the CNF formula

    :return: A generator that yields all possible assignments of True/False to the variables
    """
    for i in range(0, 2**num_vars):
        yield int_to_binary_string(i, num_vars).replace("0", "F").replace("1", "T")


# Example usage

n_vars = 3

clauses = [
    [1, 2, -3],    # Clause 1: (x1 ∨ x2 ∨ ¬x3)
    [1, -2, 3],    # Clause 2: (x1 ∨ ¬x2 ∨ x3)
    [-1, -2, 3],   # Clause 3: (¬x1 ∨ ¬x2 ∨ x3)
    [-1, -2, -3],  # Clause 4: (¬x1 ∨ ¬x2 ∨ ¬x3)
]

pattern = construct_pattern(n_vars, clauses)
print(pattern)
regex = re.compile(pattern)
for assignment in enumerate_assignments(n_vars):
    if check_sat(assignment, regex, len(clauses)):
        print(assignment, "SAT", sep="\t")
    else:
        print(assignment, "UNSAT", sep="\t")
