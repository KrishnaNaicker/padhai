#!/usr/bin/env node
// Padhai: pre-render $$display$$ and $inline$ math with KaTeX (offline, no browser JS needed).
// Usage: node render_math.js <in.html> <out.html>
// Requires the `katex` npm package (npm install katex, in this scripts folder or globally).
// Exit codes: 0 ok, 3 katex not installed, 1 a formula failed to parse (message says which).
const fs = require('fs');
const path = require('path');

let katex;
for (const base of [__dirname, process.cwd()]) {
  try { katex = require(require.resolve('katex', { paths: [base] })); break; } catch (e) { /* try next */ }
}
if (!katex) { try { katex = require('katex'); } catch (e) { console.error('katex-not-installed'); process.exit(3); } }

const [inp, out] = process.argv.slice(2);
let s = fs.readFileSync(inp, 'utf8');

// 1. Protect <pre>, <code>, <script>, <style> blocks: a "$" inside them is not math.
const kept = [];
s = s.replace(/<(pre|code|script|style)\b[\s\S]*?<\/\1>/gi, m => { kept.push(m); return `\u0000K${kept.length - 1}\u0000`; });
// 2. Escaped dollars stay literal.
s = s.replace(/\\\$/g, '\u0000DOLLAR\u0000');

const decode = t => t.replace(/&lt;/g, '<').replace(/&gt;/g, '>').replace(/&nbsp;/g, ' ').replace(/&amp;/g, '&');
function render(tex, display, whole) {
  try {
    return katex.renderToString(decode(tex), { displayMode: display, throwOnError: true, strict: 'ignore' });
  } catch (e) {
    console.error('MATH ERROR in: ' + whole.slice(0, 160).replace(/\s+/g, ' '));
    console.error('  ' + e.message.split('\n')[0]);
    process.exitCode = 1;
    return whole;
  }
}
s = s.replace(/\$\$([\s\S]+?)\$\$/g, (m, t) => render(t, true, m));
s = s.replace(/\$([^\$\n]+?)\$/g, (m, t) => render(t, false, m));

s = s.replace(/\u0000DOLLAR\u0000/g, '$');
s = s.replace(/\u0000K(\d+)\u0000/g, (m, i) => kept[+i]);
fs.writeFileSync(out, s);

// Tell the caller where KaTeX's CSS lives so it can be inlined.
try {
  const pkg = require.resolve('katex/package.json', { paths: [__dirname, process.cwd()] });
  console.log('KATEX_DIR=' + path.dirname(pkg));
} catch (e) { console.log('KATEX_DIR='); }
