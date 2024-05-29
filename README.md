# gtdb

[GoogleTranslate_IPFinder](https://github.com/GoodCoder666/GoogleTranslate_IPFinder) 的默认 IP 库及更新脚本。

## 项目结构

```
│  .gitignore		Git ignore 源文件
│  LICENSE			GPL-3.0 版权许可
│  README.md		本文件
│
├─ src
|  非代码文件
│  │  ip.txt		IP 数据库
│  │  config.ini	配置文件
|  代码文件
│  │  config.py		配置文件处理模块
│  │  database.py	数据库接口
│  │  gtdb.py		主程序入口
│  │  scanner.py	扫描模块
│  │  utils.py		网络接口

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

## 版权许可

本项目使用 [GPL-3.0](./LICENSE) 版权许可。