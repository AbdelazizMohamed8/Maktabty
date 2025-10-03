# fix_encoding.py
import os

ROOT = os.path.abspath(".")
EXTS = (".py", ".html", ".css", ".txt", ".json")  # اضافة امتدادات لو حابب

candidates = []
for dirpath, dirnames, filenames in os.walk(ROOT):
    # تتجاهل فولدرات النسخ الاحتياطي أو venv
    if any(part.lower().startswith("backup_") or part.lower() == "venv" for part in dirpath.split(os.sep)):
        continue
    for fn in filenames:
        if fn.lower().endswith(EXTS):
            candidates.append(os.path.join(dirpath, fn))

enc_tried = ["utf-8", "utf-16", "utf-16-le", "utf-16-be", "cp1252", "iso-8859-1"]

fixed = []
failed = []

for path in candidates:
    with open(path, "rb") as f:
        data = f.read()
    # try utf-8 first
    try:
        data.decode("utf-8")
        # already valid utf-8
        continue
    except Exception:
        pass
    # try other encodings and convert
    converted = None
    for enc in enc_tried[1:]:
        try:
            text = data.decode(enc)
            converted = text
            used = enc
            break
        except Exception:
            converted = None
    if converted is None:
        failed.append(path)
    else:
        # write back as utf-8 (without BOM)
        try:
            with open(path, "w", encoding="utf-8") as fw:
                fw.write(converted)
            fixed.append((path, used))
        except Exception as e:
            failed.append((path, str(e)))

print("=== Conversion summary ===")
print(f"Files scanned: {len(candidates)}")
print(f"Fixed: {len(fixed)}")
for p, enc in fixed[:50]:
    print(f"  fixed: {p}  (from {enc})")
if failed:
    print(f"Failed to convert {len(failed)} files:")
    for item in failed[:50]:
        print(" ", item)
else:
    print("No failures.")
