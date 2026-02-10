import os
from get_files_info import get_files_info

def run_tests():

    tests = [
    ("current directory", "../calculator", "."),
    ("'pkg' directory", "../calculator", "pkg"),
    ("'/bin' directory", "../calculator", "/bin"),
    ("'../' directory", "../calculator", "../")
]

    for label, wd, target in tests:
        print(f"get_files_info(\"{wd}\", \"{target}\"):")
        print(f"  Result for {label}:")
        
        result = get_files_info(wd, target)
        
        
        indented_result = "\n".join(f"    {line}" for line in result.splitlines())
        print(indented_result)
        print() 
if __name__ == "__main__":
    run_tests()
