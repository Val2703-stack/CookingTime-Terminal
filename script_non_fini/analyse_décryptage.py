import base64
import zlib
import gzip
import binascii



def fix_base64_padding(b64_string):
    return b64_string + '=' * ((4 - len(b64_string) % 4) % 4)

data_b64 = """AUkefzSE6JTuitn/+swEdVLznYLC5inYxvbRzwCZP8LC0eMoUcr1CduB8fxK3R/J4oitsXzRjgW/g/Mv1nk6JSX9XbQjbv8tj9KtUjwpYh1HdfbJ2gdT47dl0TgG+3OS0MAEMIA"""
data_b64 = fix_base64_padding(data_b64)
data_bytes = base64.b64decode(data_b64)

print("========== RAW HEX ==========")
print(binascii.hexlify(data_bytes))

print("\n========== AS UTF-8 ==========")
try:
    print(data_bytes.decode('utf-8'))
except Exception as e:
    print(f"Impossible de décoder en utf-8: {e}")

print("\n========== ZLIB DECOMPRESSION ==========")
try:
    print(zlib.decompress(data_bytes))
except Exception as e:
    print(f"Zlib error: {e}")

print("\n========== GZIP DECOMPRESSION ==========")
try:
    print(gzip.decompress(data_bytes))
except Exception as e:
    print(f"Gzip error: {e}")

# Affichage sous forme brute (bytes)
print("\n========== RAW BYTES ==========")
print(data_bytes)

print("\n========== HEX (lisible) ==========")
print(' '.join(f'{b:02x}' for b in data_bytes))

print("\n========== Tentative recherche JSON ==========")
try:
    s = data_bytes.decode('utf-8')
    import json
    d = json.loads(s)
    print(d)
except Exception as e:
    print(f"JSON error: {e}")

# Ajoute d'autres essais si besoin (brotli, lzma, etc.)
