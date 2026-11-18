/* Source-bound Wiki Standard 11 rendering and injection tests. */
const fs=require('node:fs'),assert=require('node:assert/strict'),vm=require('node:vm');
const js=fs.readFileSync('web/wiki_standard11.js','utf8');
const scope={window:{}};vm.runInNewContext(js,scope);
const W=scope.window.Qaroshi11;
assert.equal(typeof W.create,'function');
const item={
 id:'S28-001',left:'nashi',right:'mali',left_gloss:'cherish',right_gloss:'romance',
 semantic_boundary:'care versus romance',source_status:'existing editorial boundary',
 learner_question:'What is actually asserted?',explanation:'Care does not imply romance.',
 forbidden_inference:'Do not infer romantic consent.'
};
const exercise={
 id:'D31-01',topic:'self_correction',rule:'Repair a claim.',
 preferred_or_documented_example:'sen mi haro.',contrast_or_omission:'',
 scope_note:'The new claim must be expressed.',status:'existing rule',
 training:{scenario:'Misunderstood',question:'What changed?',
 editorial_answer:'The proposition changed.'}
};
const api=W.create({standard11:{contrasts:[item],conversation_rules:[exercise]}});
assert.match(api.renderContrast(item),/#word\/nashi/);
assert.match(api.renderContrast(item),/Reveal editorial explanation/);
assert.match(api.renderRule(exercise),/Reveal editorial answer/);
assert.match(api.renderRule(exercise),/sen mi haro/);
const malicious={...item,explanation:'<img src=x onerror="alert(1)">',left:'<script>'};
const escaped=api.renderContrast(malicious);
assert(!escaped.includes('<img src=x'));
assert(!escaped.includes('<script>'));
assert(escaped.includes('&lt;img'));
assert(escaped.includes('&lt;script&gt;'));
console.log('standard11 UI: contrast, source usage, reveal, escaping passed');
