# 数据模型与持久化参考

## pet 对象结构
```js
{
  id: 'p1',                       // 唯一 id，用 'p'+Date.now()
  name: '旺财',
  emoji: '🐕',
  species: '狗狗 · 中华田园',
  birthday: '2021-05-10',         // 可空
  feedings: [{date:'2026-07-07', food:'鸡胸肉+狗粮', amt:180}],
  vaccines: [{date:'2026-03-01', type:'狂犬', next:'2027-03-01'}],
  dewormings: [{date:'2026-05-28', type:'体内', cycle:30}],
  weights: [{date:'2026-03-01', kg:14.2}, {date:'2026-06-01', kg:15.1}]
}
```

## 字段用途
| 字段 | 用途 | 关键逻辑 |
|------|------|---------|
| `feedings` | 喂食记录 | `some(f=>f.date===todayStr())` 判断是否今日已喂 |
| `vaccines[].next` | 下次接种日 | `next < todayStr()` → 已到期 |
| `dewormings[].cycle` | 驱虫周期(天) | `days(date,today) > cycle` → 逾期 |
| `weights` | 体重轨迹 | 排序后画曲线，相邻算增量 |

## 时间工具
```js
function todayStr(){const d=new Date();return d.toISOString().slice(0,10);} // 注意：UTC 偏移
// 更稳妥（本地时区）：
function todayStr(){const d=new Date();const p=n=>String(n).padStart(2,'0');
  return `${d.getFullYear()}-${p(d.getMonth()+1)}-${p(d.getDate())}`;}
const days=(a,b)=>Math.floor((new Date(b)-new Date(a))/86400000);
```

## 持久化
```js
const KEY='petHealth.v1';
let pets=[], cur=null;
function save(){localStorage.setItem(KEY,JSON.stringify(pets));}
function load(){
  try{pets=JSON.parse(localStorage.getItem(KEY))||[];}catch(e){pets=[];}
  if(!pets.length) seed();      // 首次填充示例数据
  cur=pets[0];
}
function seed(){
  pets=[ /* 预置 1-2 只，一只逾期一只正常 */ ];
  save();
}
```

## 增删改模式
- 新增：`pets.push({...})` → `save()` → `renderAll()`
- 表单提交：`onsubmit` 里 `e.preventDefault()`，push 后 `save()+renderAll()`
- 切换宠物：`cur=pets[i]` → `renderAll()`
- 多宠物卡片用 `renderPets()` 重建，`cur.id===p.id` 标 active
