# Luogu Clockin

一个使用 Python 爬虫实现的洛谷自动打卡脚本。脚本会使用 `.env` 中配置的洛谷 Cookie 信息访问洛谷首页，判断当日是否已经打卡；如果尚未打卡，则请求洛谷打卡接口，并将结果记录到日志/CSV 中。可选地支持钉钉机器人通知。

> 说明：本项目仅供学习 Python 爬虫、定时任务和个人自动化使用。请遵守洛谷网站规则，不要高频请求或滥用接口。

## 背景

2023 年底 AFO 后，我的洛谷打卡天数已经到了四位数。我不想让这个数字归零，因为洛谷见证了我很重要的一段经历。那时候 AI 能力不强，我手搓了多个不同方案实现退役后的自动打卡，也踩过很多坑。这个版本的代码是我进入 ZJU 后结合阿里云服务器重构的。在这里开源给和我一样热爱 OI，缅怀那段难忘的岁月，在新的人生轨迹上不断求索的你。

## 功能

- 自动检测洛谷是否已经打卡
- 未打卡时自动发送打卡请求
- 输出当前运势与连续打卡天数
- 可选：发送钉钉机器人通知
- 可配合 Windows 定时任务或 Ubuntu `cron` 实现每日自动运行

## 项目结构

```text
luogu-clockin/
├── clockin2026.py
├── requirements.txt
├── .env.example
├── .env              # 本地私密配置，不要上传到网上
├── .gitignore
├── README.md
└── LICENSE
```

## 环境要求

- Python 3.9+

## 安装与配置

### 1. 克隆项目

```bash
git clone https://github.com/conscient2025/luogu-clockin.git
cd luogu-clockin
```

### 2. 创建并启用虚拟环境

#### Windows PowerShell

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

#### Windows CMD

```bat
python -m venv .venv
.venv\Scripts\activate.bat
```

#### macOS / Linux

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. 安装依赖

```bash
pip install -r requirements.txt
```

### 4. 配置 `.env`

示例配置：

```env
# For Luogu cookie
UID=your_uid
CLIENT=your_client_id

# For DingTalk notification(Optional)
ENABLE_DINGTALK=true # set to anything except "true" to disable
DINGTALK_WEBHOOK="https://oapi.dingtalk.com/robot/send?access_token=your_access_token"
```

字段说明：

| 字段 | 说明 |
|---|---|
| `UID` | 洛谷用户 UID |
| `CLIENT` | 洛谷 Cookie 中的 `__client_id` 值 |
| `ENABLE_DINGTALK` | 是否启用钉钉通知，只有值为 `true` 时启用 |
| `DINGTALK_WEBHOOK` | 钉钉自定义机器人 Webhook 地址 |


## 手动运行

激活虚拟环境后运行：

```bash
python clockin2026.py
```

## Windows 定时任务

可以使用 Windows 任务计划程序，配合每天自动开机/唤醒，实现每日自动打卡。

### 核心命令

假设项目路径为：

```text
D:\Projects\luogu-clockin
```

则定时任务中建议使用 venv 里的 Python，而不是系统 Python：

```bat
D:\Projects\luogu-clockin\.venv\Scripts\python.exe D:\Projects\luogu-clockin\clockin2026.py >> D:\Projects\luogu-clockin\clockin2026.log 2>&1
```

如果在“任务计划程序”图形界面中配置，推荐这样填：

- 程序或脚本：

```text
cmd.exe
```

- 添加参数：

```text
/c "D:\Projects\luogu-clockin\.venv\Scripts\python.exe D:\Projects\luogu-clockin\clockin2026.py >> D:\Projects\luogu-clockin\clockin2026.log 2>&1"
```

- 起始于：

```text
D:\Projects\luogu-clockin
```

其中：

- `>> clockin2026.log` 表示把输出追加到日志文件
- `2>&1` 表示把错误信息也写入同一个日志文件
- 使用 `.venv\Scripts\python.exe` 可以保证运行时使用项目自己的依赖环境

### 定时开关机提示

Windows 可以在 BIOS/UEFI 中设置定时开机，或使用任务计划程序设置“唤醒计算机运行此任务”。

## Ubuntu 服务器定时运行

Ubuntu 服务器上推荐使用 `cron`。

### 1. 进入项目并安装依赖

```bash
cd /home/your_user/luogu-clockin
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### 2. 测试手动运行

```bash
/home/your_user/luogu-clockin/.venv/bin/python3 /home/your_user/luogu-clockin/clockin2026.py
```

确认能正常运行后，再设置定时任务。

### 3. 编辑 crontab

```bash
crontab -e
```

添加一行，例如每天 05:20 运行：

```cron
20 5 * * * /home/your_user/luogu-clockin/.venv/bin/python3 /home/your_user/luogu-clockin/clockin2026.py >> /home/your_user/luogu-clockin/clockin2026.log 2>&1
```

查看当前用户的定时任务：

```bash
crontab -l
```

## 常见问题

### 1. `.env` 已经写了，但脚本读取不到

请确认：

- 已安装 `python-dotenv`
- 当前运行目录是项目根目录
- `.env` 文件名正确，不是 `.env.txt`

### 2. 定时任务没有运行

优先检查：

- Python 路径是否写成了 venv 中的 Python
- Ubuntu 日志路径是否有写入权限
- Windows 是否真的唤醒/开机
