import re

def is_luxury_request(text: str) -> bool:
    if not text:
        return False
    for match in re.finditer(r"\b(lux(?:ury)?|fancy)\b", text, re.IGNORECASE):
        before = text[: match.start()].rstrip()
        last_word = before.split()[-1].lower() if before.split() else ""
        if last_word in ("no", "non", "jangan"):
            continue
        return True
    return False

cases = [
    ("WTB lux bag",           True),
    ("WTB luxury watch",      True),
    ("WTB fancy shoes",       True),
    ("WTB LUX item",          True),
    ("WTB no lux",            False),
    ("WTB non luxury",        False),
    ("WTB jangan lux",        False),
    ("WTB baju biasa",        False),
    ("WTB Jangan Lux please", False),
    ("WTB non-lux bag",       True),   # hyphen, not a space — treated as match
]

all_passed = True
for text, expected in cases:
    result = is_luxury_request(text)
    status = "PASS" if result == expected else "FAIL"
    if status == "FAIL":
        all_passed = False
    print(f"[{status}] '{text}' → expected {expected}, got {result}")

print()
print("All passed!" if all_passed else "Some tests failed — check the FAIL lines above.")
