import fs from 'node:fs';

const component = fs.readFileSync(new URL('../components/parallax-home.tsx', import.meta.url), 'utf8');
const css = fs.readFileSync(new URL('../app/globals.css', import.meta.url), 'utf8');

const requirements = [
  ['single cinematic track', component.includes('className="experience-track"')],
  ['single sticky stage', component.includes('className="experience-stage"')],
  ['continuous progress variable', component.includes('"--p"')],
  ['overlapping story phase', component.includes('"--story"')],
  ['overlapping organize phase', component.includes('"--organize"')],
  ['overlapping law phase', component.includes('"--law"')],
  ['overlapping document phase', component.includes('"--docs"')],
  ['finale phase', component.includes('"--finale"')],
  ['pointer depth', component.includes('"--mx"') && component.includes('"--my"')],
  ['one long scroll track', css.includes('height:650vh')],
  ['sticky viewport', css.includes('.experience-stage') && css.includes('position:sticky')],
  ['reduced-motion fallback', css.includes('@media (prefers-reduced-motion: reduce)')],
];

const failed = requirements.filter(([, ok]) => !ok);
if (failed.length) {
  for (const [name] of failed) console.error(`FAIL landing v5 — ${name}`);
  process.exit(1);
}

if (component.includes('data-parallax-scene') || component.includes('className="parallax-scene')) {
  console.error('FAIL landing v5 — old stacked-scene architecture still present in component.');
  process.exit(1);
}

const sceneSections = [...component.matchAll(/<section/g)].length;
if (sceneSections > 2) {
  console.error(`FAIL landing v5 — expected at most cinematic track + proof section, found ${sceneSections} sections.`);
  process.exit(1);
}

console.log('PASS landing v5 — one sticky cinematic world, continuous progress, overlapping phases, pointer depth, and reduced-motion fallback verified.');
