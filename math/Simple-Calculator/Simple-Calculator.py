class Calculator:
    def __init__(self):
        pass 

    def start_calculation(self):
        print("--------Menu---------")
        print('1. Addition')
        print('2. Subtraction')
        print('3. Multiplication')
        print('4. Division')
        print('5. Modulus')
        print('6. Floor Division')
        print('7. Power')
        print('8. Factorial')
        print('9. Square root')
        print('10. Exit')

        while True:
            try:
                user_input = int(input('Enter your choice to calculate(1-10): '))
                if user_input == 1:
                    self.addition()
                elif user_input == 2:
                    self.substraction()
                elif user_input == 3:
                    self.multiplication()
                elif user_input == 4:
                    self.division()
                elif user_input == 5:
                    self.modulus()
                elif user_input == 6:
                    self.floor_division()
                elif user_input == 7:
                    self.power()
                elif user_input == 8:
                    self.factorial()
                elif user_input == 9:
                    self.sqrt()
                elif user_input == 10:
                    print('Goodbye! Have a good day.')
                    break
                else:
                    print('Wrong Choice.')

            except ValueError:
                print('please enter correct option.')
            except ZeroDivisionError:
                print('Zero cannot be divided by zero.')
            except Exception as e:
                print(f'Something went wrong: {e}')

    def addition(self):
        a = int(input('enter first value: '))
        b = int(input('enter second value: '))
        add = a + b
        print(f'The Result is: {add}')
    
    def substraction(self):
        a = int(input('enter first value: '))
        b = int(input('enter second value: '))
        minus = a - b
        print(f'The Result is: {minus}')

    def division(self):
        a = int(input('enter first value: '))
        b = int(input('enter second value: '))
        div = a / b
        print(f'The Result is: {div}')
    
    def multiplication(self):
        a = int(input('enter first value: '))
        b = int(input('enter second value: '))
        multiplication = a * b
        print(f'The Result is: {multiplication}')

    def floor_division(self):
        a = int(input('enter first value: '))
        b = int(input('enter second value: '))
        floor = a // b
        print(f'The Result is: {floor}')

    def modulus(self):
        a = int(input('enter first value: '))
        b = int(input('enter second value: '))
        mod = a % b
        print(f'The Result is: {mod}')

    def power(self):
        a = int(input('enter first value: '))
        b = int(input('enter second value: '))
        power = a ** b
        print(f'The Result is: {power}')

    def factorial(self):
        a = int(input("Enter the number: "))
        fact = 1
        for i in range(1,a+1):
            fact = fact * i
        print(f"Factorial is: {fact}")
    
    def sqrt(self):
        num = int(input("Enter the number: "))
        sqrt = num ** 0.5
        print(f"Square root of {num} : {sqrt}")



cal = Calculator()
cal.start_calculation()
