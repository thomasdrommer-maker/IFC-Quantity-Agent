/* Native IFC relationship viewer, v0.3.7; 2026-11-03; OpenAI Codex. */
(function(root){
 'use strict';
 const esc=v=>String(v??'').replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
 function index(data){const nodes=new Map((data.nodes||[]).map(n=>[n.node_id,n])),children=new Map();for(const edge of data.edges||[]){if(!children.has(edge.parent))children.set(edge.parent,[]);children.get(edge.parent).push(edge)}return {nodes,children};}
 function label(node){const name=node.name||'Unbenannt';return `${node.is_element?`<button type="button" class="tree-object" data-step-id="${node.step_id}">${esc(name)}</button>`:`<strong>${esc(name)}</strong>`}<span class="tree-meta">${esc(node.ifc_class)} · #${node.step_id}${node.global_id?' · '+esc(node.global_id):' · GlobalId fehlt'}</span>`;}
 function nodeHtml(id,graph,path=[],relation=''){
  const node=graph.nodes.get(id);if(!node)return '';
  const info=relation?`<span class="tree-relation">${esc(relation)}</span>`:'';
  if(path.includes(id))return `<div class="tree-warning">Zyklischer Verweis: ${label(node)}${info}</div>`;
  if(!(graph.children.get(id)||[]).length)return `<div class="tree-leaf">${label(node)}${info}</div>`;
  return `<details class="tree-node" data-node="${esc(id)}" data-path="${esc(JSON.stringify([...path,id]))}"><summary>${label(node)}${info}<span class="tree-meta">${graph.children.get(id).length} direkte Beziehungen</span></summary><div class="tree-children"></div></details>`;
 }
 function section(title,body){return `<details class="tree-section" open><summary>${esc(title)}</summary>${body||'<p class="muted">Keine Einträge.</p>'}</details>`;}
 function render(data,filters={}){
  const graph=index(data),all=[...graph.nodes.values()],q=(filters.query||'').toLowerCase();
  const filtered=all.filter(n=>(!q||[n.name,n.ifc_class,n.global_id,n.step_id,n.lv_ident].join(' ').toLowerCase().includes(q))&&(!filters.ifcClass||n.ifc_class===filters.ifcClass)&&(!filters.material||(n.materials||[]).includes(filters.material)));
  if(q||filters.ifcClass||filters.material)return {html:section(`Such-/Filterergebnis (${filtered.length} Objekte)`,filtered.map(n=>`<div class="tree-leaf">${label(n)}</div>`).join('')),count:filtered.length};
  if(filters.mode==='lv'){
   const groups=new Map();for(const n of all.filter(n=>n.is_element)){const key=n.lv_ident||'(LV-Ident leer)';if(!groups.has(key))groups.set(key,[]);groups.get(key).push(n)}
   return {html:[...groups.entries()].sort(([a],[b])=>a.localeCompare(b,'de')).map(([key,nodes])=>section(`${key} (${nodes.length})`,nodes.map(n=>`<div class="tree-leaf">${label(n)}</div>`).join(''))).join(''),count:all.filter(n=>n.is_element).length};
  }
  const spatial=(data.roots||[]).filter(id=>graph.nodes.get(id)?.is_spatial),detached=(data.roots||[]).filter(id=>!graph.nodes.get(id)?.is_spatial);
  let html=filters.mode==='assemblies'?section('Baugruppen – tatsächliche IFC-Beziehungen',all.filter(n=>n.is_assembly).map(n=>nodeHtml(n.node_id,graph)).join('')):section('Räumliche IFC-Struktur',spatial.map(id=>nodeHtml(id,graph)).join(''))+section('Ohne übergeordnete Beziehung',detached.map(id=>nodeHtml(id,graph)).join(''));
  if((data.cycle_roots||[]).length)html+=section('Beziehungskomponenten ohne Wurzel – prüfen',data.cycle_roots.map(id=>nodeHtml(id,graph)).join(''));
  html+=section(`Ohne direkte räumliche Zuordnung (${(data.uncontained_elements||[]).length})`,(data.uncontained_elements||[]).map(id=>{const n=graph.nodes.get(id);return n?`<div class="tree-leaf">${label(n)}</div>`:''}).join(''));
  return {html,count:all.length};
 }
 function wire(container,data,onOpen){const graph=index(data);
  container.onclick=event=>{const button=event.target.closest('[data-step-id]');if(button){event.preventDefault();event.stopPropagation();onOpen(Number(button.dataset.stepId));}};
  container.ontoggle=null;
  // Capture is required because native toggle events do not bubble.
  if(container._treeToggle)container.removeEventListener('toggle',container._treeToggle,true);
  container._treeToggle=event=>{const item=event.target;if(!item.matches('details[data-node]')||!item.open||item.dataset.loaded)return;item.dataset.loaded='1';const path=JSON.parse(item.dataset.path);item.querySelector(':scope > .tree-children').innerHTML=(graph.children.get(item.dataset.node)||[]).map(e=>nodeHtml(e.child,graph,path,`${e.relation_type} #${e.relation_step_id}`)).join('');};
  container.addEventListener('toggle',container._treeToggle,true);
 }
 const api={index,nodeHtml,render,wire};if(typeof module==='object'&&module.exports)module.exports=api;else root.IqaStructure=api;
})(globalThis);
