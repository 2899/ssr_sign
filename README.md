# ssr_sign
节点白嫖版，自动签到。

1：在腾讯云，找到云函数，点击新建
![image](https://github.com/ckjiexi/ssr_sign/blob/master/images/Pasted%20Graphic_%E5%89%AF%E6%9C%AC.png)

2:环境选择python 3.6，点击空白函数

![image](https://github.com/ckjiexi/ssr_sign/blob/master/images/Pasted%20Graphic%201_%E5%89%AF%E6%9C%AC.png)

3:把sign.py里的代码贴进去，修改部分信息为自己的。并点击下面的高级设置，把超时时间设置为60s，点击完成保存，然后点击下面的测试，是否成功，能收到邮件即为成功。

![image](https://github.com/ckjiexi/ssr_sign/blob/master/images/Pasted%20Graphic%202_%E5%89%AF%E6%9C%AC.png)

4:设置触发器，选择为1天1次。

![image](https://github.com/ckjiexi/ssr_sign/blob/master/images/Pasted%20Graphic%203_%E5%89%AF%E6%9C%AC.png)

以后，每天凌晨脚本就会自动运行，并且发送邮件通知今天的状态。
