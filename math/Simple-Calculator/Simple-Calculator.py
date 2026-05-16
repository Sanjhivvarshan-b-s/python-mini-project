print("🧮 Simple Calculator 🧮")
print("Perform basic arithmetic operations\n")

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
    print("7️⃣  Show History")
    print("8️⃣  Exit")
    print("=" * 40)
    
    choice = input("\n🎯 Enter your choice (1-8): ")
    
    if choice == '8':
        print("\n👋 Thanks for using the calculator! Goodbye!\n")
        break

    elif choice == '7':
        print("\n📜 Calculation History:\n")
        
        if len(history) == 0:
            print("📭 No calculations found in history.\n")
        else:
            for item in history:
                print(f"➡️  {item}")
            print()
    
    elif choice in ['1', '2', '3', '4', '5', '6']:
        try:
            num1 = float(input("\n📥 Enter first number: "))
            num2 = float(input("📥 Enter second number: "))
            
            if choice == '1':
                result = num1 + num2
                calculation = f"{num1} + {num2} = {result}"
                history.append(calculation)
                print(f"\n✨ Result: {calculation}\n")
            
            elif choice == '2':
                result = num1 - num2
                calculation = f"{num1} - {num2} = {result}"
                history.append(calculation)
                print(f"\n✨ Result: {calculation}\n")
            
            elif choice == '3':
                result = num1 * num2
                calculation = f"{num1} × {num2} = {result}"
                history.append(calculation)
                print(f"\n✨ Result: {calculation}\n")
            
            elif choice == '4':
                if num2 == 0:
                    print("\n❌ Error! Division by zero is not allowed.\n")
                else:
                    result = num1 / num2
                    calculation = f"{num1} ÷ {num2} = {result}"
                    history.append(calculation)
                    print(f"\n✨ Result: {calculation}\n")
            
            elif choice == '5':
                if num2 == 0:
                    print("\n❌ Error! Modulus by zero is not allowed.\n")
                else:
                    result = num1 % num2
                    calculation = f"{num1} % {num2} = {result}"
                    history.append(calculation)
                    print(f"\n✨ Result: {calculation}\n")
            
            elif choice == '6':
                result = num1 ** num2
                calculation = f"{num1} ^ {num2} = {result}"
                history.append(calculation)
                print(f"\n✨ Result: {calculation}\n")
        
        except ValueError:
            print("\n❌ Invalid input! Please enter valid numbers.\n")
    
    else:
        print("\n❌ Invalid choice! Please select 1-8.\n")