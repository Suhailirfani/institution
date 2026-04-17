"""
Fix corrupted CSS file: lines after 853 contain UTF-16 null-byte encoding.
This script reads the file, strips null bytes from the corrupted section,
and rewrites it cleanly.
"""

with open(r'd:\work\adabiyya\static\css\custom.css', 'rb') as f:
    raw = f.read()

# Decode full file as latin-1 to preserve all bytes
content = raw.decode('latin-1')

# Find the boundary - the clean section ends at the } after @media (max-width: 375px)
# We'll split by finding the null byte corruption start
lines = content.split('\r\n')

clean_lines = []
corrupt_started = False

for line in lines:
    if '\x00' in line:
        # This line has null bytes - strip them and add clean version
        if not corrupt_started:
            corrupt_started = True
        clean_line = line.replace('\x00', '')
        if clean_line.strip():  # Only keep non-empty lines
            clean_lines.append(clean_line)
    else:
        clean_lines.append(line)

clean_content = '\r\n'.join(clean_lines)

with open(r'd:\work\adabiyya\static\css\custom.css', 'w', encoding='utf-8') as f:
    f.write(clean_content)

print(f"Done. File cleaned. Total lines: {len(clean_lines)}")
