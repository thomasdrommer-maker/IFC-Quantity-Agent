/* Layout regression: filters stay visible while long lists/details scroll. */
const assert=require('node:assert/strict');
const fs=require('node:fs');
const path=require('node:path');
const http=require('node:http');
const {chromium}=require(process.env.IQA_PLAYWRIGHT_MODULE||require.resolve('playwright',{paths:[path.join(__dirname,'browser')]}));
const root=path.resolve(__dirname,'../ui');
const server=http.createServer((req,res)=>{
  const pathname=new URL(req.url,'http://localhost').pathname;
  const file=path.resolve(root,'.'+(pathname==='/'?'/index.html':pathname));
  if(!file.startsWith(root+path.sep)){res.writeHead(403).end();return;}
  try{res.setHeader('Content-Type',file.endsWith('.js')?'text/javascript':file.endsWith('.css')?'text/css':'text/html');res.end(fs.readFileSync(file));}catch{res.writeHead(404).end();}
});
(async()=>{
  await new Promise(resolve=>server.listen(0,'127.0.0.1',resolve));
  const browser=await chromium.launch({headless:true});
  try{
    for(const viewport of [{width:1500,height:900},{width:1280,height:720},{width:1280,height:600},{width:1024,height:768},{width:390,height:844}]){
      const page=await browser.newPage({viewport});const errors=[];page.on('pageerror',e=>errors.push(e.message));
      const object={global_id:'fixture-0',ifc_class:'IfcBeam',name:'Unterzug Test',materials:['Stahlbeton'],property_sets:Object.fromEntries(Array.from({length:20},(_,i)=>['Pset_Test_'+i,{id:i,Description:'Langer Testwert zur Kontrolle der Fensterhöhe',Value:7.7}])),quantities:{net_volume:{value:7.695,unit:'m3',source:'Qto_BeamBaseQuantities.NetVolume'}},findings:[]};
      await page.route('**/api/**',route=>route.fulfill({json:route.request().url().includes('/health')?{api_version:'1.0.0',rule_package:{rule_count:32}}:{object}}));
      await page.goto(`http://127.0.0.1:${server.address().port}/`);
      await page.evaluate(async()=>{
        state.analysisId='layout-fixture';state.overview={counts:{ifc_elements:600},summary:{passed:8,total:32,failed:24},model:{schema:'IFC4'},lv_ident:{}};
        state.rules=[{rule_id:'IQA-M1-FILE-001',status:'failed',expected:'old',actual:'new'}];
        state.objects=Array.from({length:600},(_,i)=>({global_id:'fixture-'+i,ifc_class:'IfcBeam',name:'Unterzug '+i,lv_ident:null,materials:[],finding_count:0}));
        document.querySelector('#upload-panel').classList.add('loaded');renderAll();await openObject('fixture-0');
        document.querySelectorAll('.pset-group').forEach(group=>group.open=true);
      });
      const before=await page.evaluate(()=>{
        const box=e=>{const r=e.getBoundingClientRect();return {top:r.top,bottom:r.bottom,height:r.height}};
        return {toolbar:box(document.querySelector('#objects-layout .table-toolbar')),head:box(document.querySelector('#objects-layout thead'))};
      });
      const result=await page.evaluate(()=>{
        const list=document.querySelector('.table-scroll.tall'),detail=document.querySelector('#detail-panel');
        list.scrollTop=list.scrollHeight;detail.scrollTop=detail.scrollHeight;
        const box=e=>{const r=e.getBoundingClientRect();return {top:r.top,bottom:r.bottom,height:r.height}};
        return {toolbar:box(document.querySelector('#objects-layout .table-toolbar')),head:box(document.querySelector('#objects-layout thead')),last:box(document.querySelector('#object-body tr:last-child')),list:box(list),detail:box(detail),listScroll:list.scrollTop,detailScroll:detail.scrollTop,pageScroll:window.scrollY,documentHeight:document.documentElement.scrollHeight};
      });
      if(process.env.IQA_LAYOUT_SCREENSHOTS)await page.screenshot({path:path.join(process.env.IQA_LAYOUT_SCREENSHOTS,`object-scroll-${viewport.width}x${viewport.height}.png`)});
      assert.equal(result.pageScroll,0,JSON.stringify({viewport,result}));
      assert.ok(result.documentHeight<=viewport.height+1,JSON.stringify({viewport,result}));
      assert.ok(result.listScroll>0&&result.detailScroll>0,JSON.stringify({viewport,result}));
      assert.ok(Math.abs(before.toolbar.top-result.toolbar.top)<1);
      assert.ok(Math.abs(before.head.top-result.head.top)<1);
      assert.ok(result.toolbar.top>=0&&result.toolbar.bottom<=viewport.height);
      assert.ok(result.last.bottom<=result.list.bottom+1,'Last row remains reachable');
      assert.ok(result.detail.bottom<=viewport.height+1&&result.detail.height>100);
      await page.mouse.move((await page.locator("#detail-panel").boundingBox()).x+30,result.detail.bottom-30);
      await page.mouse.wheel(0,1000);
      assert.equal(await page.evaluate(()=>window.scrollY),0,"Wheel must not scroll the whole page");
      assert.deepEqual(errors,[]);
      if(process.env.IQA_LAYOUT_SCREENSHOTS)await page.screenshot({path:path.join(process.env.IQA_LAYOUT_SCREENSHOTS,`object-scroll-${viewport.width}x${viewport.height}.png`)});
      await page.evaluate(()=>activateView('overview'));
      assert.equal(await page.evaluate(()=>document.body.classList.contains('object-view')),false);
      console.log(`Object scrolling ${viewport.width}x${viewport.height}: passed`);await page.close();
    }
  }finally{await browser.close();}
})().catch(error=>{console.error(error);process.exitCode=1}).finally(()=>server.close());
