print("=" * 58)
print("AP / GP / AGP / HP RECOGNIZER")
print("=" * 58)
print("Enter at least 4 numbers separated by commas.")
print("Example: 2, 4, 6, 8 or 3, 6, 12, 24")

EPS = 1e-9


def is_close(a, b, eps=EPS):
    return abs(a - b) <= eps


def parse_sequence(raw):
    parts = [item.strip() for item in raw.split(",") if item.strip()]
    if len(parts) < 4:
        return None, "Please enter at least 4 values."

    sequence = []
    for part in parts:
        try:
            sequence.append(float(part))
        except ValueError:
            return None, f"Invalid number: {part}"

    return sequence, ""


def check_ap(sequence):
    diff = sequence[1] - sequence[0]
    for i in range(2, len(sequence)):
        if not is_close(sequence[i] - sequence[i - 1], diff):
            return False, None
    return True, diff


def check_gp(sequence):
    if all(is_close(value, 0.0) for value in sequence):
        return True, 0.0

    if any(is_close(sequence[i - 1], 0.0) for i in range(1, len(sequence))):
        return False, None

    ratio = sequence[1] / sequence[0]
    for i in range(2, len(sequence)):
        if not is_close(sequence[i] / sequence[i - 1], ratio):
            return False, None

    return True, ratio


def check_hp(sequence):
    if any(is_close(value, 0.0) for value in sequence):
        return False, None

    reciprocal = [1 / value for value in sequence]
    is_ap, reciprocal_diff = check_ap(reciprocal)
    if not is_ap:
        return False, None

    return True, reciprocal_diff


def agp_candidates(sequence):
    s0, s1, s2 = sequence[0], sequence[1], sequence[2]

    if is_close(s0, 0.0):
        if is_close(s1, 0.0):
            return []
        return [s2 / (2 * s1)]

    a = s0
    b = -2 * s1
    c = s2
    disc = b * b - 4 * a * c

    if disc < -EPS:
        return []

    if is_close(disc, 0.0):
        return [-b / (2 * a)]

    if disc < 0:
        return []

    sqrt_disc = disc ** 0.5
    r1 = (-b + sqrt_disc) / (2 * a)
    r2 = (-b - sqrt_disc) / (2 * a)

    if is_close(r1, r2):
        return [r1]

    return [r1, r2]


def check_agp(sequence):
    for ratio in agp_candidates(sequence):
        valid = True
        for i in range(2, len(sequence)):
            expected = 2 * ratio * sequence[i - 1] - (ratio * ratio) * sequence[i - 2]
            if not is_close(sequence[i], expected, eps=1e-7):
                valid = False
                break
        if valid:
            return True, ratio

    return False, None


def format_number(value):
    if is_close(value, round(value)):
        return str(int(round(value)))
    return f"{value:.6g}"


while True:
    print("\nChoose an option:")
    print("1. Recognize sequence type")
    print("2. Exit")

    choice = input("Enter your choice (1-2): ").strip()

    if choice == "2":
        print("\nThanks for using the recognizer. Keep practicing! ✨")
        break

    if choice != "1":
        print("Please choose 1 or 2.")
        continue

    user_input = input("\nEnter sequence values separated by commas: ")
    sequence, error = parse_sequence(user_input)

    if error:
        print(f"❌ {error}")
        continue

    matched_types = []

    ap_ok, ap_diff = check_ap(sequence)
    if ap_ok:
        matched_types.append(f"AP (common difference d = {format_number(ap_diff)})")

    gp_ok, gp_ratio = check_gp(sequence)
    if gp_ok:
        matched_types.append(f"GP (common ratio r = {format_number(gp_ratio)})")

    agp_ok, agp_ratio = check_agp(sequence)
    if agp_ok:
        matched_types.append(f"AGP (repetition ratio r = {format_number(agp_ratio)})")

    hp_ok, hp_diff = check_hp(sequence)
    if hp_ok:
        matched_types.append(
            f"HP (reciprocal AP difference = {format_number(hp_diff)})"
        )

    print("\nResult")
    print("-" * 58)
    print("Sequence:", ", ".join(format_number(x) for x in sequence))

    if matched_types:
        print("✅ Recognized as:")
        for seq_type in matched_types:
            print("  -", seq_type)
    else:
        print("❌ Not AP, GP, AGP, or HP for the given values.")

    print("-" * 58)
