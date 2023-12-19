#!/usr/bin/python3
# -*- coding: utf-8 -*-

# 导入需要的库
import pandas as pd  # 导入 Pandas 库，用于数据处理
import numpy as np  # 导入 NumPy 库，用于科学计算

from uiautomation import WindowControl, MenuControl  # 从 uiautomation 库中导入 WindowControl 和 MenuControl 模块

# 绑定微信主窗口
wx = WindowControl(
    Name='微信',
    # searchDepth=1
)  # 创建微信主窗口对象 wx

# 切换到微信窗口
wx.SwitchToThisWindow()

# 寻找会话控件绑定
hw = wx.ListControl(Name='会话')  # 查找微信会话控件，绑定到变量 hw

# 通过 Pandas 读取名为 '回复数据.csv' 的 CSV 文件数据，使用 'utf-8' 编码
df = pd.read_csv('回复数据.csv', encoding='utf-8')

# 死循环接收消息
while True:
    # 查找未读消息控件
    we = hw.TextControl(searchDepth=4)

    # 死循环等待未读消息出现，避免超时报错
    while not we.Exists(0):
        pass

    # 存在未读消息时
    if we.Name:
        # 点击未读消息
        we.Click(simulateMove=False)

        # 读取最后一条消息
        last_msg = wx.ListControl(Name='消息').GetChildren()[-1].Name

        # 判断关键字，筛选回复内容
        msg = df.apply(lambda x: x['回复内容'] if x['关键词'] in last_msg else None, axis=1)
        
        # 移除空数据
        msg.dropna(axis=0, how='any', inplace=True)
        
        # 转换成列表
        ar = np.array(msg).tolist()

        # 当能够匹配到数据时
        if ar:
            # 发送回复内容
            wx.SendKeys(ar[0].replace('{br}', '{Shift}{Enter}'), waitTime=0)
            wx.SendKeys('{Enter}', waitTime=0)

            # 右键点击匹配的联系人
            wx.TextControl(SubName=ar[0][:5]).LeftClick()
        # 当未匹配到数据时
        else:
            # 右键点击最后一条消息对应的联系人
            wx.TextControl(SubName=last_msg[:5]).RightClick()

        # 以下部分被注释掉的代码未解除注释，功能暂时不使用
        # 匹配右键菜单控件
        # ment = MenuControl(ClassName='CMenuWnd')
        # 点击菜单中的特定选项，比如“不显示聊天”
        # ment.TextControl(Name='不显示聊天').Click()
