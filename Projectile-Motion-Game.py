import math
import random
import sys
import time

try:
    import numpy as np
    import matplotlib.pyplot as plt
except ImportError:
    print("❌ This project requires numpy and matplotlib.")
    print("Install them using: pip install numpy matplotlib")
    sys.exit(1)


GRAVITY = 9.81


def get_float(prompt, min_value=None, max_value=None):
    while True:
        raw_value = input(prompt).strip()
        try:
            value = float(raw_value)
            if min_value is not None and value < min_value:
                print(f"⚠️ Enter a value greater than or equal to {min_value}.")
                continue
            if max_value is not None and value > max_value:
                print(f"⚠️ Enter a value less than or equal to {max_value}.")
                continue
            return value
        except ValueError:
            print("⚠️ Invalid number. Try again.")


def get_int(prompt, min_value=None, max_value=None):
    while True:
        raw_value = input(prompt).strip()
        try:
            value = int(raw_value)
            if min_value is not None and value < min_value:
                print(f"⚠️ Enter a value greater than or equal to {min_value}.")
                continue
            if max_value is not None and value > max_value:
                print(f"⚠️ Enter a value less than or equal to {max_value}.")
                continue
            return value
        except ValueError:
            print("⚠️ Invalid integer. Try again.")


def projectile_stats(speed, angle_deg):
    angle_rad = math.radians(angle_deg)
    flight_time = (2 * speed * math.sin(angle_rad)) / GRAVITY
    max_height = (speed ** 2 * (math.sin(angle_rad) ** 2)) / (2 * GRAVITY)
    horizontal_range = (speed ** 2 * math.sin(2 * angle_rad)) / GRAVITY
    return flight_time, max_height, horizontal_range


def trajectory_points(speed, angle_deg, point_count=350):
    flight_time, _, _ = projectile_stats(speed, angle_deg)
    if flight_time <= 0:
        return np.array([0.0]), np.array([0.0]), flight_time

    angle_rad = math.radians(angle_deg)
    t = np.linspace(0, flight_time, point_count)
    x = speed * math.cos(angle_rad) * t
    y = speed * math.sin(angle_rad) * t - 0.5 * GRAVITY * (t ** 2)
    y = np.maximum(y, 0)
    return x, y, flight_time


def show_plot(x, y, target_x=None, target_radius=3.0):
    plt.figure(figsize=(10, 6))
    plt.plot(x, y, color="#0078D7", linewidth=2.2, label="Projectile Path")
    plt.scatter([x[-1]], [0], color="#D7263D", s=70, label="Landing Point")

    if target_x is not None:
        plt.scatter([target_x], [0], color="#2E8B57", s=80, marker="*", label="Target")
        plt.axvspan(target_x - target_radius, target_x + target_radius, alpha=0.15, color="#2E8B57")

    plt.title("Projectile Motion Simulator")
    plt.xlabel("Horizontal Distance (m)")
    plt.ylabel("Vertical Height (m)")
    plt.grid(alpha=0.3)
    plt.ylim(bottom=0)
    plt.xlim(left=0)
    plt.legend()
    plt.tight_layout()
    plt.show()


def run_practice_mode():
    print("\n🎯 Practice Mode")
    speed = get_float("Enter launch speed (m/s): ", min_value=1)
    angle = get_float("Enter launch angle (degrees 1-89): ", min_value=1, max_value=89)

    print("\n⏳ Simulating trajectory...")
    time.sleep(0.6)

    x, y, _ = trajectory_points(speed, angle)
    flight_time, max_height, horizontal_range = projectile_stats(speed, angle)

    print("\n📊 Results")
    print(f"- Flight Time: {flight_time:.2f} s")
    print(f"- Maximum Height: {max_height:.2f} m")
    print(f"- Horizontal Range: {horizontal_range:.2f} m")

    show_plot(x, y)


def run_target_challenge():
    print("\n🎮 Target Challenge")
    attempts = get_int("How many attempts do you want? (1-10): ", min_value=1, max_value=10)
    target_x = random.uniform(30, 180)
    hit_radius = 3.0

    print(f"\n🎯 Target is placed at {target_x:.2f} m")
    print(f"✅ Hit zone: ±{hit_radius} m")

    success = False
    for turn in range(1, attempts + 1):
        print(f"\n--- Attempt {turn}/{attempts} ---")
        speed = get_float("Enter launch speed (m/s): ", min_value=1)
        angle = get_float("Enter launch angle (degrees 1-89): ", min_value=1, max_value=89)

        x, y, _ = trajectory_points(speed, angle)
        landing_x = x[-1]
        error = landing_x - target_x

        print(f"Landing Distance: {landing_x:.2f} m")
        if abs(error) <= hit_radius:
            print("🎉 Direct hit! You nailed the target!")
            show_plot(x, y, target_x=target_x, target_radius=hit_radius)
            success = True
            break

        direction = "short" if error < 0 else "long"
        print(f"❌ Missed! Your shot was {abs(error):.2f} m too {direction}.")
        show_plot(x, y, target_x=target_x, target_radius=hit_radius)

    if not success:
        print("\n🏁 Challenge Over")
        print(f"Target was at {target_x:.2f} m. Better luck next round!")


def main():
    print("🚀 Welcome to Projectile Motion Game 🚀")
    print("Physics + fun with trajectory plotting\n")

    while True:
        print("Choose an option:")
        print("1) Practice Mode")
        print("2) Target Challenge")
        print("3) Exit")

        choice = input("Enter choice (1-3): ").strip()

        if choice == "1":
            run_practice_mode()
        elif choice == "2":
            run_target_challenge()
        elif choice == "3":
            print("👋 Exiting... See you next launch!")
            sys.exit(0)
        else:
            print("⚠️ Invalid choice. Please pick 1, 2, or 3.\n")


if __name__ == "__main__":
    main()