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
      ? {role:'assistant',content:'A cat is zekunga. [S1]'}
      : {role:'assistant',content:'<tool_call>lookup_dictionary</tool_call>'};
    return {ok:true,json:async () => ({choices:[{message}]})};
  }
};
vm.createContext(context);
vm.runInContext(code + '\nthis.search = assistantSources; this.request = assistantRequest;', context);
(async () => {
  const matches = context.search('Translate cat');
  const cat = matches.find(x => x.title === 'Dictionary: zekunga');
  assert(cat);
  const docs = [{...cat, id:'S1'}];
  assert.equal((await context.request('test-key','Translate cat',docs)), 'A cat is zekunga. [S1]');
  assert(requests[0].messages[1].content.includes('[S1] Dictionary: zekunga'));
  assert(!('tools' in requests[0]));
  await assert.rejects(context.request('test-key','Translate cat',docs), /did not return an answer/);
  console.log('Assistant dictionary lookup tests passed.');
})().catch(error => { console.error(error); process.exitCode = 1; });
