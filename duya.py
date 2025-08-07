import requests
import random
import string
import json
import base64  # 用于可能的 Base64 解码


def generate_email():
    chars = string.ascii_lowercase + string.digits
    domains = ['gmail.com', '163.com', '126.com', 'qq.com', 'outlook.com', 'hotmail.com']
    name = ''.join(random.choice(chars) for _ in range(10))
    return f"{name}@{random.choice(domains)}"


def generate_password(length=10):
    chars = string.ascii_letters + string.digits
    return ''.join(random.choice(chars) for _ in range(length))


def get_subscription():
    register_url = 'https://api.duya.pro/v1/auth/register'
    login_url = 'https://api.duya.pro/v1/auth/login'
    subscription_url = 'https://api.duya.pro/v1/public/user/subscribe'
    
    email = generate_email()
    password = generate_password()
    user_agent = "Mozilla/5.0"
    headers_base = {
        'Content-Type': 'application/json',
        'Origin': 'https://duya.pro',
        'User-Agent': user_agent
    }

    try:
        print(f"[+] 生成的随机邮箱: {email}")
        print(f"[+] 生成的随机密码: {password}")

        # 1. 注册账号
        register_data = json.dumps({'email': email, 'password': password})
        register_headers = headers_base.copy()
        register_headers.update({'Referer': 'https://duya.pro/register'})
        register_response = requests.post(
            register_url, 
            headers=register_headers, 
            data=register_data
        )
        register_result = register_response.json()
        token = register_result.get('data', {}).get('token')
        if not token:
            raise Exception('注册失败或未返回 token')
        print(f"[+] 注册成功，Token: {token}")

        # 2. 登录账号（某些 API 可能不需要这步，视情况调整）
        login_data = json.dumps({'email': email, 'password': password})
        login_headers = headers_base.copy()
        login_headers.update({'Referer': 'https://duya.pro/login'})
        login_response = requests.post(
            login_url, 
            headers=login_headers, 
            data=login_data
        )
        login_result = login_response.json()
        token = login_result.get('data', {}).get('token')
        if not token:
            raise Exception('登录失败或未返回 token')
        print(f"[+] 登录成功，Token: {token}")

        # 3. 获取订阅 token
        subscribe_headers = {
            'Authorization': token,
            'User-Agent': user_agent,
            'Origin': 'https://duya.pro',
            'Referer': 'https://duya.pro/dashboard'
        }
        subscribe_response = requests.get(
            subscription_url, 
            headers=subscribe_headers
        )
        subscribe_result = subscribe_response.json()
        sub_list = subscribe_result.get('data', {}).get('list', [])
        if not sub_list:
            raise Exception('未获取到订阅列表')
        sub_token = sub_list[0].get('token')
        if not sub_token:
            raise Exception('未找到订阅 token')
        print(f"[+] 订阅 Token: {sub_token}")

        # 4. 获取订阅内容
        final_url = f"https://api.duya.pro/api/subscribe?token={sub_token}&user_agent={requests.utils.quote(user_agent)}"
        content_response = requests.get(final_url, headers={'User-Agent': user_agent})
        content = content_response.text
        
        # 尝试解码 Base64（如果是 Base64 格式）
        try:
            decoded_content = base64.b64decode(content).decode('utf-8')
            print("\n[+] 解码后的订阅内容：")
            print(decoded_content)
            return decoded_content
        except:
            print("\n[+] 原始订阅内容（非 Base64）：")
            print(content)
            return content
    except Exception as e:
        print(f"[-] 发生错误: {str(e)}")
        return None


if __name__ == "__main__":
    print("===== 开始获取订阅 =====")
    result = get_subscription()
    print("\n===== 运行结束 =====")