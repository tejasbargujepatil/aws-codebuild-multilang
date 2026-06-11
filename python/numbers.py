numbers = [45, 12, 78, 3, 56, 89, 23, 67, 34, 91]

highest = max(numbers)
lowest  = min(numbers)
average = sum(numbers) / len(numbers)

print("=" * 40)
print("        PYTHON NUMBER ANALYSIS")
print("=" * 40)
print(f"Numbers : {numbers}")
print(f"Highest : {highest}")
print(f"Lowest  : {lowest}")
print(f"Average : {average:.2f}")
print("=" * 40)
