import fs from 'fs';
const src = fs.readFileSync('/home/user/saif/js/app.js','utf8');
const start = src.indexOf('/* ============ 5) محاكي');
const end = src.indexOf('/* ============ 6)');
const math = src.slice(start,end);
// stub minimal DOM helpers used in that block
const ctx = {};
const fn = new Function('$','$$','mm','document','window', math + `
  return {MATS,apply1,applyCNOT,applySWAP,measure,initState,fmtState,sameState,quirkUrl,cmul};
`);
const M = fn(()=>null, ()=>[], null, {}, {});
const S2=Math.SQRT1_2;
let pass=0, fail=0, log=[];
const t=(name,cond,extra='')=>{ if(cond){pass++;} else {fail++; log.push('FAIL: '+name+' '+extra);} };
const close=(a,b,e=1e-9)=>Math.abs(a-b)<e;
const eq=(s,exp,msg)=>{ const ok=s.length===exp.length && s.every((v,i)=>close(Math.abs(v[0]),Math.abs(exp[i][0]),1e-6) && close(Math.abs(v[1]),Math.abs(exp[i][1]),1e-6)); t(msg,ok,JSON.stringify(s)); };

// 1) state norm and init
let s=M.initState(1); t('init state |0>', s[0][0]===1 && s[1][0]===0);
// 2) X flips
eq(M.apply1(s,1,'X',0), [[0,0],[1,0]], 'X|0> = |1>');
// 3) H creates |+>
let hp=M.apply1(s,1,'H',0); t('H|0> amplitudes 1/sqrt2', close(hp[0][0],S2)&&close(hp[1][0],S2));
// 4) H^2 = I
let hh=M.apply1(hp,1,'H',0); t('H^2 = I', close(hh[0][0],1)&&close(hh[1][0],0));
// 5) Z phase
let zp=M.apply1(hp,1,'Z',0); t('Z|+> = |->', close(zp[1][0],-S2));
// 6) S phase i
let sp=M.apply1(hp,1,'S',0); t('S|+> amplitude i on |1>', close(sp[1][1],S2)&&close(sp[1][0],0));
// 7) T phase
let tp=M.apply1(hp,1,'T',0); t('T phase pi/4', close(tp[1][0],S2*Math.cos(Math.PI/4),1e-9)&&close(tp[1][1],S2*Math.sin(Math.PI/4),1e-9));
// 8) Y
let yp=M.apply1(s,1,'Y',0); t('Y|0> = i|1>', close(yp[1][1],1));
// 9) CNOT truth table (4 cases)
{
  let ok=true;
  const states=[[ [1,0],[0,0] ],[[0,0],[1,0]],[[1,0],[0,0]],[[0,0],[1,0]]];
  // build 2-qubit basis states and check CNOT mapping
  const names=['00','01','10','11'];
  const expIdx={ '00':0,'01':1,'10':3,'11':2 };
  for(let i=0;i<4;i++){
    let st=Array(4).fill(0).map(()=>[0,0]); st[i]=[1,0];
    let out=M.applyCNOT(st,2,0,1);
    if(!close(out[expIdx[names[i]]][0],1)) ok=false;
  }
  t('CNOT maps all 4 basis states correctly',ok);
}
// 10) Bell state
{
  let st=M.initState(2); st=M.apply1(st,2,'H',0); st=M.applyCNOT(st,2,0,1);
  const bell=[[S2,0],[0,0],[0,0],[S2,0]];
  t('H+CNOT produces Bell state', M.sameState(st,bell));
}
// 11) SWAP
{
  let st=M.initState(2); st=M.apply1(st,2,'X',0); // |10>
  st=M.applySWAP(st,2,0,1); // -> |01>
  t('SWAP swaps |10> to |01>', close(st[1][0],1)&&close(st[2][0],0));
}
// 12) Measurement statistics (2000 shots on H) within 5%
{
  let st=M.apply1(M.initState(1),1,'H',0); let z=0;
  for(let i=0;i<2000;i++){ if(M.measure(st,1).value==='0') z++; }
  t('measurement ~50/50 (2000 shots)', Math.abs(z/2000-0.5)<0.05, 'got '+z/2000);
}
// 13) normalisation after random circuits
{
  let ok=true;
  for(const g of ['X','Y','Z','H','S','T']){
    let st=M.apply1(M.initState(1),1,g,0);
    const n=st.reduce((a,v)=>a+v[0]*v[0]+v[1]*v[1],0);
    if(Math.abs(n-1)>1e-9) ok=false;
  }
  t('norm preserved for all single-qubit gates',ok);
}
// 14) quirk url encodes
{
  const u=M.quirkUrl([['H'],['Measure']]);
  t('quirk url built', u.startsWith('https://algassert.com/quirk#circuit='));
}

// 15) X twice = identity
t('X^2 = I', (()=>{let s=M.apply1(M.apply1(M.initState(1),1,'X',0),1,'X',0); return close(s[0][0],1);})());
// 16) S^2 = Z
t('S^2 = Z', (()=>{let a=M.apply1(M.apply1(M.initState(1),1,'H',0),1,'Z',0); let b=M.apply1(M.apply1(M.apply1(M.initState(1),1,'H',0),1,'S',0),1,'S',0); return M.sameState(a,b);})());
// 17) T^2 = S
t('T^2 = S', (()=>{let a=M.apply1(M.apply1(M.apply1(M.initState(1),1,'H',0),1,'T',0),1,'T',0); let b=M.apply1(M.apply1(M.initState(1),1,'H',0),1,'S',0); return M.sameState(a,b);})());
// 18) CNOT twice = identity
t('CNOT^2 = I', (()=>{let s=M.initState(2); s=M.apply1(s,2,'H',0); let before=s.map(v=>[v[0],v[1]]); s=M.applyCNOT(s,2,0,1); s=M.applyCNOT(s,2,0,1); return M.sameState(before,s);})());
// 19) SWAP twice = identity
t('SWAP^2 = I', (()=>{let s=M.initState(2); s=M.apply1(s,2,'X',0); s=M.applySWAP(s,2,0,1); s=M.applySWAP(s,2,0,1); return close(s[2][0],1);})());
// 20) H on both qubits gives 4 equal amplitudes
t('H on 2 qubits = 4 equal amplitudes', (()=>{let s=M.initState(2); s=M.apply1(s,2,'H',0); s=M.apply1(s,2,'H',1); return s.every(v=>close(Math.abs(v[0]),0.5));})());
console.log(JSON.stringify({pass,fail,log},null,1));

