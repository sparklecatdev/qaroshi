const assert = require('node:assert/strict');
const fs = require('node:fs');
const vm = require('node:vm');

const page = fs.readFileSync('index.html', 'utf8');
const data = JSON.parse(page.match(/<script type="application\/json" id="wiki-data">([\s\S]*?)<\/script>/)[1]);
const js = fs.readFileSync('web/qaroshi.js', 'utf8');
const search = js.slice(js.indexOf('  let assistantIndex;'), js.indexOf('  function assistantDocument(html){'));
const context = {
  W: data.words, P: data.phrases,
  wordBy: new Map(data.words.map(w => [w.qaroshi.toLowerCase(), w])),
  enc: encodeURIComponent, form: x => x
};
vm.createContext(context);
vm.runInContext(search + '\nthis.search = assistantSources;', context);

function includesWords(query, words) {
  const results = context.search(query);
  for (const word of words) assert(results.some(r => r.title === 'Dictionary: ' + word), `${query}: missing ${word}`);
  assert(results.filter(r => r.kind === 'word').length <= 70);
  assert(results.filter(r => r.kind === 'phrase').length <= 30);
}

includesWords('Translate I loved cats into Qaroshi', ['mi', 'zekunga', 'nashi']);
includesWords('Translate sen qaro-ri-m daru-te', ['qaro', 'daru']);
includesWords('Translate goro-te-se', ['goro']);
includesWords('Translate gorotese', ['goro']);
includesWords('Translate you into Qaroshi', ['ti']);
console.log('Assistant dictionary retrieval tests passed.');
