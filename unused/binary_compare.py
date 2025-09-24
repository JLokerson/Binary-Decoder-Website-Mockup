def binary_to_text(binary_str):
    chars = []
    for b in binary_str.split():
        try:
            chars.append(chr(int(b, 2)))
        except:
            chars.append('?')
    return ''.join(chars)

def read_file(path):
    with open(path, 'r', encoding='utf-8') as f:
        return f.read()

def compare_text(decoded, reference):
    import difflib
    diff = difflib.unified_diff(reference.splitlines(), decoded.splitlines(), lineterm='')
    return '\n'.join(diff)

if __name__ == "__main__":
    binary_data = read_file("binary-output.txt")
    will_text = read_file("will text.txt")
    decoded_text = binary_to_text(binary_data)
    print("Decoded Text:\n", decoded_text)
    print("\nComparison to Will Document:\n")
    print(compare_text(decoded_text, will_text))
