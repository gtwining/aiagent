import os
from functions.get_file_content import get_file_content
from config import MAX_CHARS

def test_runner():
    # 1. Test the Lorem Ipsum truncation logic
    print("Testing get_file_content(\"calculator\", \"lorem.txt\"):")
    lorem_result = get_file_content("calculator", "lorem.txt")
    
    # Validation logic for the large file
    if f"truncated at {MAX_CHARS} characters" in lorem_result:
        print(f"  Result: Success (File truncated correctly)")
        print(f"  Length: {len(lorem_result)} characters")
        # Print just the footer to show the truncation message
        print(f"  Footer: ...{lorem_result[-70:]}")
    else:
        print(f"  Result: {lorem_result}")
    print("-" * 40)

    # 2. Test standard and security cases
    test_cases = [
        ("main.py", "Result for main.py:"),
        ("pkg/calculator.py", "Result for pkg/calculator.py:"),
        ("/bin/cat", "Result for /bin/cat (Security Test):"),
        ("pkg/does_not_exist.py", "Result for missing file:")
    ]

    for path, label in test_cases:
        print(f"get_file_content(\"calculator\", \"{path}\"):")
        print(f"  {label}")
        content = get_file_content("calculator", path)
        
        # Indent the output for readability
        indented = "\n".join(f"    {line}" for line in content.splitlines())
        print(indented)
        print()

if __name__ == "__main__":
    test_runner()
