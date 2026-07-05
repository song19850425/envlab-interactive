#!/usr/bin/env python3
"""EnvLab 一键部署脚本
用法:
  python deploy.py github       # 推送到 GitHub Pages
  python deploy.py cos          # 同步到腾讯云 COS
  python deploy.py both         # 同时推送到两个平台

要求:
  pip install coscmd  (仅 COS 需要)
  git 已配置远程仓库  (仅 GitHub 需要)
"""
import os, sys, subprocess, json

SRC = os.path.dirname(os.path.abspath(__file__))
CONFIG = os.path.join(SRC, ".deploy_config.json")

GUIDE = """使用方法：

【方式一：GitHub Pages · 免费】
1. 在 GitHub 新建仓库（如 envlab）
2. 在终端执行：
   cd "EnvLab-叙事升级版"
   git init
   git add .
   git commit -m "初始部署"
   git remote add origin https://github.com/你的用户名/envlab.git
   git push -u origin main
3. 在 GitHub 仓库 Settings → Pages → 选择 main 分支 → Save
4. 等待 2 分钟，访问 https://你的用户名.github.io/envlab

【方式二：腾讯云 COS · ≈¥3-5/月】
1. 登录腾讯云 → 对象存储 → 创建 Bucket（选择公有读）
2. 开启「静态网站」配置
3. 安装工具：
   pip install coscmd
   coscmd config -a 你的SecretId -s 你的SecretKey -b Bucket名 -r ap-xxx
4. 同步文件：
   coscmd upload -r ./ "文件夹名/"
5. 访问生成的静态网站域名

【方式三：WorkBuddy CloudStudio】
用 WorkBuddy 内置的 cloudstudio-deploy 技能
"""

def check_github():
    """检查是否有 git 和远程仓库"""
    try:
        r = subprocess.run(["git", "remote", "-v"], capture_output=True, text=True, cwd=SRC)
        if r.returncode == 0 and r.stdout.strip():
            print(f"✅ Git 远程仓库已配置:\n{r.stdout}")
            return True
        else:
            print("⚠️  未检测到 Git 远程仓库")
            print("请先创建 GitHub 仓库并关联:")
            print(f"  cd \"{SRC}\"")
            print('  git remote add origin https://github.com/你的用户名/envlab.git')
            return False
    except FileNotFoundError:
        print("❌ 未安装 Git，请先安装 https://git-scm.com")
        return False

def check_cos():
    """检查是否有 coscmd"""
    r = subprocess.run(["coscmd", "--version"], capture_output=True, text=True)
    if r.returncode == 0:
        print(f"✅ coscmd 已安装: {r.stdout.strip()}")
        return True
    else:
        print("❌ 未安装 coscmd，请执行: pip install coscmd")
        print("然后配置: coscmd config -a SecretId -s SecretKey -b Bucket -r 区域")
        return False

def deploy_github():
    print("\n" + "="*50)
    print("🚀 部署到 GitHub Pages")
    print("="*50)
    if not check_github():
        return
    for cmd, desc in [
        (["git", "add", "."], "添加文件..."),
        (["git", "commit", "-m", f"部署更新 {__import__('datetime').datetime.now().strftime('%Y-%m-%d %H:%M')}"], "提交..."),
        (["git", "push", "-u", "origin", "main"], "推送到 GitHub..."),
    ]:
        print(f"  → {desc}")
        r = subprocess.run(cmd, capture_output=True, text=True, cwd=SRC)
        if r.returncode != 0:
            print(f"  ❌ 失败: {r.stderr.strip()}")
            return
    print("  ✅ 推送成功！等待 2 分钟访问你的 GitHub Pages 链接")

def deploy_cos():
    print("\n" + "="*50)
    print("🚀 同步到腾讯云 COS")
    print("="*50)
    if not check_cos():
        return
    print("  → 同步文件中...")
    r = subprocess.run(["coscmd", "upload", "-r", ".", "/"], capture_output=True, text=True, cwd=SRC)
    if r.returncode != 0:
        print(f"  ❌ 失败: {r.stderr.strip()}")
        return
    print("  ✅ COS 同步完成！")

if __name__ == "__main__":
    if len(sys.argv) < 2 or sys.argv[1] not in ("github", "cos", "both", "help"):
        print(GUIDE)
        sys.exit(0)

    if sys.argv[1] in ("github", "both"):
        deploy_github()
    if sys.argv[1] in ("cos", "both"):
        deploy_cos()
    print("\n💡 更多部署选项请执行: python deploy.py help")
