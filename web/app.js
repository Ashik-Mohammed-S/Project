const $=s=>document.querySelector(s);
const esc=s=>String(s).replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
document.querySelectorAll('[data-question]').forEach(b=>b.onclick=()=>{$('#question').value=b.dataset.question;$('#question').focus();});
$('#ask').onsubmit=async event=>{
  event.preventDefault();$('#submit').disabled=true;$('#answer').hidden=false;$('#answer').textContent='Finding evidence…';$('#evidence').textContent='';
  try{const response=await fetch('/api/ask',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({question:$('#question').value,mode:$('#mode').value})});const data=await response.json();if(!response.ok)throw Error(data.error||'Request failed');$('#answer').innerHTML=`<strong>${data.abstained?'ABSTAINED':data.mode==='extractive'?'EVIDENCE QUOTATION':'LOCAL MODEL ANSWER'}</strong>${esc(data.answer)}<br><small>Sources: ${esc(data.citations.join(', ')||'none')} · ${data.elapsed_ms} ms · ${esc(data.reason||data.mode)}</small>`;$('#evidence').innerHTML=data.evidence.map(e=>`<details><summary>${esc(e.id)} · ${esc(e.title)}</summary><p>${esc(e.text)}</p><code>${esc(e.source)}</code></details>`).join('');}
  catch(error){$('#answer').textContent=error.message;}finally{$('#submit').disabled=false;}
};
async function loadReport(){try{const r=await fetch('/api/reports/'+encodeURIComponent($('#report').value));const data=await r.json();if(!r.ok)throw Error(data.error);const rows=data.rows;const keys=rows.length?Object.keys(rows[0]):[];$('#table').innerHTML=rows.length?'<thead><tr>'+keys.map(k=>'<th>'+esc(k.replaceAll('_',' '))+'</th>').join('')+'</tr></thead><tbody>'+rows.map(row=>'<tr>'+keys.map(k=>'<td>'+esc(row[k]??'—')+'</td>').join('')+'</tr>').join('')+'</tbody>':'<tr><td>No exceptions found.</td></tr>';}
catch(error){$('#table').innerHTML='<tr><td>'+esc(error.message)+'</td></tr>';}}
$('#report').onchange=loadReport;loadReport();
