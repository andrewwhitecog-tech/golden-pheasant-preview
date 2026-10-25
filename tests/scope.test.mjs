import test from 'node:test';import assert from 'node:assert/strict';import {buildScope} from '../scope.mjs';
const base={kind:'cleaning',width:'12',height:'8',count:'2',openings:'12',year:'2000',repair:'no'};
test('net rectangular area accounts for count and exclusions',()=>{const r=buildScope(base);assert.equal(r.area,180);assert.equal(r.flags.length,0);assert.match(r.summary,/No price, bid, booking/);});
test('rejects missing, negative and nonfinite dimensions',()=>{for(const width of ['', '-1','Infinity','abc'])assert.ok(buildScope({...base,width}).errors.width);});
test('rejects fractional surface count',()=>assert.ok(buildScope({...base,count:'1.5'}).errors.count));
test('rejects excluded area equal to or greater than gross',()=>{for(const openings of ['192','200'])assert.ok(buildScope({...base,openings}).errors.openings);});
test('future work gets planning boundary',()=>{for(const kind of ['painting','mural'])assert.match(buildScope({...base,kind}).flags.join(' '),/not open for booking/);});
test('old property and repair needs receive review notes',()=>{const r=buildScope({...base,year:'1960',repair:'yes'});assert.equal(r.flags.length,2);assert.match(r.summary,/qualified professional/);});
test('unknown year is explicit and does not invent a date',()=>assert.match(buildScope({...base,year:''}).summary,/year is unknown/));
test('invalid choices are rejected',()=>{assert.ok(buildScope({...base,kind:'<script>'}).errors.kind);assert.ok(buildScope({...base,repair:'maybe'}).errors.repair);});
test('decimal measurements retain a useful tenth',()=>assert.equal(buildScope({...base,width:'10.5',height:'8.2',count:'1',openings:'0'}).area,86.1));

test('small positive surface stays positive and visible in summary',()=>{const r=buildScope({kind:'cleaning',width:0.1,height:0.1,count:1,openings:0,year:2000,repair:'no'});assert.equal(r.ok,true);assert.equal(r.area,0.01);assert.match(r.summary,/0\.01 sq ft/);});
