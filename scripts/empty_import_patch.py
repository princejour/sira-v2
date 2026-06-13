from pathlib import Path
import re

STAMP = 'SIRA_V2_RICH_IMPORT_CARD_OK_CLASSES_STORE_SYNC_20260613_01'

RICH_IMPORT_JS = r'''
<script>
(function(){
  function norm(s){return String(s||'').replace(/[\u064B-\u065F\u0670]/g,'').replace(/[أإآ]/g,'ا').replace(/ة/g,'ه').replace(/ى/g,'ي').replace(/\s+/g,'').toLowerCase();}
  function findIndex(headers, aliases){var hh=headers.map(norm);for(var a=0;a<aliases.length;a++){var n=norm(aliases[a]);for(var i=0;i<hh.length;i++){if(hh[i]===n||hh[i].indexOf(n)>=0||n.indexOf(hh[i])>=0)return i;}}return -1;}
  function cell(row,i){return i>=0?String(row[i]||'').trim():'';}
  function makeRecord(cls,name,uid,bdate,bplace,father){bplace=(bplace||'').trim()||'تونس';father=(father||'').trim();return {'القسم':cls,'className':cls,'class':cls,'اسم التلميذ':name,'الاسم واللقب':name,'name':name,'studentName':name,'المعرف الوحيد':uid,'معرف وحيد':uid,'uniqueId':uid,'studentId':uid,'identifiantUnique':uid,'تاريخ الولادة':bdate,'birthDate':bdate,'dateNaissance':bdate,'مكان الولادة':bplace,'مكانها':bplace,'مكان الميلاد':bplace,'مكان الازدياد':bplace,'birthPlace':bplace,'placeOfBirth':bplace,'lieuNaissance':bplace,'اسم الأب':father,'اسم الاب':father,'الأب':father,'الاب':father,'fatherName':father,'father':father,'nomPere':father,'الولي':father,'اسم الولي':father,'ولي الأمر':father,'اسم ولي الأمر':father,'guardianName':father,'guardian':father,'parentName':father,'tuteur':father};}
  function parseRichTable(aoa){if(!aoa||!aoa.length)return null;var h=(aoa[0]||[]).map(function(x){return String(x||'').trim();});var ic=findIndex(h,['القسم','قسم','class','classe']);var iname=findIndex(h,['اسم التلميذ','الاسم واللقب','الإسم واللقب','اسم ولقب','الاسم','name','studentName']);if(ic<0||iname<0)return null;var iid=findIndex(h,['المعرف الوحيد','معرف وحيد','uniqueId','identifiant unique','id unique']);var ib=findIndex(h,['تاريخ الولادة','تاريخ الميلاد','date naissance','birthDate']);var ip=findIndex(h,['مكان الولادة','مكان الميلاد','مكان الازدياد','مكانها','lieu naissance','birthPlace','placeOfBirth']);var ifa=findIndex(h,['اسم الأب','اسم الاب','الأب','الاب','fatherName','nom pere','pere']);var personal={},records=[];for(var r=1;r<aoa.length;r++){var row=aoa[r]||[],cls=cell(row,ic),name=cell(row,iname);if(!cls||!name)continue;if(!personal[cls])personal[cls]=[];if(personal[cls].indexOf(name)<0)personal[cls].push(name);records.push(makeRecord(cls,name,cell(row,iid),cell(row,ib),cell(row,ip),cell(row,ifa)));}return Object.keys(personal).length?{personal:personal,records:records}:null;}
  function refresh(personal){try{if(typeof replaceDataWithPersonalClasses==='function')replaceDataWithPersonalClasses();}catch(e){}try{if(typeof refreshClassSelectOptions==='function')refreshClassSelectOptions(Object.keys(personal||{})[0]||'');}catch(e){}try{if(typeof resetDashboard==='function')resetDashboard();}catch(e){}try{if(typeof renderStudentsList==='function')renderStudentsList();}catch(e){}try{if(typeof renderPersonalClassesList==='function')renderPersonalClassesList();}catch(e){}try{if(typeof clearImportedClassesFile==='function')clearImportedClassesFile();}catch(e){}}
  function saveRich(parsed){var personal=parsed.personal,records=parsed.records||[];try{if(typeof savePersonalClasses==='function')savePersonalClasses(personal);}catch(e){}try{localStorage.setItem('personalClasses',JSON.stringify(personal));localStorage.setItem('importedPersonalClasses',JSON.stringify(personal));}catch(e){}var byName={},byClassName={};records.forEach(function(r){var n=r['الاسم واللقب'],c=r['القسم'];byName[n]=r;byClassName[c+'|'+n]=r;});['studentInfoRecords','importedStudentInfoRecords','personalStudentInfoRecords','studentsInfo','studentInfos'].forEach(function(k){try{localStorage.setItem(k,JSON.stringify(records));}catch(e){}});['studentInfoByName','studentInfosByName','studentCards','studentCardsByName','siraStudentInfo'].forEach(function(k){try{localStorage.setItem(k,JSON.stringify(byName));}catch(e){}});try{localStorage.setItem('studentInfoByClassAndName',JSON.stringify(byClassName));}catch(e){}refresh(personal);try{if(typeof showToast==='function')showToast('تم استيراد الأقسام ومعطيات بطاقة السيرة بنجاح','success');}catch(e){alert('تم استيراد الأقسام ومعطيات بطاقة السيرة بنجاح');}}
  function richImport(){var input=document.querySelector('input[type=file]'),file=input&&input.files&&input.files[0];if(!file||!window.XLSX)return false;var reader=new FileReader();reader.onload=function(ev){try{var wb=XLSX.read(ev.target.result,{type:'array'}),ws=wb.Sheets[wb.SheetNames[0]],aoa=XLSX.utils.sheet_to_json(ws,{header:1,raw:false,defval:''}),parsed=parseRichTable(aoa);if(parsed)saveRich(parsed);else if(window.__siraOriginalImportPersonalClassesFile)window.__siraOriginalImportPersonalClassesFile();}catch(err){if(window.__siraOriginalImportPersonalClassesFile)window.__siraOriginalImportPersonalClassesFile();}};reader.readAsArrayBuffer(file);return true;}
  function parseClasses(k){try{return JSON.parse(localStorage.getItem(k)||'{}');}catch(e){return {};}}
  function countClasses(o){if(!o||typeof o!=='object'||Array.isArray(o))return 0;return Object.keys(o).filter(function(k){return Array.isArray(o[k])&&o[k].length>0;}).length;}
  function syncClassStores(){var p=parseClasses('personalClasses'),ip=parseClasses('importedPersonalClasses');var c=countClasses(p),ci=countClasses(ip);var best=ci>c?ip:p;if(countClasses(best)>0){try{localStorage.setItem('personalClasses',JSON.stringify(best));localStorage.setItem('importedPersonalClasses',JSON.stringify(best));}catch(e){}return best;}return p;}
  function install(){if(window.__siraRichImportInstalled)return;window.__siraRichImportInstalled=true;window.__siraOriginalImportPersonalClassesFile=window.importPersonalClassesFile;window.importPersonalClassesFile=function(){if(richImport())return;if(window.__siraOriginalImportPersonalClassesFile)return window.__siraOriginalImportPersonalClassesFile.apply(this,arguments);};try{importPersonalClassesFile=window.importPersonalClassesFile;}catch(e){}document.addEventListener('click',function(ev){var t=(ev.target&&ev.target.textContent)||'';if(/Firebase|فاير/i.test(t)){syncClassStores();setTimeout(function(){refresh(syncClassStores());},800);setTimeout(function(){refresh(syncClassStores());},2000);return;}if(/استيراد وحفظ|استيراد/.test(t)){if(richImport()){ev.preventDefault();ev.stopPropagation();}}},true);}
  install();setTimeout(install,500);setTimeout(install,1500);setTimeout(install,3000);
})();
</script>
'''


def inject_guard(html_text: str) -> str:
    if STAMP in html_text:
        return html_text
    if re.search(r'<head[^>]*>', html_text, flags=re.I):
        return re.sub(r'(<head[^>]*>)', lambda m: m.group(1) + RICH_IMPORT_JS, html_text, count=1, flags=re.I)
    return RICH_IMPORT_JS + html_text


def patch_app_html(path: Path) -> bool:
    s = path.read_text(encoding='utf-8', errors='ignore')
    original = s
    s = re.sub(r'<option\s+value="9">\s*8\s*أساسي\s*9\s*</option>\s*<option\s+value="8">\s*8\s*أساسي\s*8\s*</option>\s*<option\s+value="7">\s*8\s*أساسي\s*7\s*</option>\s*<option\s+value="6">\s*8\s*أساسي\s*6\s*</option>', '', s, flags=re.I)
    s = s.replace('const ORIGINAL_DEFAULT_CLASSES = JSON.parse(JSON.stringify(data));', 'const ORIGINAL_DEFAULT_CLASSES = {};\nObject.keys(data).forEach(k => delete data[k]);')
    s = s.replace('setTimeout(autoRestoreWhenEmpty, 1400);', '// Auto restore disabled in empty-import build\n    // setTimeout(autoRestoreWhenEmpty, 1400);')
    s = inject_guard(s)
    if s != original:
        path.write_text(s, encoding='utf-8')
        return True
    return False


def bump_gradle_version(root: Path) -> None:
    for gf in list(root.rglob('build.gradle')) + list(root.rglob('build.gradle.kts')):
        s = gf.read_text(encoding='utf-8', errors='ignore')
        original = s
        if gf.parent.name == 'app':
            s = re.sub(r'versionCode\s+\d+', 'versionCode 208', s)
            s = re.sub(r'versionCode\s*=\s*\d+', 'versionCode = 208', s)
            s = re.sub(r'versionName\s+"[^"]+"', 'versionName "empty-import-v8-classes-store-sync"', s)
            s = re.sub(r'versionName\s*=\s*"[^"]+"', 'versionName = "empty-import-v8-classes-store-sync"', s)
            s = re.sub(r"versionName\s+'[^']+'", "versionName 'empty-import-v8-classes-store-sync'", s)
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
        raise SystemExit('No HTML file was patched')
    bump_gradle_version(root)

if __name__ == '__main__':
    main()
