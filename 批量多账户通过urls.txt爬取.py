from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException, NoSuchElementException, WebDriverException
import os
import time

# 设置WebDriver路径
driver_path = 'C:\\Program Files\\Google\\Chrome\\Application\\chromedriver.exe'  # 替换为你的chromedriver路径

# 创建img文件夹（如果不存在）
download_dir = os.path.join(os.getcwd(), r'img\桌面美女图片')
if not os.path.exists(download_dir):
    os.makedirs(download_dir)

# 创建或打开url.txt文件以追加模式写入
url_file_path = os.path.join(download_dir, 'url_桌面美女图片.txt')
with open(url_file_path, 'w') as url_file:
    pass  # 清空文件内容

# 配置Chrome选项以设置下载路径
chrome_options = Options()
prefs = {
    "profile.default_content_settings.popups": 0,
    "download.default_directory": download_dir
}
chrome_options.add_experimental_option("prefs", prefs)
chrome_options.add_argument('--window-size=1000x600')  # 设置窗口大小
chrome_options.add_argument('--headless')  # 启用无头模式
chrome_options.add_argument('--disable-gpu')  # 禁用GPU加速

# 设置代理
# proxy_address = "socks5://127.0.0.1:10086"
# proxy_address = "http://127.0.0.1:30005"
# chrome_options.add_argument(f'--proxy-server={proxy_address}')
def create_driver():
    service = Service(driver_path)
    return webdriver.Chrome(service=service, options=chrome_options)

def login(driver, username, password):
    driver.get('https://www.3gbizhi.com/')  # 替换为目标网站的主页URL

    # 等待“登录/注册”按钮出现并点击
    login_register_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, '.btn_default.btn-login'))
    )
    login_register_button.click()

    # 等待登录框出现
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'account')))

    # 登录操作
    username_input = driver.find_element(By.ID, 'account')
    password_input = driver.find_element(By.ID, 'password')
    login_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, '.btn_default.gosubmit.btn-login-tc.mtv'))
    )

    username_input.send_keys(username)  # 替换为你的用户名
    password_input.send_keys(password)  # 替换为你的密码
    login_button.click()

    # 等待登录成功并跳转到主页面
    # try:
    #     WebDriverWait(driver, 10).until(EC.url_changes('https://www.com/'))
    # except TimeoutException:
    #     raise Exception("登录失败")

# 从 name.txt 文件中读取账号列表
accounts = []
with open('name.txt', 'r') as file:
    for line in file:
        account = line.strip().split(',')
        if len(account) == 1:
            accounts.append((account[0], account[0]))  # 账号和密码相同

# 循环处理每个图片页面

download_count = 0
current_account_index = 0

# 从 urls.txt 文件中读取 URL 列表
with open('urls.txt', 'r') as file:
    urls = [line.strip() for line in file]

# 设置需要爬取的次数
page_number = 0
total_pages = len(urls)-1

image_page_url = urls[page_number]
print(image_page_url)

## 记录是否需要睡眠,默认需要睡眠
flag = 1

while current_account_index < len(accounts) or page_number <= total_pages:
    username, password = accounts[current_account_index]
    print(f"使用账号: {username}, 密码: {password}")
    driver = create_driver()
    try:
        login(driver, username, password)

        while True:
            image_page_url = urls[page_number]
            try:
                print(f"正在处理页面 {page_number}: {image_page_url}")

                # 导航到包含图片的页面
                driver.get(image_page_url)

                # 检查是否是404页面或其他错误页面
                if "404" in driver.title or "Error" in driver.title:
                    print(f"页面 {page_number} 不存在或有错误")
                    break
                # 等待页面加载完成
                WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.CLASS_NAME, 'btnDwongo')))

                # 再次滚动页面以确保所有内容被加载
                last_height = driver.execute_script("return document.body.scrollHeight")
                while True:
                    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                    time.sleep(2)  # 根据实际情况调整等待时间
                    new_height = driver.execute_script("return document.body.scrollHeight")
                    if new_height == last_height:
                        break
                    last_height = new_height

                # 找到“下载高清原图”按钮并点击
                download_high_res_button = WebDriverWait(driver, 20).until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, '.btnDwongo'))
                )
                download_high_res_button.click()

                # 等待“打包下载”链接出现
                pack_download_link = WebDriverWait(driver, 20).until(
                    EC.element_to_be_clickable((By.XPATH, '//div[@class="downtip"]/a[text()="打包下载"]'))
                )

                # 获取“打包下载”链接的href属性
                href_attribute = pack_download_link.get_attribute('href')
                print(f"页面 {page_number} 的打包下载链接: {href_attribute}")

                # 将链接保存到url.txt文件
                with open(url_file_path, 'a') as url_file:
                    url_file.write(href_attribute + '\n')

                # 记录当前窗口句柄
                original_window = driver.current_window_handle

                # 点击“打包下载”链接
                pack_download_link.click()

                # 等待一段时间以确保新窗口可能已经打开
                time.sleep(5)  # 根据实际情况调整等待时间

                # 获取所有窗口句柄
                all_windows = driver.window_handles

                if len(all_windows) > 1:
                    # 新窗口已打开
                    for window_handle in all_windows:
                        if window_handle != original_window:
                            driver.switch_to.window(window_handle)
                            break

                    # 等待页面加载完成
                    time.sleep(5)  # 根据实际情况调整等待时间

                    # 检查页面是否包含“积分不足”的关键字
                    page_source = driver.page_source
                    if "无法下载" in page_source:
                        print(f"账号 {username} 积分不足，切换到下一个账号")
                        download_count = 0
                        current_account_index += 1
                        driver.quit()
                        flag = 0
                        break  # 结束当前账号的循环

                    # 关闭新窗口
                    driver.close()

                    # 切换回原始窗口
                    driver.switch_to.window(original_window)
                else:
                    # 新窗口未打开，文件正常下载
                    print(f"文件正常下载")

                # 等待下载完成
                if flag == 1 or flag == 0:
                    time.sleep(20)  # 根据实际情况调整等待时间

                download_count += 1

                page_number += 1
                if page_number > total_pages:
                    break
                image_page_url = urls[page_number]

                if download_count >= 10:
                    break

            except TimeoutException:
                print(f"页面 {page_number} 处理超时")
                break  # 结束当前账号的循环
            except NoSuchElementException as e:
                print(f"页面 {page_number} 缺少必要的元素: {e}")
                break  # 结束当前账号的循环
            except WebDriverException as e:
                print(f"发生Web驱动程序错误: {e}")
                break  # 结束当前账号的循环

    except Exception as e:
        print(f"登录失败或发生其他错误: {e}")

    finally:
        # 关闭浏览器
        driver.quit()

    # 重置下载计数器并切换到下一个账户
    download_count = 0
    current_account_index += 1

print(f"所有下载的ZIP文件和链接保存在: {download_dir}")