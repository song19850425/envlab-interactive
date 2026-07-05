#!/usr/bin/env python3
"""
54项业务叙事法 · 公众号推文自动发布到草稿箱

使用方法：
  1. 在下方填入你的 AppID 和 AppSecret
  2. 在微信公众平台后台「设置与开发 - IP白名单」中添加本机IP
  3. python3 push_to_wechat.py
  4. 登录公众号后台 → 草稿箱 → 预览 → 发布
"""

import json, os, sys, time, re
import urllib.request
import urllib.error

# ═══════════════════════════════════════
# 配置区（填入你的信息）
# ═══════════════════════════════════════
APPID = "wx2ac3bee14a9c5b3f"
APPSECRET = "f3e87ffd19d9039f2d3bb76a633e7229"
ARTICLE_HTML = "C:/Users/jingh/WorkBuddy/20260326095724/EnvLab-叙事升级版/每周政策更新_2026-07-05.html"
COVER_IMAGE = "C:/Users/jingh/WorkBuddy/20260326095724/EnvLab-叙事升级版/cover_policy_0705.png"
# ═══════════════════════════════════════

TOKEN_CACHE = "token_cache.json"

def log(msg):
    print(f"[{time.strftime('%H:%M:%S')}] {msg}")

def get_access_token():
    """获取或缓存 access_token"""
    if os.path.exists(TOKEN_CACHE):
        with open(TOKEN_CACHE) as f:
            cache = json.load(f)
        if time.time() - cache["ts"] < 7000:
            log("使用缓存的 access_token")
            return cache["token"]
    
    url = (f"https://api.weixin.qq.com/cgi-bin/token"
           f"?grant_type=client_credential&appid={APPID}&secret={APPSECRET}")
    resp = json.loads(urllib.request.urlopen(url, timeout=15).read())
    if "access_token" not in resp:
        raise Exception(f"获取 token 失败: {resp}")
    token = resp["access_token"]
    json.dump({"token": token, "ts": time.time()}, open(TOKEN_CACHE, "w"))
    log("获取新的 access_token 成功")
    return token

def upload_image(token, img_path):
    """上传图片为永久素材，返回URL"""
    url = f"https://api.weixin.qq.com/cgi-bin/material/add_material?access_token={token}&type=image"
    import http.client
    boundary = "----WebKitFormBoundary7MA4YWxkTrZu0gW"
    with open(img_path, "rb") as f:
        img_data = f.read()
    body = (
        f"--{boundary}\r\n"
        f'Content-Disposition: form-data; name="media"; filename="{os.path.basename(img_path)}"\r\n'
        f"Content-Type: image/png\r\n\r\n"
    ).encode("utf-8") + img_data + f"\r\n--{boundary}--\r\n".encode("utf-8")
    
    req = urllib.request.Request(url, data=body)
    req.add_header("Content-Type", f"multipart/form-data; boundary={boundary}")
    resp = json.loads(urllib.request.urlopen(req, timeout=30).read())
    if "url" not in resp:
        raise Exception(f"上传图片失败: {resp}")
    log(f"图片上传成功: {resp['url']}")
    return resp["url"]

def upload_thumb(token, img_path):
    """上传封面为永久素材，返回media_id"""
    url = f"https://api.weixin.qq.com/cgi-bin/material/add_material?access_token={token}&type=image"
    import http.client
    boundary = "----WebKitFormBoundary7MA4YWxkTrZu0gW"
    with open(img_path, "rb") as f:
        img_data = f.read()
    body = (
        f"--{boundary}\r\n"
        f'Content-Disposition: form-data; name="media"; filename="{os.path.basename(img_path)}"\r\n'
        f"Content-Type: image/png\r\n\r\n"
    ).encode("utf-8") + img_data + f"\r\n--{boundary}--\r\n".encode("utf-8")
    
    req = urllib.request.Request(url, data=body)
    req.add_header("Content-Type", f"multipart/form-data; boundary={boundary}")
    resp = json.loads(urllib.request.urlopen(req, timeout=30).read())
    if "media_id" not in resp:
        raise Exception(f"上传封面失败: {resp}")
    log(f"封面上传成功: {resp['media_id']}")
    return resp["media_id"]

def html_to_wechat_text(html):
    """将HTML文章转换为微信公众号支持的格式"""
    # 提取标题
    title_match = re.search(r'<h1[^>]*>(.+?)</h1>', html, re.DOTALL)
    title = title_match.group(1).strip() if title_match else "EnvLab 文章"
    title = re.sub(r'<[^>]+>', '', title)
    title = re.sub(r'\s+', '', title)[:64]
    
    # 提取正文（纯文本，带基本样式）
    body = html
    
    # 替换图片标签 - 保留img但src需替换为微信CDN
    # 这里只做文本清理
    body = re.sub(r'<script[^>]*>.*?</script>', '', body, flags=re.DOTALL)
    body = re.sub(r'<style[^>]*>.*?</style>', '', body, flags=re.DOTALL)
    body = re.sub(r'<!DOCTYPE[^>]*>', '', body)
    body = re.sub(r'<html[^>]*>', '', body)
    body = re.sub(r'</html>', '', body)
    body = re.sub(r'<head[^>]*>.*?</head>', '', body, flags=re.DOTALL)
    
    # 保持基本排版标签
    allowed_tags = ['p','br','strong','b','em','i','u','a','img','span','div',
                    'h1','h2','h3','h4','h5','h6','ul','ol','li','table','tr','td','th',
                    'blockquote','code','pre','hr','section']
    for tag in ['html','head','body','meta','link','style','script']:
        body = re.sub(f'<{tag}[^>]*>', '', body, flags=re.DOTALL)
        body = re.sub(f'</{tag}>', '', body, flags=re.DOTALL)
    
    # 生成摘要（限120字）
    digest = re.sub(r'<[^>]+>', '', body).strip()[:120]
    digest = digest.replace('\n', '').replace('\r', '')
    
    return title, body, digest

def push_draft(token, article):
    """推送草稿到公众号"""
    url = f"https://api.weixin.qq.com/cgi-bin/draft/add?access_token={token}"
    payload = {"articles": [article]}
    data = json.dumps(payload, ensure_ascii=False).encode("utf-8")
    req = urllib.request.Request(url, data=data)
    req.add_header("Content-Type", "application/json; charset=utf-8")
    resp = json.loads(urllib.request.urlopen(req, timeout=30).read())
    if "media_id" not in resp:
        raise Exception(f"推送草稿失败: {resp}")
    return resp["media_id"]

def main():
    if APPID == "your_appid_here":
        log("❌ 请先在脚本中填入你的 AppID 和 AppSecret")
        sys.exit(1)
    
    # 1. 读取文章
    if ARTICLE_HTML and os.path.exists(ARTICLE_HTML):
        html_path = ARTICLE_HTML
    else:
        html_path = input("请输入公众号文章 HTML 文件路径: ").strip()
    
    if not os.path.exists(html_path):
        log(f"❌ 文件不存在: {html_path}")
        sys.exit(1)
    
    with open(html_path, encoding="utf-8") as f:
        html_content = f.read()
    
    log(f"✅ 读取文章: {html_path}")
    
    # 2. 获取 token
    token = get_access_token()
    
    # 3. 上传封面图（如果有）
    thumb_media_id = None
    if COVER_IMAGE and os.path.exists(COVER_IMAGE):
        log(f"上传封面中: {COVER_IMAGE}")
        thumb_media_id = upload_thumb(token, COVER_IMAGE)
        log(f"封面 media_id: {thumb_media_id}")
    else:
        log(f"封面文件不存在或未设置: {COVER_IMAGE}")
    
    # 4. 上传文章中的图片
    base_dir = os.path.dirname(html_path)
    img_tags = re.findall(r'<img[^>]+src=["\']([^"\']+)["\']', html_content)
    for src in img_tags:
        if src.startswith("http"):
            continue  # 网络图片可以被微信自动识别
        # 尝试解析相对路径
        img_full_path = src if os.path.isabs(src) else os.path.join(base_dir, src)
        if os.path.exists(img_full_path):
            try:
                img_url = upload_image(token, img_full_path)
                html_content = html_content.replace(f'src="{src}"', f'src="{img_url}"')
                log(f"  图片替换: {src} → 微信CDN")
            except Exception as e:
                log(f"  ⚠️ 图片上传失败: {src} ({e})")
    
    # 5. 转换HTML为微信格式
    title, body, digest = html_to_wechat_text(html_content)
    
    # 6. 构造文章
    article = {
        "title": title,
        "content": body,
        "digest": digest,
        "need_open_comment": 1,
        "only_fans_can_comment": 0,
    }
    if thumb_media_id:
        article["thumb_media_id"] = thumb_media_id
    
    # 7. 推送草稿
    media_id = push_draft(token, article)
    log(f"\n🎉 推送成功！草稿 media_id: {media_id}")
    log(f"👉 请登录 mp.weixin.qq.com → 草稿箱 查看并发布")
    
    # 8. 清理缓存
    if os.path.exists(TOKEN_CACHE):
        os.remove(TOKEN_CACHE)

if __name__ == "__main__":
    main()
