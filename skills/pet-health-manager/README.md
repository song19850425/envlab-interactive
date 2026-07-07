# 🐾 宠物健康管家 · Pet Health Manager Skill

把"喂食 / 疫苗 / 驱虫 / 体重追踪 + 逾期自动提醒"做成**移动端可分享的单文件交互 HTML**，零后端、扫码即用。

## 干什么用
- 宠物主记录日常健康数据，手机加到主屏像 App 一样用
- 驱虫/疫苗到期自动提醒（留存钩子）
- 体重曲线可视化
- 配套 WorkBuddy automation 做每周主动提醒

## 目录结构
```
pet-health-manager/
├── SKILL.md                      # 核心工作流（触发 + 7 步）
├── gotchas.md                    # 10 条实战失败案例
├── references/
│   ├── data-model.md             # pet 对象模型 + localStorage
│   ├── reminder-automation.md    # 逾期主动提醒 automation 设计
│   └── business-model.md         # 商业化路径（L1→L3）
└── examples/
    └── pet-health-manager.html   # 完整可运行 Demo
```

## 快速体验
打开 `examples/pet-health-manager.html` 即可。预置两只宠物（旺财🐕 驱虫逾期、咪咪🐱 正常）。

## 在线 Demo
https://song19850425.github.io/envlab-interactive/pet/pet-health-manager.html

## 核心特性
- ✅ 移动端优先（视口锁定 + 表单 16px + 标签吸顶）
- ✅ 数据存浏览器本地（localStorage），不上传服务器（隐私友好）
- ✅ 体重曲线按设备像素比高清重绘
- ✅ 逾期扫描逻辑可复制到育儿/植物养护等任意"记录+周期提醒"场景

## 部署
推到 GitHub Pages 任意子目录即可，甩链接给用户，引导"添加到主屏幕"。

## 商业化
| 阶段 | 模式 |
|------|------|
| L1 | 驱虫药/疫苗 CPS 分润（零库存） |
| L2 | 多宠会员 ¥99/年 |
| L3 | 宠物医院 SaaS 引流 |

详见 `references/business-model.md`。
