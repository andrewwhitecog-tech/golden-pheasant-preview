import {buildScope} from './scope.mjs';
const form = document.querySelector('#scope-form');
const summary = document.querySelector('#summary');
const result = document.querySelector('#scope-result');
form.addEventListener('submit', event => {
 event.preventDefault();
 const input=Object.fromEntries(new FormData(form)); const value=buildScope(input);
 form.querySelectorAll('[aria-invalid]').forEach(el=>el.removeAttribute('aria-invalid'));
 form.querySelectorAll('.error').forEach(el=>el.textContent='');
 if (!value.ok) {
  result.hidden=true; summary.value=''; document.querySelector('#download-summary').disabled=true;
  document.querySelector('#form-status').textContent='Check the highlighted fields.';
  for (const [key,message] of Object.entries(value.errors)) { const el=form.elements.namedItem(key); el.setAttribute('aria-invalid','true'); document.querySelector('#'+key+'-error').textContent=message; }
  form.elements.namedItem(Object.keys(value.errors)[0]).focus(); return;
 }
 document.querySelector('#form-status').textContent='Your planning summary is ready.';
 document.querySelector('#area').textContent=value.area.toLocaleString('en-US',{maximumSignificantDigits:12});
 document.querySelector('#result-title').textContent=value.title;
 summary.value=value.summary;
 document.querySelector('#flags').replaceChildren(...value.flags.map(text=>{const li=document.createElement('li'); li.textContent=text; return li;}));
 result.hidden=false; summary.style.height='auto'; summary.style.height=summary.scrollHeight+'px'; document.querySelector('#download-summary').disabled=false;
});
document.querySelector('#download-summary').addEventListener('click',()=>{
 const blob=new Blob([summary.value],{type:'text/plain;charset=utf-8'});const url=URL.createObjectURL(blob);const a=document.createElement('a');a.href=url;a.download='Golden-Pheasant-project-summary.txt';a.click();setTimeout(()=>URL.revokeObjectURL(url),1000);
 document.querySelector('#form-status').textContent='Summary download prepared. Nothing was sent to Golden Pheasant.';
});
form.addEventListener('input',()=>{result.hidden=true;summary.value='';document.querySelector('#form-status').textContent='Inputs changed. Update your summary to use these details.';document.querySelector('#download-summary').disabled=true;});
