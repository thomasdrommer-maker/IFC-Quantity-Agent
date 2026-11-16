/* Native IFC relationship viewer, v0.3.11; 2026-11-15; OpenAI Codex. */
(function(root){
 'use strict';
 const esc=v=>String(v??'').replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
 function index(data){const nodes=new Map((data.nodes||[]).map(n=>[n.node_id,n])),children=new Map();for(const edge of data.edges||[]){if(!children.has(edge.parent))children.set(edge.parent,[]);children.get(edge.parent).push(edge)}return {nodes,children};}
 function label(node){
  const present=v=>v!==null&&v!==undefined&&v!=='';
  const field=v=>present(v)?esc(v):'<em class="detail-missing">Nicht angegeben</em>';
  const core=node.bim_core||{};
  const attribute=(key,native)=>{
   if(present(native))return `<span><b>${key}:</b> ${field(native)} <small>(natives IFC-Attribut)</small>${present(core[key])&&String(core[key])!==String(native)?`<span class="tree-source-difference">BIM_Core.${key}: ${field(core[key])} · abweichender PSet-Wert</span>`:''}</span>`;
   if(present(core[key]))return `<span><b>${key}:</b> ${field(core[key])} <small>(Quelle: BIM_Core.${key}; natives IFC-Attribut leer)</small></span>`;
   return `<span><b>${key}:</b> ${field(native)} <small>(nativ und in BIM_Core)</small></span>`;
  };
  const differences=[['IfcName',node.name],['IfcClass',node.ifc_class]].filter(([key,native])=>present(core[key])&&String(core[key])!==String(native??'')).map(([key])=>`<span class="tree-source-difference">BIM_Core.${key}: ${field(core[key])} · ${key==='IfcClass'?'abweichende PSet-Angabe; native Klasse bleibt maßgeblich':'abweichender PSet-Wert'}</span>`).join('');
  return `<span class="tree-field-label">IfcName (nativ): </span>${node.is_element?`<button type="button" class="tree-object" data-step-id="${node.step_id}">${field(node.name)}</button>`:`<strong>${field(node.name)}</strong>`}<span class="tree-meta">IfcClass (nativ): ${esc(node.ifc_class)} · #${node.step_id}${node.global_id?' · '+esc(node.global_id):' · GlobalId fehlt'}</span><span class="tree-attributes">${differences}${attribute('IfcDescription',node.description)}${attribute('IfcObjectType',node.object_type)}</span>`;
 }
 function nodeHtml(id,graph,path=[],relation=''){
  const node=graph.nodes.get(id);if(!node)return '';
  const info=relation?`<span class="tree-relation">${esc(relation)}</span>`:'';
  if(path.includes(id))return `<div class="tree-warning">Zyklischer Verweis: ${label(node)}${info}</div>`;
  if(!(graph.children.get(id)||[]).length)return `<div class="tree-leaf">${label(node)}${info}</div>`;
  return `<details class="tree-node" ${path.length===0?'open':''} data-node="${esc(id)}" data-path="${esc(JSON.stringify([...path,id]))}"><summary>${label(node)}${info}<span class="tree-meta">${graph.children.get(id).length} direkte Beziehungen</span><button type="button" class="tree-collapse" data-collapse-children aria-label="Untergruppen zuklappen">Untergruppen zuklappen</button></summary><div class="tree-children"></div></details>`;
 }
 function section(title,body){return `<details class="tree-section" open><summary>${esc(title)}<button type="button" class="tree-collapse" data-collapse-children aria-label="Untergruppen zuklappen">Untergruppen zuklappen</button></summary>${body||'<p class="muted">Keine Einträge.</p>'}</details>`;}
 function render(data,filters={}){
  const graph=index(data),all=[...graph.nodes.values()],q=(filters.query||'').toLowerCase();
  const filtered=all.filter(n=>(!q||[n.name,n.ifc_class,n.description,n.object_type,n.global_id,n.step_id,n.lv_ident,...Object.values(n.bim_core||{})].join(' ').toLowerCase().includes(q))&&(!filters.ifcClass||n.ifc_class===filters.ifcClass)&&(!filters.material||(n.materials||[]).includes(filters.material)));
  if(q||filters.ifcClass||filters.material)return {html:section(`Such-/Filterergebnis (${filtered.length} Objekte)`,filtered.map(n=>`<div class="tree-leaf">${label(n)}</div>`).join('')),count:filtered.length};
  if(filters.mode==='lv'){
   const groups=new Map();for(const n of all.filter(n=>n.is_element)){const key=n.lv_ident||'(LV-Ident leer)';if(!groups.has(key))groups.set(key,[]);groups.get(key).push(n)}
   return {html:[...groups.entries()].sort(([a],[b])=>a.localeCompare(b,'de')).map(([key,nodes])=>section(`${key} (${nodes.length})`,nodes.map(n=>`<div class="tree-leaf">${label(n)}</div>`).join(''))).join(''),count:all.filter(n=>n.is_element).length};
  }
  const spatial=(data.roots||[]).filter(id=>graph.nodes.get(id)?.is_spatial),detached=(data.roots||[]).filter(id=>!graph.nodes.get(id)?.is_spatial);
  let html=filters.mode==='assemblies'?section('Baugruppen – tatsächliche IFC-Beziehungen',all.some(n=>n.is_assembly)?all.filter(n=>n.is_assembly).map(n=>nodeHtml(n.node_id,graph)).join(''):'<p class="structure-empty-message">Keine Baugruppen im Modell vorhanden.</p>'):section('Räumliche IFC-Struktur',spatial.map(id=>nodeHtml(id,graph)).join(''))+section('Ohne übergeordnete Beziehung',detached.map(id=>nodeHtml(id,graph)).join(''));
  if((data.cycle_roots||[]).length)html+=section('Beziehungskomponenten ohne Wurzel – prüfen',data.cycle_roots.map(id=>nodeHtml(id,graph)).join(''));
  html+=section(`Ohne direkte räumliche Zuordnung (${(data.uncontained_elements||[]).length})`,(data.uncontained_elements||[]).map(id=>{const n=graph.nodes.get(id);return n?`<div class="tree-leaf">${label(n)}</div>`:''}).join(''));
  return {html,count:all.length};
 }
 function wire(container,data,onOpen){const graph=index(data);
  container.onclick=event=>{const collapse=event.target.closest('[data-collapse-children]');if(collapse){event.preventDefault();event.stopPropagation();collapse.closest('details').querySelectorAll('details[open]').forEach(group=>group.open=false);return;}const button=event.target.closest('[data-step-id]');if(button){event.preventDefault();event.stopPropagation();onOpen(Number(button.dataset.stepId));}};
  container.ontoggle=null;
  // Capture is required because native toggle events do not bubble.
  if(container._treeToggle)container.removeEventListener('toggle',container._treeToggle,true);
  const loadItem=item=>{if(!item.matches('details[data-node]')||!item.open||item.dataset.loaded)return;item.dataset.loaded='1';const path=JSON.parse(item.dataset.path);item.querySelector(':scope > .tree-children').innerHTML=(graph.children.get(item.dataset.node)||[]).map(e=>nodeHtml(e.child,graph,path,`${e.relation_type} #${e.relation_step_id}`)).join('');};
  container._treeToggle=event=>loadItem(event.target);
  container.addEventListener('toggle',container._treeToggle,true);
  container.querySelectorAll('details[data-node][open]').forEach(loadItem);
 }
 const api={index,nodeHtml,render,wire};if(typeof module==='object'&&module.exports)module.exports=api;else root.IqaStructure=api;
})(globalThis);
