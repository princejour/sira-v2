from pathlib import Path
import re

STAMP = 'SIRA_V2_EMPTY_IMPORT_ON_INSTALL_20260613_03'


def inject_empty_guard(html_text: str) -> str:
    guard_lines = [
        '<script>',
        '(function(){',
        f"  var stamp = '{STAMP}';",
        "  var stampKey = '__sira_v2_empty_import_stamp__';",
        '  function clearOnceAfterInstall(){',
        '    try{',
        '      if(localStorage.getItem(stampKey) !== stamp){',
        '        localStorage.clear();',
        '        sessionStorage.clear();',
        '        localStorage.setItem(stampKey, stamp);',
        "        localStorage.setItem('personalClasses', '{}');",
        "        localStorage.setItem('importedPersonalClasses', '{}');",
        "        localStorage.setItem('studentInfoRecords', '[]');",
        "        localStorage.setItem('importedStudentInfoRecords', '[]');",
        '      }',
        '    }catch(e){}',
        '  }',
        '  function removeDefaultClassOptions(){',
        '    try{',
        r"      var forbidden = /8\s*أساسي\s*(6|7|8|9)|الصف\s*العاشر|تجريبي|افتراضي/i;",
        "      document.querySelectorAll('option').forEach(function(opt){",
        "        var text = (opt.textContent || '') + ' ' + (opt.value || '');",
        '        if(forbidden.test(text)) opt.remove();',
        '      });',
        "      document.querySelectorAll('[data-class], .class-card, .student-row, .student-item').forEach(function(el){",
        "        var text = el.textContent || '';",
        '        if(forbidden.test(text)) el.remove();',
        '      });',
        '    }catch(e){}',
        '  }',
        '  clearOnceAfterInstall();',
        '  window.__SIRA_V2_EMPTY_IMPORT_ONLY__ = true;',
        "  window.addEventListener('DOMContentLoaded', removeDefaultClassOptions);",
        "  window.addEventListener('load', function(){ setTimeout(removeDefaultClassOptions, 300); setTimeout(removeDefaultClassOptions, 1200); });",
        '})();',
        '</script>',
    ]
    guard = '\n'.join(guard_lines)
    if STAMP in html_text:
        return html_text
    if re.search(r'<head[^>]*>', html_text, flags=re.I):
        return re.sub(r'(<head[^>]*>)', r'\1' + guard, html_text, count=1, flags=re.I)
    return guard + html_text


def patch_app_html(path: Path) -> bool:
    s = path.read_text(encoding='utf-8', errors='ignore')
    original = s

    s = re.sub(
        r'<option\s+value="9">\s*8\s*أساسي\s*9\s*</option>\s*<option\s+value="8">\s*8\s*أساسي\s*8\s*</option>\s*<option\s+value="7">\s*8\s*أساسي\s*7\s*</option>\s*<option\s+value="6">\s*8\s*أساسي\s*6\s*</option>',
        '',
        s,
        flags=re.I,
    )

    s = s.replace(
        'const ORIGINAL_DEFAULT_CLASSES = JSON.parse(JSON.stringify(data));',
        'const ORIGINAL_DEFAULT_CLASSES = {};\nObject.keys(data).forEach(k => delete data[k]);',
    )

    s = re.sub(
        r'function replaceDataWithPersonalClasses\(\)\{.*?\n\}\nfunction getClassLabel',
        '''function replaceDataWithPersonalClasses(){
    const personal = getPersonalClasses();
    Object.keys(data).forEach(k => delete data[k]);
    Object.keys(personal || {}).forEach(k => {
        if(!Array.isArray(personal[k]) || personal[k].length === 0) return;
        const classKey = normalizeClassNameForStorage(k);
        if(!data[classKey]) data[classKey] = [];
        personal[k].forEach(studentName => {
            if(studentName && !data[classKey].includes(studentName)) data[classKey].push(studentName);
        });
    });
    applyStudentRenamesToData();
}
function getClassLabel''',
        s,
        flags=re.S,
    )

    s = re.sub(
        r'function saveImportedPersonalClasses\(personal\)\{.*?\n\}\nfunction importPersonalClassesFile',
        '''function saveImportedPersonalClasses(personal){
    const keys = Object.keys(personal || {});
    if(keys.length === 0){
        showToast('لم يتم العثور على أقسام وتلاميذ داخل الملف. تأكد من وجود عمود: القسم وعمود: اسم التلميذ','info');
        return;
    }
    const saved = {};
    keys.forEach(className => {
        if(!Array.isArray(personal[className])) return;
        const classKey = normalizeClassNameForStorage(className);
        if(!saved[classKey]) saved[classKey] = [];
        personal[className].forEach(studentName => {
            if(studentName && !saved[classKey].includes(studentName)) saved[classKey].push(studentName);
        });
    });
    savePersonalClasses(saved);
    saveImportedStudentInfoRecords();
    replaceDataWithPersonalClasses();
    refreshClassSelectOptions(Object.keys(saved)[0] || '');
    resetDashboard();
    renderStudentsList();
    renderPersonalClassesList();
    clearImportedClassesFile();
    showToast('تم استبدال كل الأقسام القديمة بالأقسام المستوردة فقط','success');
}
function importPersonalClassesFile''',
        s,
        flags=re.S,
    )

    s = s.replace(
        'setTimeout(autoRestoreWhenEmpty, 1400);',
        '// Auto restore disabled in empty-import build\n    // setTimeout(autoRestoreWhenEmpty, 1400);',
    )

    s = inject_empty_guard(s)

    if s != original:
        path.write_text(s, encoding='utf-8')
        return True
    return False


def bump_gradle_version(root: Path) -> None:
    for gf in list(root.rglob('build.gradle')) + list(root.rglob('build.gradle.kts')):
        s = gf.read_text(encoding='utf-8', errors='ignore')
        original = s
        if gf.parent.name == 'app':
            s = re.sub(r'versionCode\s+\d+', 'versionCode 202', s)
            s = re.sub(r'versionCode\s*=\s*\d+', 'versionCode = 202', s)
            s = re.sub(r'versionName\s+"[^"]+"', 'versionName "empty-import-v2"', s)
            s = re.sub(r'versionName\s*=\s*"[^"]+"', 'versionName = "empty-import-v2"', s)
            s = re.sub(r"versionName\s+'[^']+'", "versionName 'empty-import-v2'", s)
        if s != original:
            gf.write_text(s, encoding='utf-8')
            print('Updated Gradle version:', gf)


def main() -> None:
    root = Path('.')
    patched = 0
    for html in root.rglob('*.html'):
        if patch_app_html(html):
            patched += 1
            print('Patched HTML:', html)

    if patched == 0:
        raise SystemExit('No HTML file was patched; cannot guarantee empty startup')

    bump_gradle_version(root)


if __name__ == '__main__':
    main()
