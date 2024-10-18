# gtdb

[GoogleTranslate_IPFinder](https://github.com/GoodCoder666/GoogleTranslate_IPFinder) 的官方 IP 库及更新脚本。

> 2024/10/18：更新超级 IP 库，从 [GotoX IP](https://github.com/SeaHOH/GotoX/blob/master/data/ip.txt) 分离出了 IPv4 和 IPv6。当默认 IP 库全部无效时，建议尝试此 IP 库（IPv4 优先）。

## 项目结构

```
│  .gitignore       Git ignore 源文件
│  LICENSE          GPL-3.0 版权许可
│  README.md        本文件
│
├─ full             超级 IP 库
│  │  v4.txt        IPv4 库
│  │  v6.txt        IPv6 库
├─ src
|  非代码文件
│  │  ip.txt        IP 数据库
│  │  config.ini    配置文件
|  代码文件
│  │  config.py     配置文件处理模块
│  │  database.py   数据库接口
│  │  gtdb.py       主程序入口
│  │  scanner.py    扫描模块
│  │  utils.py      网络接口

** 把 ip.txt 和 config.ini 放在 src 目录下是为了方便运行。
```

## 运行脚本

在安装了 Python >= 3.6 的任意系统中执行 `gtdb.py` 即可。

若配置了 `progressBar = true`（使用进度条）则需要 `tqdm` 模块：

```
pip3 install tqdm
```

否则无第三方依赖项。

## 配置文件

运行脚本需要同一目录下存在正确的配置文件 `config.ini`。下面解释其中的一些参数：

- section `[logging]`

  - `silent`: 是否禁用控制台日志。如果你需要定时自动执行脚本，可以使用 `silent = true`。默认值：`false`
  - `updateInterval`: 更新间隔。每隔设定的时间更新一次控制台日志，单位为秒（s）。默认值：`2.0`
  - `progressBar`: 是否使用进度条代替日志输出。如果设置为 `true`，则需要安装 `tqdm` 模块。默认值：`false`

- section `[scan]`

  - `numThreads`: 扫描使用的线程数。**请根据硬件配置情况调整**，过大可能导致程序无法正常执行。默认值：`64`
  - `timeout`: 请求时间限制，单位为秒（s）。若目标 IP 超出此时间为响应，则自动判定为不可用。默认值：`1.5`
  - `randomize`: 是否随机化扫描。默认值：`true`
  - `resultLimit`: 结果数量限制。当扫出的 IP 数量达到限制时，停止扫描并保存结果。设置为 `0` 则表示无限制。默认值：`0`
  - `stabilityThreshold`: 稳定性阈值。指定单个 IP 判定为可用前的测试次数。默认值：3
  - `host`: 扫描域名，一般不需要修改。默认值：`translate.googleapis.com`
  - `format`: 请求模板，一般不需要修改。默认值：`https://{}/translate_a/single?client=gtx&sl=en&tl=fr&q=a`
  - `ipRanges`: 扫描使用的 IP 段，可以设置多个。默认值：`142.250.0.0/15`

- section `[database]`

  - `dbfile`: 数据库文件名。默认值：`ip.txt`
  - `saveMode`: 保存模式，可选 `append` / `overwrite`。分别表示在原有基础上添加数据或完全覆盖原有数据库。注意数据保存时会自动按字典序排序。

## CONTRIBUTING

我们希望能为不同网络环境的用户提供统一 IP 库。由于作者本人资源有限，无法做到在所有地区、网络、运营商分别进行 IP 扫描。

欢迎贡献可用的 IP。请先 clone 原有的 IP 库，**不要修改除 `numThreads` 和 `[logging]` 以外的其他配置项**，直接运行 `gtdb.py` 来完成 IP 库的更新。

更新之后提交 Pull Request，分支命名为 `update-yyyyMMdd`（即 `update` 加上更新的时间，如 `update-20240726`）。**您的 PR 不应包含对 `ip.txt` 以外文件的修改。**建议在评论区备注自己所在地区以及运营商方便验证。感谢您对此项目的支持！

> [!TIP]
>
> 如果你是在对代码/其他文件做改进，直接无视上面的内容。随便 PR。欢迎！