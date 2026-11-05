/* Object detail presentation v0.3.5 · 2026-11-02 · OpenAI Codex.
 * Display only: no unit inference, quantity conversion or IFC writeback.
 */
(function(root){
  'use strict';
  const escape=value=>String(value??'').replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
  const missing=value=>value===null||value===undefined||value===''||(Array.isArray(value)&&value.length===0);
  function display(value){
    if(missing(value))return '<span class="detail-missing">Nicht angegeben</span>';
    if(Array.isArray(value))return value.map(display).join('<br>');
    if(typeof value==='object')return '<dl class="nested-properties">'+Object.entries(value).map(([key,item])=>`<div><dt>${escape(key)}</dt><dd>${display(item)}</dd></div>`).join('')+'</dl>';
    if(typeof value==='boolean')return value?'Ja':'Nein';
    return escape(value);
  }
  function rawData(data){return `<details class="technical-data"><summary>Technische Rohdaten (JSON)</summary><pre>${escape(JSON.stringify(data,null,2))}</pre></details>`;}
  function propertySets(data={}){
    const groups=Object.entries(data||{});
    if(!groups.length)return '<p class="detail-missing">Keine Property Sets vorhanden.</p>';
    return '<p class="detail-help">Originalwerte aus IFC. Einheiten werden nicht aus Eigenschaftsnamen abgeleitet.</p>'+groups.map(([name,properties],index)=>{
      const rows=properties&&typeof properties==='object'&&!Array.isArray(properties)?Object.entries(properties).filter(([key])=>key!=='id'):[['Wert',properties]];
      const id=properties?.id;
      return `<details class="pset-group" ${index===0?'open':''}><summary><span>${escape(name)}</span><small>${rows.length} Eigenschaften</small></summary>${id!==undefined?`<p class="pset-record">IFC-Datensatz #${escape(id)}</p>`:''}<table class="property-table"><caption class="visually-hidden">${escape(name)}</caption><thead><tr><th scope="col">Eigenschaft</th><th scope="col">Wert</th></tr></thead><tbody>${rows.map(([key,value])=>`<tr><th scope="row">${escape(key)}</th><td>${display(value)}</td></tr>`).join('')}</tbody></table></details>`;
    }).join('')+rawData(data);
  }
  function quantities(data={}){
    const labels={gross_volume_701:'Bruttovolumen · BASF 701',custom_gross_volume:'Bruttovolumen · eigenes QTO',net_volume:'Nettovolumen · IFC-Basisquantität'};
    const rows=Object.entries(data||{});
    if(!rows.length)return '<p class="detail-missing">Keine Mengen vorhanden.</p>';
    return '<p class="detail-help">Brutto- und Nettowerte getrennt. Zahlenanzeige mit bis zu 6 Nachkommastellen; exakter Rohwert aufklappbar.</p>'+rows.map(([key,quantity])=>{
      const q=quantity||{},present=!missing(q.value),number=typeof q.value==='number'&&Number.isFinite(q.value)?new Intl.NumberFormat('de-DE',{maximumFractionDigits:6}).format(q.value):escape(q.value);
      const unit=({'m3':'m³','m2':'m²'})[q.unit]||q.unit||'';
      return `<article class="quantity-card"><h5>${escape(labels[key]||key)}</h5><p class="quantity-value">${present?`${number}${unit?' <span>'+escape(unit)+'</span>':''}`:'<span class="detail-missing">Nicht vorhanden</span>'}</p><dl class="quantity-source"><dt>Quelle</dt><dd>${missing(q.source)?'Nicht angegeben':escape(q.source)}</dd></dl>${present?`<details class="quantity-exact"><summary>Exakten Rohwert anzeigen</summary><code>${escape(q.value)}</code>${unit?' '+escape(unit):''}</details>`:''}</article>`;
    }).join('')+rawData(data);
  }
  const api={propertySets,quantities};
  if(typeof module==='object'&&module.exports)module.exports=api;
  else root.IqaObjectDetails=api;
})(typeof globalThis!=='undefined'?globalThis:this);
