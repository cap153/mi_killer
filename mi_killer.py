from DrissionPage import Chromium
from DrissionPage.common import Settings
import datetime

# 创建对象
cart = Chromium(9225).latest_tab

# 指定秒杀时间
kill_time = "2024-06-18 18:18:00.00000000"

# 打开小米商城购物车，需要手动点击登陆
cart.get("https://www.mi.com/shop/buy/cart")
# 等待登录完成，直到购物车全选按钮出现，超时时间我设置为1分钟
cart.wait.ele_displayed('x://*[@id="app"]/div[2]/div/div/div/div[1]/div[2]/div[1]/div[1]/i',timeout=60)

while(True):
    # 获取当前时间
    now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')
    print(now) # 打印当前时间测试
    # 判断当前时间是否到达了秒杀时间
    if(now>kill_time):
        try:
            # 开启找不到元素立即抛出异常，用于勾选全选按钮的判断
            Settings.raise_when_ele_not_found = True
            # # 通过全选按钮点击后class的变化判断商品是否全选(小米商城购物车会记住上次选择的商品)
            while not cart.ele('.iconfont icon-checkbox icon-checkbox-selected'):
                # 没有全选的情况，点击购物车全选按钮
                cart.ele('x://*[@id="app"]/div[2]/div/div/div/div[1]/div[2]/div[1]/div[1]/i').click()
            # 二次判断消抖，如果商品可以被全选并跳出循环，意味着仅存在预约的商品情况时到达了秒杀时间，预约商品可以被选中
            if not cart.ele('.iconfont icon-checkbox icon-checkbox-selected'):
                # 没有全选的情况，点击购物车全选按钮
                cart.ele('x://*[@id="app"]/div[2]/div/div/div/div[1]/div[2]/div[1]/div[1]/i').click()
            # 关闭找不到元素立即抛出异常，确保后续页面有足够时间正常加载
            Settings.raise_when_ele_not_found = False
            # 点击结算按钮
            cart.ele('去结算').click()
            # 点击默认的收获地址
            cart.wait.ele_displayed('x://*[@id="app"]/div[2]/div/div/div[2]/div/div[2]/div[2]/div[1]', timeout=60) # 等待收获地址完全加载
            cart.ele('x://*[@id="app"]/div[2]/div/div/div[2]/div/div[2]/div[2]/div[1]').click()
            # 点击立即下单
            cart.ele('立即下单').click()
            break
        except Exception as err:
            # 如果发生任何异常都进行捕捉，防止浏览器退出
            print("%s\n发生了错误，请手动完成后续步骤"%err+input())
    # 判断当前秒数是不是0，实现间隔一分钟刷新页面，防止掉登录(小米商城购物车会记住上次选择的商品)
    if(datetime.datetime.now().second == 0):
        while(True):
            cart.refresh() # DrissionPage的页面刷新方法，内置了wait.load_start()程序会自动等待加载结束
            try:
                # 等待全选按钮加载
                cart.wait.ele_displayed('x://*[@id="app"]/div[2]/div/div/div/div[1]/div[2]/div[1]/div[1]/i')
                break # 按钮加载成功说明没有问题，跳出循环
            except:
                # 没有成功加载按钮说明出现了错误，无论什么错误都再次刷新页面
                continue

# 成功的信息输出和测试时的程序暂停
input('恭喜，抢购成功')
