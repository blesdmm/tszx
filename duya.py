import requests
import random
import string
import json
import base64
import time

def generate_email():
    """生成随机邮箱"""
    user = ''.join(random.choices(string.ascii_lowercase + string.digits, k=8))
    domains = ['gmail.com', 'qq.com', '163.com', 'outlook.com']
    return f"{user}@{random.choice(domains)}"

def generate_password():
    """生成随机密码"""
    chars = string.ascii_letters + string.digits
    return ''.join(random.choices(chars, k=10))

def get_subscription():
    """获取订阅主函数"""
    BASE_URL = 'https://api.duya.pro'
    endpoints = {
        'register': '/v1/auth/register',
        'login': '/v1/auth/login',
        'subscribe': '/v1/public/user/subscribe'
    }
    
    user_agent = "Mozilla/5.0 (iPhone; CPU iPhone OS 15_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.0 Mobile/15E148 Safari/604.1"
    
    try:
        # 生成账号
        email = generate_email()
        password = generate_password()
        print(f"📧 邮箱: {email}")
        print(f"🔑 密码: {password}")
        
        # 1. 注册
        reg_url = BASE_URL + endpoints['register']
        reg_data = json.dumps({'email': email, 'password': password})
        reg_headers = {
            'Content-Type': 'application/json',
            'Origin': 'https://duya.pro',
            'Referer': 'https://duya.pro/register',
            'User-Agent': user_agent
        }
        
        reg_res = requests.post(reg_url, headers=reg_headers, data=reg_data, timeout=15)
        reg_json = reg_res.json()
        
        if not reg_json.get('success'):
            return f"❌ 注册失败: {reg_json.get('message', '未知错误')}"
        
        print("✅ 注册成功")
        
        # 2. 登录
        time.sleep(1)  # 防请求过快
        login_url = BASE_URL + endpoints['login']
        login_data = json.dumps({'email': email, 'password': password})
        login_headers = {
            'Content-Type': 'application/json',
            'Origin': 'https://duya.pro',
            'Referer': 'https://duya.pro/login',
            'User-Agent': user_agent
        }
        
        login_res = requests.post(login_url, headers=login_headers, data=login_data, timeout=15)
        login_json = login_res.json()
        token = login_json.get('data', {}).get('token')
        
        if not token:
            return "❌ 登录失败: 未获取到token"
        
        print("✅ 登录成功")
        
        # 3. 获取订阅token
        time.sleep(1)
        sub_url = BASE_URL + endpoints['subscribe']
        sub_headers = {
            'Authorization': token,
            'User-Agent': user_agent,
            'Origin': 'https://duya.pro',
            'Referer': 'https://duya.pro/dashboard'
        }
        
        sub_res = requests.get(sub_url, headers=sub_headers, timeout=15)
        sub_json = sub_res.json()
        
        # 检查订阅列表
        sub_list = sub_json.get('data', {}).get('list', [])
        if not sub_list:
            return "❌ 未获取到订阅列表"
        
        # 获取第一个订阅token
        sub_token = sub_list[0].get('token')
        if not sub_token:
            return "❌ 未找到订阅token"
        
        print(f"🔗 订阅Token: {sub_token}")
        
        # 4. 下载订阅内容
        final_url = f"{BASE_URL}/api/subscribe?token={sub_token}"
        content_res = requests.get(final_url, headers={'User-Agent': user_agent}, timeout=15)
        content = content_res.text
        
        # 尝试Base64解码
        try:
            decoded = base64.b64decode(content).decode('utf-8')
            return "✅ 订阅获取成功！\n\n" + decoded
        except:
            return "✅ 订阅获取成功！\n\n" + content
            
    except Exception as e:
        return f"⚠️ 发生错误: {str(e)}"

if __name__ == "__main__":
    print("="*50)
    print("🚀 开始获取订阅配置")
    print("="*50)
    
    result = get_subscription()
    
    print("\n" + "="*50)
    print("✨ 运行结果")
    print("="*50)
    print(result)
    print("="*50)
    
    # 手机端友好提示
    print("\n💡 提示：长按屏幕可复制订阅内容")