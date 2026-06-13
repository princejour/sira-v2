from pathlib import Path
import re

MARK = "SIRA_V2_FIREBASE_ALL_IMPORTED_CLASSES_FIX"


def patch_html(path: Path) -> bool:
    text = path.read_text(encoding="utf-8", errors="ignore")
    if MARK in text:
        return False
    original = text
    injection = """
    // SIRA_V2_FIREBASE_ALL_IMPORTED_CLASSES_FIX
    try{
        localStorage.setItem('importedPersonalClasses', JSON.stringify(saved));
        localStorage.setItem('personalClasses', JSON.stringify(saved));
        window.__SIRA_V2_ALL_IMPORTED_CLASSES__ = saved;
    }catch(e){}
"""
    text = re.sub(
        r"(savePersonalClasses\(saved\);)",
        r"\1" + injection,
        text,
        count=1,
    )
    text = re.sub(
        r"(saveImportedStudentInfoRecords\(\);)",
        "if(window.__siraV2NormalizeStudentInfoNow) window.__siraV2NormalizeStudentInfoNow();\n    "
        "if(window.__siraV2SyncImportedClassStoresNow) window.__siraV2SyncImportedClassStoresNow();\n    "
        r"\1",
        text,
        count=1,
    )
    if text != original:
        path.write_text(text, encoding="utf-8")
        print("Patched Firebase all-classes upload:", path)
        return True
    return False


def main() -> None:
    patched = 0
    for html in Path('.').rglob('*.html'):
        if patch_html(html):
            patched += 1
    if patched == 0:
        print("No Firebase upload all-classes patch was applied")


if __name__ == "__main__":
    main()
