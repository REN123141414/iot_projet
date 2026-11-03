# TempHumiX IHM

精简版，保留课件第 3–6 章所需代码和当前最终界面；不包含 Challenge。

## 启动最终界面（Mac）

解压后把整个 IHM 文件夹放在 ~/Desktop/iot_projet/ 中。
如果该位置已有 IHM，先将旧文件夹改名为 IHM_backup，保留旧环境与数据。

```bash
cd ~/Desktop/iot_projet/IHM
bash start_mac.command
```

脚本优先复用已有环境，没有时用 Homebrew Python 3.12 创建并安装依赖。
连接参数：192.168.1.1:1883，设备 44666，大写 Topic，前缀 /iot。
窗口打开后 Connecter 连接，Démarrer 开始采集。

## 结构

| 文件 / 目录 | 作用 |
|---|---|
| main.py | 最终界面启动入口 |
| ihm_mqtt_simple/ | 最终 UI、MQTT、线程、SQLite 和历史曲线 |
| console_mqtt_lecture/ | 第 3.3 节：控制台接收 |
| console_mqtt_ecriture/ | 第 3.4–3.5 节：控制台发送和读写并行 |
| mqtt_thread/ | 第 3.6 节：独立线程版本 |
| config_tp.py、config.json | 所有入口的公共配置 |
| commandes.py | Topic 和控制命令 |
| regenerate_ui.py | 把 Designer 的 .ui 转换成 .py |

所有控制台入口可用所选 Python 执行，例如：
`python console_mqtt_lecture/main.py`。
最终版本的 .ui 文件和生成的 .py 均在 ihm_mqtt_simple 中。

## 数据

实物归档 IOT.db；演示归档 IOT_demo.db。
需要迁移历史数据时，关闭旧程序后复制原数据库至本文件夹。
这份压缩包不包含旧数据库或 Python 虚拟环境。
