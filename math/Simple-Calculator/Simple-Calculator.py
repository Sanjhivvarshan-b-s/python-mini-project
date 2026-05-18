import math

print("🧮 Simple Scientific Calculator 🧮")
print("Perform arithmetic and scientific operations\n")

history = []

while True:
    print("=" * 40)
    print("📋 Choose an operation:")
    print("1️⃣  Addition (+)")
    print("2️⃣  Subtraction (-)")
    print("3️⃣  Multiplication (×)")
    print("4️⃣  Division (÷)")
    print("5️⃣  Modulus (%)")
    print("6️⃣  Power (^)")
    print("7️⃣  Square Root (√)")
    print("8️⃣  Sine (sin)")
    print("9️⃣  Cosine (cos)")
    print("🔟 Tangent (tan)")
    print("1️⃣1️⃣ Logarithm (log10)")
    print("1️⃣2️⃣ Natural Log (ln)")
    print("1️⃣3️⃣ Show History")
    print("1️⃣4️⃣ Exit")
    print("=" * 40)

    choice = input("\n🎯 Enter your choice (1-14): ")

    # Exit
    if choice == '14':
        print("\n👋 Thanks for using the calculator! Goodbye!\n")
        break

    # Show history
    elif choice == '13':
        print("\n📜 Calculation History:\n")

        if len(history) == 0:
            print("📭 No calculations found in history.\n")
        else:
            for item in history:
                print(f"➡️  {item}")
            print()

    # Basic arithmetic operations (require two numbers)
    elif choice in ['1', '2', '3', '4', '5', '6']:
        try:
            num1 = float(input("\n📥 Enter first number: "))
            num2 = float(input("📥 Enter second number: "))

            if choice == '1':
                result = num1 + num2
                calculation = f"{num1} + {num2} = {result}"

            elif choice == '2':
                result = num1 - num2
                calculation = f"{num1} - {num2} = {result}"

            elif choice == '3':
                result = num1 * num2
                calculation = f"{num1} × {num2} = {result}"

            elif choice == '4':
                if num2 == 0:
                    print("\n❌ Error! Division by zero is not allowed.\n")
                    continue
                result = num1 / num2
                calculation = f"{num1} ÷ {num2} = {result}"

            elif choice == '5':
                if num2 == 0:
                    print("\n❌ Error! Modulus by zero is not allowed.\n")
                    continue
                result = num1 % num2
                calculation = f"{num1} % {num2} = {result}"

            elif choice == '6':
                result = num1 ** num2
                calculation = f"{num1} ^ {num2} = {result}"

            history.append(calculation)
            print(f"\n✨ Result: {calculation}\n")

        except ValueError:
            print("\n❌ Invalid input! Please enter valid numbers.\n")

    # Scientific operations (require one number)
    elif choice in ['7', '8', '9', '10', '11', '12']:
        try:
            num = float(input("\n📥 Enter a number: "))

            if choice == '7':  # Square Root
                if num < 0:
                    print("\n❌ Error! Cannot calculate square root of a negative number.\n")
                    continue
                result = math.sqrt(num)
                calculation = f"√{num} = {result}"

            elif choice == '8':  # Sine
                result = math.sin(math.radians(num))
                calculation = f"sin({num}°) = {result}"

            elif choice == '9':  # Cosine
                result = math.cos(math.radians(num))
                calculation = f"cos({num}°) = {result}"

            elif choice == '10':  # Tangent
                result = math.tan(math.radians(num))
                calculation = f"tan({num}°) = {result}"

            elif choice == '11':  # Log base 10
                if num <= 0:
                    print("\n❌ Error! Logarithm is only defined for positive numbers.\n")
                    continue
                result = math.log10(num)
                calculation = f"log10({num}) = {result}"

            elif choice == '12':  # Natural Log
                if num <= 0:
                    print("\n❌ Error! Natural logarithm is only defined for positive numbers.\n")
                    continue
                result = math.log(num)
                calculation = f"ln({num}) = {result}"

            history.append(calculation)
            print(f"\n✨ Result: {calculation}\n")

        except ValueError:
            print("\n❌ Invalid input! Please enter a valid number.\n")

    else:
        print("\n❌ Invalid choice! Please select 1-14.\n")