import math

print("=" * 58)
print("CARTESIAN TO POLAR TRANSFORMATION")
print("=" * 58)
print("Convert (x, y) coordinates to polar form (r, theta).")


def format_number(value):
    if abs(value - round(value)) < 1e-9:
        return str(int(round(value)))
    return f"{value:.6f}".rstrip("0").rstrip(".")


while True:
    print("\nChoose an option:")
    print("1. Convert Cartesian to Polar")
    print("2. Exit")

    choice = input("Enter your choice (1-2): ").strip()

    if choice == "2":
        print("\nThanks for using Coordinate to Polar Transformation! ✨")
        break

    if choice != "1":
        print("❌ Please choose 1 or 2.")
        continue

    try:
        x = float(input("Enter x coordinate: ").strip())
        y = float(input("Enter y coordinate: ").strip())
    except ValueError:
        print("❌ Invalid input. Please enter numeric values.")
        continue

    radius = math.hypot(x, y)
    theta_rad = math.atan2(y, x)
    theta_deg = math.degrees(theta_rad)

    if theta_deg < 0:
        theta_deg += 360

    quadrant = "Origin"
    if x > 0 and y > 0:
        quadrant = "Quadrant I"
    elif x < 0 and y > 0:
        quadrant = "Quadrant II"
    elif x < 0 and y < 0:
        quadrant = "Quadrant III"
    elif x > 0 and y < 0:
        quadrant = "Quadrant IV"
    elif x == 0 and y != 0:
        quadrant = "Y-axis"
    elif y == 0 and x != 0:
        quadrant = "X-axis"

    print("\nResult")
    print("-" * 58)
    print(f"Cartesian form: ({format_number(x)}, {format_number(y)})")
    print(f"Polar form: r = {format_number(radius)}, theta = {format_number(theta_deg)} degrees")
    print(f"Theta in radians: {format_number(theta_rad)}")
    print(f"Location: {quadrant}")
    print("-" * 58)
