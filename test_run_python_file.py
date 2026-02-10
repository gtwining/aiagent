from functions.run_python_file import run_python_file

def run_tests():
    test_cases = [
        ("Usage instructions", "calculator", "main.py", None),
        ("Actual calculation", "calculator", "main.py", ["3 + 5"]),
        ("Internal tests", "calculator", "tests.py", None),
        ("Security breach", "calculator", "../main.py", None),
        ("Missing file", "calculator", "nonexistent.py", None),
        ("Wrong file type", "calculator", "lorem.txt", None)
    ]

    for label, wd, fp, args in test_cases:
        print(f"--- Test: {label} ---")
        print(f"Calling: run_python_file(\"{wd}\", \"{fp}\", args={args})")
        result = run_python_file(wd, fp, args)
        print(result)
        print("-" * 40 + "\n")

if __name__ == "__main__":
    run_tests()
