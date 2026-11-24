const IqaQuantities=(()=>{
  const qs={groupBy:'lv_ident',data:null,material:''};
  const num=v=>new Intl.NumberFormat('de-DE',{minimumFractionDigits:2,maximumFractionDigits:2}).format(v);
  const cell=e=>{
    const total=e.objects_with_value+e.objects_missing;
    if(e.sum===null)return `<span class="severity warning">fehlt</span> <span class="cell-sub">0 von ${total}</span>`;
    const partial=e.objects_missing?` <span class="severity warning">${e.objects_with_value} von ${total}</span>`:'';
    return `<div class="cell-main" title="${esc(e.source_path)}">${num(e.sum)}</div>${partial}`;
  };
  const rowHtml=(g,attrs='')=>`<tr ${attrs}><td><div class="cell-main">${esc(g.label)}</div>${g.unassigned?'<div class="cell-sub">nicht zugeordnet, nicht ersetzt</div>':''}</td><td>${fmt(g.object_count)}</td><td>${cell(g.gross_701)}</td><td>${cell(g.custom_qto)}</td><td>${cell(g.net_volume)}</td><td>${esc(g.materials.map(m=>`${m.name} (${m.objects})`).join(', ')||'—')}</td><td>${g.finding_count?`<span class="severity warning">${g.finding_count}</span>`:'—'}</td></tr>`;
  const hasWarning=g=>g.unassigned||g.gross_701.objects_missing||g.custom_qto.objects_missing||g.net_volume.objects_missing||g.finding_count;

  async function load(){
    if(!state.analysisId)return;
    const q=new URLSearchParams({group_by:qs.groupBy});if(qs.material)q.set('material',qs.material);
    qs.data=await api(`/api/v1/analyses/${state.analysisId}/quantity-summary?${q}`);
    $('#qty-empty').classList.add('hidden');$('#qty-content').classList.remove('hidden');
    if(!qs.material){const mats=[...new Set(qs.data.groups.flatMap(g=>g.materials.map(m=>m.name)))].sort();$('#qty-material').innerHTML='<option value="">Alle Materialien</option>'+mats.map(m=>`<option value="${esc(m)}">${esc(m)}</option>`).join('')}
    $('#qty-drill').classList.add('hidden');
    render();
  }
  function render(){
    const d=qs.data;if(!d)return;
    const search=$('#qty-search').value.toLowerCase(),onlyWarn=$('#qty-only-warnings').checked;
    const groups=d.groups.filter(g=>(!search||g.label.toLowerCase().includes(search))&&(!onlyWarn||hasWarning(g)));
    $('#qty-warnings').innerHTML=d.warnings.length?`<div class="reference-status differs"><strong>Hinweise zur Datenlage</strong><p>${d.warnings.map(w=>esc(w.message)).join(' · ')}. Fehlende Werte werden nicht durch andere Quellen ersetzt; Brutto, QTO-Brutto und Netto werden nie vermischt.</p></div>`:'';
    $('#qty-head').innerHTML=`<tr><th>${d.group_by==='lv_ident'?'LV-Ident (BASF_General.540)':'Native IFC-Klasse'}</th><th>Objekte</th><th>Brutto 701 (${esc(d.unit.replace('3','³'))})</th><th>QTO-Brutto (${esc(d.unit.replace('3','³'))})</th><th>Netto (${esc(d.unit.replace('3','³'))})</th><th>Material</th><th>Findings</th></tr>`;
    $('#qty-body').innerHTML=groups.map((g,i)=>rowHtml(g,`data-qty-index="${d.groups.indexOf(g)}" class="clickable"`)).join('');
    $('#qty-foot').innerHTML=rowHtml({...d.totals,label:'Gesamt',unassigned:false});
    $('#qty-count').textContent=`${groups.length} von ${d.groups.length} Gruppen`;
    $$('#qty-body tr').forEach(tr=>tr.addEventListener('click',()=>drill(d.groups[Number(tr.dataset.qtyIndex)])));
  }
  async function drill(g){
    const q=new URLSearchParams({limit:'1000'});
    if(qs.groupBy==='ifc_class')q.set('ifc_class',g.key);else if(g.unassigned)q.set('missing_lv_ident','true');else q.set('lv_ident',g.key);
    const r=await api(`/api/v1/analyses/${state.analysisId}/objects?${q}`);
    const items=qs.material?r.items.filter(o=>(o.materials||[]).includes(qs.material)):r.items;
    const v=x=>x===null||x===undefined?'<span class="severity warning">fehlt</span>':num(x);
    $('#qty-drill-title').textContent=`Objekte in „${g.label}“`;$('#qty-drill-count').textContent=`${items.length} Objekte`;
    $('#qty-drill-body').innerHTML=items.map(o=>`<tr class="clickable" data-global-id="${esc(o.global_id)}" data-step-id="${esc(o.step_id)}"><td><div class="cell-main">${esc(o.ifc_class)}</div><div class="cell-sub">#${esc(o.step_id)}</div></td><td>${esc(value(o.name))}</td><td>${esc(value(o.global_id))}</td><td>${o.lv_ident?esc(o.lv_ident):'<span class="severity warning">leer</span>'}</td><td>${v(o.gross_701)}</td><td>${v(o.custom_qto)}</td><td>${v(o.net_volume)}</td></tr>`).join('');
    $$('#qty-drill-body tr').forEach(tr=>tr.addEventListener('click',()=>openObject(tr.dataset.globalId,null)));
    $('#qty-drill').classList.remove('hidden');
  }
  $$('[data-qty-group]').forEach(b=>b.addEventListener('click',()=>{qs.groupBy=b.dataset.qtyGroup;$$('[data-qty-group]').forEach(x=>{x.classList.toggle('active',x===b);x.setAttribute('aria-pressed',String(x===b))});load()}));
  $('#qty-material').addEventListener('change',e=>{qs.material=e.target.value;load()});
  $('#qty-search').addEventListener('input',render);$('#qty-only-warnings').addEventListener('change',render);
  return {load};
})();
