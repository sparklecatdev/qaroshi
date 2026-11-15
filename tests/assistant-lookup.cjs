const assert = require('node:assert/strict');
const fs = require('node:fs');
const vm = require('node:vm');
const page = fs.readFileSync('index.html', 'utf8');
const data = JSON.parse(page.match(/<script type="application\/json" id="wiki-data">([\s\S]*?)<\/script>/)[1]);
const js = fs.readFileSync('web/qaroshi.js', 'utf8');
const code = js.slice(js.indexOf('  let assistantIndex;'), js.indexOf('  function assistantDocument(html){'));
const requests = [];
const context = {
  W: data.words, P: data.phrases,
  wordBy: new Map(data.words.map(w => [w.qaroshi.toLowerCase(), w])),
  enc: encodeURIComponent, form: x => x,
  fetch: async (url, options) => {
    requests.push(JSON.parse(options.body));
    const message = requests.length === 1
      ? {role:'assistant', content:null, tool_calls:[{id:'call1',type:'function',function:{name:'lookup_dictionary',arguments:JSON.stringify({query:'cat'})}}]}
      : {role:'assistant',content:'A cat is zekunga. [S1]'};
    return {ok:true,json:async () => ({choices:[{message}]})};
  }
};
vm.createContext(context);
vm.runInContext(code + '\nthis.lookup = assistantLookup; this.request = assistantRequest;', context);
(async () => {
  const docs = [];
  assert.equal((await context.request('test-key','Translate cat',docs)), 'A cat is zekunga. [S1]');
  const result = JSON.parse(requests[1].messages.at(-1).content);
  assert(result.results.some(x => x.title === 'Dictionary: zekunga'));
  assert(docs.some(x => x.title === 'Dictionary: zekunga' && result.results.some(r => r.id === x.id)));
  const count = docs.length;
  context.lookup('cat',docs);
  assert.equal(docs.length,count);
  assert(context.lookup('',docs).error);
  console.log('Assistant dictionary lookup tests passed.');
})().catch(error => { console.error(error); process.exitCode = 1; });
