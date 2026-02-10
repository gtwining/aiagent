from functions.write_file import write_file

def run_tests():
    test_cases = [
        # (label, working_dir, file_path, content)
        ("Overwrite existing file", "calculator", "lorem.txt", "wait, this isn't lorem ipsum"),
        ("Nested directory write", "calculator", "pkg/morelorem.txt", "lorem ipsum dolor sit amet"),
        ("Security breach", "calculator", "/tmp/temp.txt", "this should not be allowed")
    ]

    for label, wd, fp, content in test_cases:
        print(f"--- Test: {label} ---")
        print(f"Calling: write_file(\"{wd}\", \"{fp}\", ...)")
        result = write_file(wd, fp, content)
        print(f"Result: {result}\n")

if __name__ == "__main__":
    run_tests()