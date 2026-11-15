const assert = require('node:assert/strict');
const fs = require('node:fs');
const vm = require('node:vm');

const js = fs.readFileSync('web/qaroshi.js', 'utf8');
const code = js.slice(js.indexOf('  function assistantAnswerHTML('), js.indexOf('  function renderDictionary(route){'));
const elements = {};
for (const id of ['assistantForm','assistantSubmit','assistantStatus','assistantResult','assistantAnswer','assistantReferences','assistantQuery','assistantKey','assistantClearKey']) {
  elements[id] = {value:'', addEventListener(type, fn){this[type] = fn}};
}
const saved = new Map();
const storage = {getItem:k=>saved.get(k), setItem:(k,v)=>saved.set(k,v), removeItem:k=>saved.delete(k)};
const esc = s => String(s).replace(/[&<>"']/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
const context = {esc, localStorage:storage, $:id=>elements[id], main:{}, mkHeader:()=>'', setToc:()=>{},
  assistantSources:()=>[], assistantRequest:async()=> '**Answer:** <img src=x onerror=alert(1)> [G02]', C:[], D:{guides:{}}, assistantDocument:()=>'',
  fetch:async()=>({ok:true,json:async()=>({choices:[{message:{content:'**Answer:** <img src=x onerror=alert(1)> [G02]'}}]})})};
vm.createContext(context);
vm.runInContext(code+'\nthis.format=assistantAnswerHTML; this.render=renderAssistant;', context);
const formatted = context.format('**First sentence:**\n*Resonance:* **lën**\n\n---\n\n- one\n- two\n\n<script>alert(1)</script>');
assert(formatted.includes('<strong>First sentence:</strong>'));
assert(formatted.includes('<em>Resonance:</em> <strong>lën</strong>'));
assert(formatted.includes('<hr>'));
assert(formatted.includes('<ul><li>one</li><li>two</li></ul>'));
assert(formatted.includes('&lt;script&gt;'));
context.render();
elements.assistantKey.value = 'test-key';
elements.assistantKey.input();
context.render();
assert.equal(elements.assistantKey.value, 'test-key');
elements.assistantClearKey.click();
assert.equal(elements.assistantKey.value, '');
assert.equal(saved.size, 0);
elements.assistantKey.value = 'test-key';
elements.assistantQuery.value = 'question';
elements.assistantForm.submit({preventDefault(){}}).then(()=>{
  assert(elements.assistantAnswer.innerHTML.includes('<strong>Answer:</strong>'));
  assert(!elements.assistantAnswer.innerHTML.includes('<img'));
  console.log('Answer formatting and key storage tests passed.');
}).catch(error=>{console.error(error);process.exitCode=1});
