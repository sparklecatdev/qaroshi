/* Qaroshi Wiki 9.6 dictionary discovery: deterministic, locally ranked search
 * and source-linked lexical relations. Browser + Node, no network.
 * Exact English gloss matches are NOT automatically synonyms; category
 * co-membership is NOT a semantic relation or an antonym license.
 */
(function(root){
  'use strict';
  const fold=s=>String(s||'').normalize('NFD').replace(/[\u0300-\u036f]/g,'').toLowerCase().trim();
  const tokens=s=>fold(s).match(/[a-z0-9ë]+/g)||[];
  const unique=items=>[...new Set(items)];
  const trimGloss=s=>fold(s).replace(/\s*\([^)]*\)\s*/g,' ').replace(/[.,;:]+$/g,'').replace(/\s+/g,' ').trim();
  const isUseful=t=>t.length>=3&&!new Set(['the','and','for','with','that','from','this','into','about','some','thing','form','type']).has(t);
  function createIndex(words){
    if(!Array.isArray(words))throw new TypeError('Dictionary entries required');
    const byForm=new Map(),byId=new Map(),glosses=new Map(),reverse=new Map(),docs=[],byDomain=new Map();
    for(const w of words){
      if(!w || typeof w.qaroshi!=='string'||!w.id)continue;
      const form=fold(w.qaroshi),english=fold(w.english),gloss=trimGloss(w.english);
      const row={w,form,english,gloss,domain:fold(w.domain),sound:fold(w.sound_out),
        components:fold(w.components),note:fold(w.note),ipa:fold(w.ipa),
        englishTokens:unique(tokens(w.english)),formTokens:unique(tokens(w.qaroshi))};
      docs.push(row);byId.set(w.id,row);if(!byForm.has(form))byForm.set(form,row);
      if(!byDomain.has(w.domain))byDomain.set(w.domain,[]);byDomain.get(w.domain).push(row);
      if(gloss){
        if(!glosses.has(gloss))glosses.set(gloss,[]);
        glosses.get(gloss).push(row);
      }
    }
    // The canonical 'components' column is a decomposition, not a guessed
    // relation from substrings. Reverse links only refer to real headwords.
    for(const row of docs){
      if(!row.w.components)continue;
      const parts=String(row.w.components).split(/\s+\+\s+/).map(fold);
      for(const stem of unique(parts)){
        if(stem===row.form||!byForm.has(stem))continue;
        if(!reverse.has(stem))reverse.set(stem,[]);
        reverse.get(stem).push(row);
      }
    }
    function score(row,query,terms){
      if(!query)return 100;
      const {form,english,gloss,domain,note,sound,ipa,components,englishTokens}=row;
      let rank=0;
      if(form===query)rank=1200;
      else if(gloss===query)rank=1100;
      else if(english===query)rank=1000;
      else if(form.startsWith(query))rank=850;
      else if(englishTokens.includes(query))rank=790;
      else if(english.startsWith(query))rank=730;
      else if(form.includes(query))rank=640;
      else if(english.includes(query))rank=560;
      else if(sound===query)rank=520;
      else if(components.includes(query))rank=350;
      else if(domain.includes(query))rank=240;
      else if(note.includes(query)||ipa.includes(query)||sound.includes(query))rank=160;
      // ALL tokens must match somewhere; prevents broad, noisy OR results.
      const termScores=terms.map(t=>{
        if(form===t)return 185;
        if(gloss===t)return 175;
        if(englishTokens.includes(t))return 145;
        if(form.startsWith(t))return 128;
        if(englishTokens.some(x=>x.startsWith(t)))return 105;
        if(form.includes(t))return 87;
        if(english.includes(t))return 67;
        if(components.includes(t))return 37;
        if(domain.includes(t))return 22;
        if(note.includes(t)||sound.includes(t)||ipa.includes(t))return 12;
        return 0;
      });
      if(termScores.some(x=>x===0))return -1;
      rank+=termScores.reduce((a,b)=>a+b,0);
      // Favor primary lexical bases when relevance otherwise ties, without
      // making morphological productivity or native use claims.
      if(!row.w.components)rank+=7;
      return rank;
    }
    function find(query,{domain='',pos='',limit=80}={}){
      const q=fold(query),terms=unique(tokens(q));
      if(!q){
        const arr=docs.filter(x=>(!domain||x.w.domain===domain)&&(!pos||x.w.pos===pos));
        return {total:arr.length,results:arr.slice(0,Math.max(1,limit)).map(x=>x.w)};
      }
      const ranked=[];
      for(const row of docs){
        if((domain&&row.w.domain!==domain)||(pos&&row.w.pos!==pos))continue;
        const relevance=score(row,q,terms);
        if(relevance>=0)ranked.push({row,relevance});
      }
      ranked.sort((a,b)=>b.relevance-a.relevance||
        a.row.form.localeCompare(b.row.form)||a.row.w.id.localeCompare(b.row.w.id));
      return {total:ranked.length,results:ranked.slice(0,Math.max(1,limit)).map(x=>x.row.w)};
    }
    function related(form){
      const head=byForm.get(fold(form));
      if(!head)return {parts:[],compounds:[],sameGloss:[],neighbors:[],unsupportedAntonyms:true};
      const w=head.w,parts=[];
      for(const part of unique((w.components||'').split(/\s+\+\s+/).map(fold).filter(Boolean))){
        const item=byForm.get(part);
        parts.push({form:part,entry:item?.w||null});
      }
      const compounds=(reverse.get(head.form)||[])
        .sort((a,b)=>a.form.localeCompare(b.form)).map(x=>x.w);
      const sameGloss=(glosses.get(head.gloss)||[])
        .filter(x=>x.w.id!==w.id).slice(0,24).map(x=>x.w);
      // Topic neighbors are *not* synonyms. Prioritize shared independent
      // definitional tokens rather than random alphabetically-first entries.
      const orig=new Set(head.englishTokens.filter(isUseful));
      const neighbors=(byDomain.get(w.domain)||[]).filter(x=>x.w.id!==w.id && x.gloss!==head.gloss)
        .map(x=>({row:x,common:x.englishTokens.filter(t=>orig.has(t)&&isUseful(t)).length}))
        .filter(x=>x.common>0)
        .sort((a,b)=>b.common-a.common||a.row.form.localeCompare(b.row.form))
        .slice(0,10).map(x=>x.row.w);
      return {parts,compounds:compounds.slice(0,32),compoundTotal:compounds.length,
        sameGloss,neighbors,unsupportedAntonyms:true};
    }
    return Object.freeze({find,related,byId,byForm,size:docs.length,domains:byDomain.size,fold});
  }
  root.QaroshiDiscovery=Object.freeze({createIndex,fold});
})(typeof window!=='undefined'?window:globalThis);
