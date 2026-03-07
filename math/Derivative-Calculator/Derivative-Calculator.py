print("=" * 58)
print("POLYNOMIAL DERIVATIVE CALCULATOR")
print("=" * 58)
print("Enter coefficients from highest power to constant.")
print("Example: for 3x^3 - 2x + 7, enter: 3,0,-2,7")


def format_number(value):
    if abs(value - round(value)) < 1e-9:
        return str(int(round(value)))
    return f"{value:.6f}".rstrip("0").rstrip(".")


def parse_coefficients(raw):
    parts = [item.strip() for item in raw.split(",") if item.strip()]
    if len(parts) == 0:
        return None, "Please enter at least one coefficient."

    coeffs = []
    for part in parts:
        try:
            coeffs.append(float(part))
        except ValueError:
            return None, f"Invalid coefficient: {part}"

    while len(coeffs) > 1 and abs(coeffs[0]) < 1e-12:
        coeffs.pop(0)

    return coeffs, ""


def derivative_coefficients(coeffs):
    degree = len(coeffs) - 1
    if degree <= 0:
        return [0.0]

    derived = []
    for i, coeff in enumerate(coeffs[:-1]):
        power = degree - i
        derived.append(coeff * power)

    return derived


def nth_derivative_coefficients(coeffs, n):
    result = coeffs[:]
    for _ in range(n):
        result = derivative_coefficients(result)
        if len(result) == 1 and abs(result[0]) < 1e-12:
            return [0.0]
    return result


def evaluate_polynomial(coeffs, x):
    result = 0.0
    for coeff in coeffs:
        result = result * x + coeff
    return result


def polynomial_to_string(coeffs):
    degree = len(coeffs) - 1
    terms = []

    for i, coeff in enumerate(coeffs):
        power = degree - i

        if abs(coeff) < 1e-12:
            continue

        sign = "+" if coeff >= 0 else "-"
        abs_coeff = abs(coeff)

        if power == 0:
            body = format_number(abs_coeff)
        elif power == 1:
            if abs(abs_coeff - 1.0) < 1e-12:
                body = "x"
            else:
                body = f"{format_number(abs_coeff)}x"
        else:
            if abs(abs_coeff - 1.0) < 1e-12:
                body = f"x^{power}"
            else:
                body = f"{format_number(abs_coeff)}x^{power}"

        terms.append((sign, body))

    if not terms:
        return "0"

    first_sign, first_body = terms[0]
    expression = first_body if first_sign == "+" else f"-{first_body}"

    for sign, body in terms[1:]:
        expression += f" {sign} {body}"

    return expression


while True:
    print("\nChoose an option:")
    print("1. Find 1st derivative")
    print("2. Find nth derivative")
    print("3. Evaluate derivative at x")
    print("4. Exit")

    choice = input("Enter your choice (1-4): ").strip()

    if choice == "4":
        print("\nThanks for using Derivative Calculator! ✨")
        break

    if choice not in {"1", "2", "3"}:
        print("❌ Please choose between 1 and 4.")
        continue

    raw = input("\nEnter coefficients (highest power to constant): ").strip()
    coeffs, error = parse_coefficients(raw)
    if error:
        print(f"❌ {error}")
        continue

    print("\nPolynomial:", polynomial_to_string(coeffs))

    if choice == "1":
        first = derivative_coefficients(coeffs)
        print("First derivative:", polynomial_to_string(first))

    elif choice == "2":
        try:
            n = int(input("Enter derivative order n (>= 1): ").strip())
            if n < 1:
                raise ValueError
        except ValueError:
            print("❌ n must be an integer >= 1.")
            continue

        nth = nth_derivative_coefficients(coeffs, n)
        print(f"{n}th derivative:", polynomial_to_string(nth))

    elif choice == "3":
        try:
            x = float(input("Enter x value: ").strip())
            order = int(input("Derivative order to evaluate (>= 1): ").strip())
            if order < 1:
                raise ValueError
        except ValueError:
            print("❌ Enter valid numeric x and integer order >= 1.")
            continue

        derived = nth_derivative_coefficients(coeffs, order)
        value = evaluate_polynomial(derived, x)
        print(f"Derivative used: {polynomial_to_string(derived)}")
        print(f"Value at x = {format_number(x)}: {format_number(value)}")
