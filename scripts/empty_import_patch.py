from pathlib import Path
import re

STAMP = 'SIRA_V2_RICH_IMPORT_FIREBASE_ALL_20260613_01'

RICH_IMPORT_JS = r'''
<script>
(function(){
  var stamp='SIRA_V2_RICH_IMPORT_FIREBASE_ALL_20260613_01';
  function norm(s){return String(s||'').replace(/[\u064B-\u065F\u0670]/g,'').replace(/[أإآ]/g,'ا').replace(/ة/g,'ه').replace(/ى/g,'ي').replace(/\s+/g,'').toLowerCase();}
  function findIndex(headers, aliases){var hh=headers.map(norm);for(var a=0;a<aliases.length;a++){var n=norm(aliases[a]);for(var i=0;i<hh.length;i++){if(hh[i]===n||hh[i].indexOf(n)>=0||n.indexOf(hh[i])>=0)return i;}}return -1;}
  function cell(row,i){return i>=0?String(row[i]||'').trim():'';}
  function toast(msg,type){try{if(typeof showToast==='function')showToast(msg,type||'success');else alert(msg);}catch(e){}}
  function makeRecord(cls,name,uid,bdate,bplace,father){bplace=(bplace||'').trim()||'تونس';father=(father||'').trim();return {'القسم':cls,'className':cls,'class':cls,'اسم التلميذ':name,'الاسم واللقب':name,'name':name,'studentName':name,'المعرف الوحيد':uid,'معرف وحيد':uid,'uniqueId':uid,'studentId':uid,'identifiantUnique':uid,'تاريخ الولادة':bdate,'birthDate':bdate,'dateNaissance':bdate,'مكان الولادة':bplace,'مكانها':bplace,'مكان الميلاد':bplace,'مكان الازدياد':bplace,'birthPlace':bplace,'placeOfBirth':bplace,'lieuNaissance':bplace,'اسم الأب':father,'اسم الاب':father,'الأب':father,'الاب':father,'fatherName':father,'father':father,'nomPere':father,'الولي':father,'اسم الولي':father,'ولي الأمر':father,'اسم ولي الأمر':father,'guardianName':father,'guardian':father,'parentName':father,'tuteur':father};}
  function parseRichTable(aoa){if(!aoa||!aoa.length)return null;var headers=(aoa[0]||[]).map(function(x){return String(x||'').trim();});var idxCls=findIndex(headers,['القسم','قسم','class','classe']);var idxName=findIndex(headers,['اسم التلميذ','الاسم واللقب','الإسم واللقب','اسم ولقب','الاسم','name','studentName']);if(idxCls<0||idxName<0)return null;var idxUid=findIndex(headers,['المعرف الوحيد','معرف وحيد','uniqueId','identifiant unique','id unique']);var idxBirth=findIndex(headers,['تاريخ الولادة','تاريخ الميلاد','date naissance','birthDate']);var idxPlace=findIndex(headers,['مكان الولادة','مكان الميلاد','مكان الازدياد','مكانها','lieu naissance','birthPlace','placeOfBirth']);var idxFather=findIndex(headers,['اسم الأب','اسم الاب','الأب','الاب','fatherName','nom pere','pere']);var personal={},records=[];for(var r=1;r<aoa.length;r++){var row=aoa[r]||[],cls=cell(row,idxCls),name=cell(row,idxName);if(!cls||!name)continue;if(!personal[cls])personal[cls]=[];if(personal[cls].indexOf(name)<0)personal[cls].push(name);records.push(makeRecord(cls,name,cell(row,idxUid),cell(row,idxBirth),cell(row,idxPlace),cell(row,idxFather)));}return Object.keys(personal).length?{personal:personal,records:records}:null;}
  function setStores(personal,records){personal=personal||{};records=records||[];try{if(typeof savePersonalClasses==='function')savePersonalClasses(personal);}catch(e){}try{localStorage.setItem('personalClasses',JSON.stringify(personal));localStorage.setItem('importedPersonalClasses',JSON.stringify(personal));}catch(e){}var byName={},byClassName={};records.forEach(function(r){var n=r['الاسم واللقب']||r.name||r.studentName,c=r['القسم']||r.className||r.class;if(n){byName[n]=r;if(c)byClassName[c+'|'+n]=r;}});['studentInfoRecords','importedStudentInfoRecords','personalStudentInfoRecords','studentsInfo','studentInfos'].forEach(function(k){try{localStorage.setItem(k,JSON.stringify(records));}catch(e){}});['studentInfoByName','studentInfosByName','studentCards','studentCardsByName','siraStudentInfo'].forEach(function(k){try{localStorage.setItem(k,JSON.stringify(byName));}catch(e){}});try{localStorage.setItem('studentInfoByClassAndName',JSON.stringify(byClassName));}catch(e){}refreshAll(personal);}
  function refreshAll(personal){try{if(typeof replaceDataWithPersonalClasses==='function')replaceDataWithPersonalClasses();}catch(e){}try{if(typeof refreshClassSelectOptions==='function')refreshClassSelectOptions(Object.keys(personal||{})[0]||'');}catch(e){}try{if(typeof resetDashboard==='function')resetDashboard();}catch(e){}try{if(typeof renderStudentsList==='function')renderStudentsList();}catch(e){}try{if(typeof renderPersonalClassesList==='function')renderPersonalClassesList();}catch(e){}try{if(typeof clearImportedClassesFile==='function')clearImportedClassesFile();}catch(e){}}
  function saveRich(parsed){setStores(parsed.personal,parsed.records||[]);toast('تم استيراد الأقسام ومعطيات بطاقة السيرة بنجاح','success');}
  function richImport(){var input=document.querySelector('input[type=file]'),file=input&&input.files&&input.files[0];if(!file||!window.XLSX)return false;var reader=new FileReader();reader.onload=function(ev){try{var wb=XLSX.read(ev.target.result,{type:'array'}),ws=wb.Sheets[wb.SheetNames[0]],aoa=XLSX.utils.sheet_to_json(ws,{header:1,raw:false,defval:''}),parsed=parseRichTable(aoa);if(parsed)saveRich(parsed);else if(window.__siraOriginalImportPersonalClassesFile)window.__siraOriginalImportPersonalClassesFile();}catch(err){if(window.__siraOriginalImportPersonalClassesFile)window.__siraOriginalImportPersonalClassesFile();}};reader.readAsArrayBuffer(file);return true;}
  function jget(k,def){try{return JSON.parse(localStorage.getItem(k)||def);}catch(e){return JSON.parse(def);}}
  function nonEmptyObj(o){return o&&typeof o==='object'&&!Array.isArray(o)&&Object.keys(o).length>0;}
  function collectPayload(){var p=jget('personalClasses','{}'),ip=jget('importedPersonalClasses','{}');if(!nonEmptyObj(p)&&nonEmptyObj(ip))p=ip;if(nonEmptyObj(p))try{localStorage.setItem('personalClasses',JSON.stringify(p));localStorage.setItem('importedPersonalClasses',JSON.stringify(p));}catch(e){}var candidates=['studentInfoRecords','importedStudentInfoRecords','personalStudentInfoRecords','studentsInfo','studentInfos'];var rec=[];for(var i=0;i<candidates.length;i++){var x=jget(candidates[i],'[]');if(Array.isArray(x)&&x.length>rec.length)rec=x;}return {personalClasses:p,importedPersonalClasses:p,studentInfoRecords:rec,importedStudentInfoRecords:rec,updatedAt:new Date().toISOString(),source:'sira-v2-all-classes'};}
  function fb(){return window.firebase||null;}
  async function uploadAllFirebase(){var f=fb();if(!f)throw new Error('Firebase غير جاهز');var payload=collectPayload();var ok=false;if(f.firestore){try{await f.firestore().collection('sira2_sync').doc('all_classes').set(payload,{merge:true});ok=true;}catch(e){}}if(f.database){try{await f.database().ref('sira2_sync/all_classes').set(payload);ok=true;}catch(e){}}if(!ok)throw new Error('تعذر الرفع إلى Firebase');toast('تم رفع كل الأقسام ومعطيات بطاقة السيرة إلى Firebase','success');}
  async function downloadAllFirebase(){var f=fb();if(!f)throw new Error('Firebase غير جاهز');var data=null;if(f.firestore){try{var d=await f.firestore().collection('sira2_sync').doc('all_classes').get();if(d&&d.exists)data=d.data();}catch(e){}}if(!data&&f.database){try{var s=await f.database().ref('sira2_sync/all_classes').once('value');data=s.val();}catch(e){}}if(!data)throw new Error('لا توجد نسخة كاملة محفوظة في Firebase');var p=data.personalClasses||data.importedPersonalClasses||{};var r=data.studentInfoRecords||data.importedStudentInfoRecords||[];setStores(p,r);toast('تم استرجاع كل الأقسام ومعطيات بطاقة السيرة من Firebase','success');}
  function install(){if(window.__siraRichImportInstalled)return;window.__siraRichImportInstalled=true;window.__siraOriginalImportPersonalClassesFile=window.importPersonalClassesFile;window.importPersonalClassesFile=function(){if(richImport())return;if(window.__siraOriginalImportPersonalClassesFile)return window.__siraOriginalImportPersonalClassesFile.apply(this,arguments);};try{importPersonalClassesFile=window.importPersonalClassesFile;}catch(e){}window.__siraUploadAllFirebase=uploadAllFirebase;window.__siraDownloadAllFirebase=downloadAllFirebase;document.addEventListener('click',function(ev){var t=(ev.target&&ev.target.textContent)||'';if(/رفع.*(Firebase|فاير)|(?:Firebase|فاير).*رفع/i.test(t)){ev.preventDefault();ev.stopPropagation();uploadAllFirebase().catch(function(e){toast(String(e.message||e),'error');});return;}if(/(استرجاع|استيراد).*(Firebase|فاير)|(?:Firebase|فاير).*(استرجاع|استيراد)/i.test(t)){ev.preventDefault();ev.stopPropagation();downloadAllFirebase().catch(function(e){toast(String(e.message||e),'error');});return;}if(/استيراد وحفظ|استيراد/.test(t)&&!/(Firebase|فاير)/i.test(t)){if(richImport()){ev.preventDefault();ev.stopPropagation();}}},true);}
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
            s = re.sub(r'versionCode\s+\d+', 'versionCode 207', s)
            s = re.sub(r'versionCode\s*=\s*\d+', 'versionCode = 207', s)
            s = re.sub(r'versionName\s+"[^"]+"', 'versionName "empty-import-v7-firebase-all-sync"', s)
            s = re.sub(r'versionName\s*=\s*"[^"]+"', 'versionName = "empty-import-v7-firebase-all-sync"', s)
            s = re.sub(r"versionName\s+'[^']+'", "versionName 'empty-import-v7-firebase-all-sync'", s)
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
