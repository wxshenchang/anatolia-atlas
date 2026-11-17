#!/usr/bin/env node
/**
 * 数据完整性自检：把 README 里「每个条目都要有出处」的规则变成可执行检查。
 * 用法：node _build/check_data.js
 * 任何一项不通过 → 退出码 1（CI 会红）。
 */
'use strict';
const fs = require('fs');
const path = require('path');

const ROOT = path.join(__dirname, '..');
const sandbox = { window: {} };

function loadJs(rel) {
  const code = fs.readFileSync(path.join(ROOT, rel), 'utf8');
  // 只在本进程的假 window 上求值，不引入浏览器依赖
  const fn = new Function('window', 'document', 'self', code);
  fn(sandbox.window, undefined, sandbox.window);
  return sandbox.window;
}

function loadAtlasSnapshots() {
  const dir = path.join(ROOT, 'data', 'atlas');
  const snaps = [];
  for (const key of fs.readdirSync(dir)) {
    const f = path.join(dir, key, `s_${key}.geojson`);
    if (!fs.existsSync(f)) continue;
    const fc = JSON.parse(fs.readFileSync(f, 'utf8'));
    snaps.push({ key, count: fc.features ? fc.features.length : 0, fc });
  }
  return snaps;
}

const problems = [];
const warn = [];
const ok = (label, n) => console.log(`  ✓ ${label}: ${n}`);

function main() {
  const w = loadJs('js/map_data.js');
  loadJs('js/lore_core.js');

  const dynasties = w.DYNASTY_DATA || [];
  const corridors = w.CORRIDOR_DATA || [];
  const lore = w.ATLAS_LORE_DATA || {};
  const snaps = loadAtlasSnapshots();

  console.log('数据完整性自检\n');

  // ---- 时代 / 快照
  const phases = dynasties.reduce((a, d) => a + (d.phases || []).length, 0);
  ok('历史时代', dynasties.length);
  ok('时期快照（phases）', phases);
  ok('快照 geojson 目录', snaps.length);
  if (snaps.length !== phases) problems.push(`phases ${phases} 与 data/atlas 快照目录 ${snaps.length} 不一致`);

  // ---- 事件：必须有 source 与 detail
  let evTotal = 0;
  const evNoSrc = [];
  const evNoDetail = [];
  for (const d of dynasties) {
    for (const m of d.milestones || []) {
      evTotal++;
      if (!String(m.source || '').trim()) evNoSrc.push(`${d.key} ${m.year} ${m.headline}`);
      if (!String(m.detail || '').trim()) evNoDetail.push(`${d.key} ${m.year} ${m.headline}`);
    }
  }
  ok('历史事件', evTotal);
  if (evNoSrc.length) problems.push(`${evNoSrc.length} 条事件缺 source：${evNoSrc.slice(0, 5).join(' / ')}`);
  if (evNoDetail.length) problems.push(`${evNoDetail.length} 条事件缺 detail：${evNoDetail.slice(0, 5).join(' / ')}`);

  // ---- 聚落：必须有 source
  let settleTotal = 0;
  const settleNoSrc = [];
  for (const d of dynasties) {
    for (const s of d.settlements || []) {
      settleTotal++;
      if (!String(s.source || '').trim()) settleNoSrc.push(`${d.key} ${s.ancient}`);
      if (!Array.isArray(s.coord) || s.coord.length !== 2) problems.push(`聚落坐标异常：${s.ancient}`);
    }
  }
  ok('聚落', settleTotal);
  if (settleNoSrc.length) problems.push(`${settleNoSrc.length} 处聚落缺 source：${settleNoSrc.slice(0, 5).join(' / ')}`);

  // ---- 路线站点
  let stopTotal = 0;
  const stopNoSrc = [];
  for (const c of corridors) {
    for (const s of c.stops || []) {
      stopTotal++;
      if (!String(s.source || '').trim()) stopNoSrc.push(`${c.key} ${s.name}`);
    }
  }
  ok('旅行路线 / 站点', `${corridors.length} / ${stopTotal}`);
  if (stopNoSrc.length) problems.push(`${stopNoSrc.length} 个站点缺 source`);

  // ---- 政权档案：from/to/intro/source
  const info = lore.POLITY_INFO || [];
  const infoBad = info.filter(
    (r) => !Number.isFinite(r.from) || !Number.isFinite(r.to) || !String(r.intro || '').trim() || !String(r.source || '').trim()
  );
  ok('政权档案', info.length);
  if (infoBad.length) problems.push(`${infoBad.length} 条政权档案不完整：${infoBad.slice(0, 5).map((r) => r.name).join(' / ')}`);

  // ---- 宗教分期：[name, from, to, text, source]
  const spans = lore.RELIGION_SPANS || [];
  const spanBad = spans.filter((s) => !Array.isArray(s) || s.length < 5 || !String(s[4] || '').trim());
  ok('宗教分期', spans.length);
  if (spanBad.length) problems.push(`${spanBad.length} 条宗教分期缺出处`);

  // ---- 人物 / 关隘 / 地名志
  const persons = lore.PERSON_PROFILES || [];
  const personBad = persons.filter((p) => !String(p.source || '').trim());
  ok('人物', persons.length);
  if (personBad.length) problems.push(`${personBad.length} 位人物缺 source`);

  const passes = lore.STRATEGIC_PASSES || [];
  const passBad = passes.filter((p) => !String(p.source || '').trim());
  ok('关隘', passes.length);
  if (passBad.length) problems.push(`${passBad.length} 处关隘缺 source：${passBad.map((p) => p.ancientZh).join(' / ')}`);

  const gaz = lore.PLACE_GAZETTEER || [];
  const gazBad = gaz.filter((g) => !String(g.source || '').trim());
  ok('地名志', gaz.length);
  if (gazBad.length) problems.push(`${gazBad.length} 条地名志缺 source`);

  // ---- 每个画在图上的政权都要有档案与宗教（缺宗教需显式在白名单里）
  const RELIGION_EXEMPT = new Set(['卡什卡诸部']); // 仅赫梯单方文献，按「无考据不写」处理
  const drawn = new Set();
  for (const s of snaps) for (const f of s.fc.features || []) drawn.add(f.properties.title);
  const baseName = (n) => n.replace(/（.*?）/g, '');
  const infoNames = new Set(info.map((r) => r.name));
  const relNames = new Set(spans.map((s) => s[0]));
  const missingInfo = [...drawn].filter((n) => !infoNames.has(n) && !infoNames.has(baseName(n)));
  const missingRel = [...drawn].filter(
    (n) => !relNames.has(n) && !relNames.has(baseName(n)) && !RELIGION_EXEMPT.has(n)
  );
  ok('图上政权', drawn.size);
  if (missingInfo.length) problems.push(`${missingInfo.length} 个图上政权没有档案：${missingInfo.slice(0, 6).join(' / ')}`);
  if (missingRel.length) problems.push(`${missingRel.length} 个图上政权没有宗教分期：${missingRel.slice(0, 6).join(' / ')}`);

  // ---- 快照不能是空的
  for (const s of snaps) if (!s.count) problems.push(`快照 ${s.key} 没有任何政权要素`);

  // ---- 事件地点不能明显飞到大洋里（粗检经纬度范围）
  for (const d of dynasties) {
    for (const m of d.milestones || []) {
      const [lng, lat] = m.coord || [];
      if (!Number.isFinite(lng) || !Number.isFinite(lat) || lng < -180 || lng > 180 || lat < -90 || lat > 90) {
        problems.push(`事件坐标异常：${m.headline}`);
      } else if (lng < 20 || lng > 52 || lat < 22 || lat > 48) {
        warn.push(`事件在图外（正常，会锚定都城）：${m.year} ${m.headline}`);
      }
    }
  }

  console.log('');
  if (warn.length) console.log(`ℹ 提示 ${warn.length} 条（不算失败）`);
  if (problems.length) {
    console.error('\n✗ 自检失败：');
    for (const p of problems) console.error('  - ' + p);
    process.exit(1);
  }
  console.log('✓ 全部通过：事件/政权/宗教/聚落/人物/关隘/地名志 都有出处，图上政权都有档案。');
}

main();
