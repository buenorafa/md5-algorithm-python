import hashlib
from md5 import MD5


# Function to compare the results
def test_md5_implementation(strings):
    for s in strings:
        # Using hashlib
        hashlib_md5 = hashlib.md5(s.encode()).hexdigest()

        # Using my implementation
        my_md5 = MD5.digest(s)

        # Comparing the results
        print(f"String: {s}")
        print(f"hashlib MD5: {hashlib_md5}")
        print(f"My MD5:      {my_md5}")
        print(f"Match:       {hashlib_md5 == my_md5}")
        print("-" * 50)


# Test strings
test_strings = ["hello", "world", "OpenAI", "IFPB", "Seguranca de Dados"]

# Testing
test_md5_implementation(test_strings)
