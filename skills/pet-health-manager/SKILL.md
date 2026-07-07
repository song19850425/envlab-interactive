---
name: pet-health-manager
description: 当用户需要创建移动端宠物健康管理工具、宠物记录 App、或"喂食/疫苗/驱虫/体重追踪 + 逾期自动提醒"类应用时加载。适用于把宠物健康/育儿/植物养护等"记录 + 周期提醒"场景做成可分享的单文件交互 HTML，并配套 WorkBuddy 自动化做主动提醒。
agent_created: true
version: 1.0.0
---

# 宠物健康管家 · 移动端交互式健康管理 Skill

## 触发条件
- 用户想做宠物/育儿/植物等的健康管理工具，尤其提到"喂食、疫苗、驱虫、体重、提醒"
- 用户要一个"不用上架 App、扫码即用、手机能加主屏"的轻量工具
- 用户已有 EnvLab 类交互页，想复制同款"单文件 HTML + localStorage + 移动端适配"模式
- 用户想把"超时未驱虫→自动提醒"做成主动推送（WorkBuddy automation）

## 核心架构（MVP，零后端）
单文件 HTML，数据存浏览器 `localStorage`，部署到 GitHub Pages 后甩链接即用。

```
宠物健康管家.html
├─ 移动端 CSS（视口锁定 + 媒体查询 + DPR 高清曲线）
├─ 数据模型（pet 对象数组，localStorage 持久化）
├─ 4 个模块：喂食 / 疫苗 / 驱虫 / 体重
├─ 仪表盘（逾期扫描 + 关键指标）
└─ 体重曲线（Canvas + DPR 重绘）
```

## 工作流

### 第 1 步：确认场景与对象模型
- 对象（宠物/孩子/植物）的字段：名字、emoji、品种/描述、生日
- 4 类记录字段（按需增删）：
  - 喂食：`{date, food, amt}`
  - 疫苗：`{date, type, next}`（next=下次到期日）
  - 驱虫：`{date, type, cycle}`（cycle=周期天数，用于算逾期）
  - 体重：`{date, kg}`
- 所有记录挂在 `pet` 对象下，多宠物用数组 + 当前选中 `cur`

### 第 2 步：写 HTML（移动端优先）
关键 CSS（务必带）：
```css
<meta name="viewport" content="width=device-width,initial-scale=1,maximum-scale=1,user-scalable=no">
* { box-sizing:border-box; -webkit-tap-highlight-color:transparent }
/* 表单输入字号 ≥16px 防止 iOS 聚焦缩放；按钮 min-height≥46px 好点 */
```
- 标签栏 `position:sticky;top:0` 吸顶，单手好操作
- 表格 `overflow-x:auto` 防溢出
- 暗色主题配色（用户偏好赛博朋克）：bg `#0e1117`、pink `#e8255a`、blue `#3b82f6`、green `#22c55e`、amber `#f59e0b`、red `#ef4444`

### 第 3 步：localStorage 持久化
```js
const KEY='petHealth.v1';
function save(){localStorage.setItem(KEY,JSON.stringify(pets));}
function load(){try{pets=JSON.parse(localStorage.getItem(KEY))||[];}catch(e){pets=[];}if(!pets.length)seed();}
// seed() 预置 1-2 只示例宠物，让首次打开就有内容
```

### 第 4 步：逾期扫描（核心卖点）
```js
const days=(a,b)=>Math.floor((new Date(b)-new Date(a))/86400000);
function checkOverdue(pet){
  const d=pet.dewormings.at(-1);
  if(d){const diff=days(d.date,todayStr()); if(diff>d.cycle) return `驱虫已超时 ${diff-d.cycle} 天`; }
  const v=pet.vaccines.at(-1);
  if(v&&v.next&&v.next<todayStr()) return `疫苗已到期`;
  return null;
}
```
- 仪表盘顶部用红色 alert 展示逾期项；宠物卡片角标用 ok/warn 状态
- **这是留存钩子**：用户每周打开都被"催"，形成 Track-on-Time 习惯闭环

### 第 5 步：体重曲线（高清）
```js
const dpr=window.devicePixelRatio||1, cssW=cv.clientWidth, cssH=220;
cv.width=cssW*dpr; cv.height=cssH*dpr; ctx.setTransform(dpr,0,0,dpr,0,0);
// X 按索引均分，Y 按 kg 范围映射；<2 个点提示"记录至少 2 条后显示"
```

### 第 6 步：部署成可分享链接
- 推到 GitHub Pages（已有 EnvLab 仓库可在 `pet/` 子目录放一份）
- 链接形如 `https://song19850425.github.io/envlab-interactive/pet/pet-health-manager.html`
- 用户手机打开 → 右上角"···"→ 添加到主屏幕 → 全屏像 App
- 数据只存用户自己手机，**不上传服务器**（隐私卖点）

### 第 7 步（可选）：主动提醒自动化
把"被动提醒"升级为"主动推送"——创建 WorkBuddy automation（每周日跑）：
1. 扫描记录中 `days(last, today) > cycle` 的宠物
2. 生成"本周该驱虫清单"文案
3. 你（或接微信/短信后自动）转发给对应主人
- 参考 `references/reminder-automation.md`

## 分发与商业化
```
L1 佣金：驱虫药/疫苗 CPS 分润（零库存，ARPU ¥20-60/年）
L2 会员：多宠管理 + 报告解读 + 问诊入口（¥99/年）
L3 B端：宠物医院 SaaS 引流工具（按门店收费）
```
详情见 `references/business-model.md`。完整可运行示例见 `examples/pet-health-manager.html`。

## 输入 / 输出
- **输入**：场景描述（宠物/育儿/植物）+ 要追踪的字段
- **输出**：自包含单文件 HTML（移动端可用）+ 可选 automation 配置
