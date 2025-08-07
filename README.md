# VOICEVOX 中文跨语种自动生成脚本

## 介绍
可使用拼音或汉字自动生成 VOICEVOX 中文跨语种调声

## 预编译版本
> 仅有 Windows, Linux, MacOS 的 x86_64 的预编译版本
- GitHub:
- - Windows: [下载](https://github.com/hooay233/srszw/releases/download/v0.1/srszw-0.1-win-built.zip)
- - Linux: [下载](https://github.com/hooay233/srszw/releases/download/v0.1/srszw-0.1-gnu-built.zip)
- - MacOS: [下载](https://github.com/hooay233/srszw/releases/download/v0.1/srszw-0.1-mac-built.zip)
- Gitee(中国大陆用户在这下载):
- - Windows: [下载](https://gitee.com/hooay233/srszw-script/releases/download/v0.1/srszw-0.1-win-built.zip)
- - Linux: [下载](https://gitee.com/hooay233/srszw-script/releases/download/v0.1/srszw-0.1-gnu-built.zip)
- - MacOS: [下载](https://gitee.com/hooay233/srszw-script/releases/download/v0.1/srszw-0.1-mac-built.zip)

## 使用方法
### 下载项目
1. 点击 [这里](https://gitee.com/hooay233/srszw-script/repository/archive/master.zip) 下载 zip
2. 解压 zip
### 安装依赖
1. 安装 [Python3](https://python.org)
2. 安装 pypinyin
在终端输入 `pip install pypinyin` 安装
### 运行
1. 运行 `srszw.py`
2. 用 VOICEVOX 打开 `output/output.vvproj`，如果能够正常打开，则说明生成成功

## 生成自己的文本的跨语种
### 1. 复制一份空模板

复制 `./examples/empty.hooay-srszw.json` ，重命名为 `你的文件名.hooay-srszw.json`

### 2. 通过模板编辑

打开 `你的文件名.hooay-srszw.json`，然后你将看到：
```json
{
	"script_version": "0.1",
	"app_version": "0.23.0",
	"talk": [
		{
			"charactor":"shikokumetan",
			"style": null,
			"speedScale": 1,
			"pitchScale": 0,
			"intonationScale": 1,
			"volumeScale": 1,
			"prePhonemeLength": 0.1,
			"postPhonemeLength": 0.1,
			"pauseLengthScale": 1,
			"text": {
				"pinyin": null,
				"zi": "你要生成的文字"
			}
		}
	]
}
```
一下是对各个项的解释：
- `script_version`: 脚本版本，目前没有用
- `app_version`: VOICEVOX 版本，一般情况下不需要修改
- `talk`: 文本列表，存储每一个台词的信息，用 `,` 分割每个台词，用  `{` 和 `}` 包含每个台词
- - `charactor`: 角色名，通常是角色名的罗马字，详见：`./charactors/vvx.json`
- - `style`: 声线，除 `normal` 代表 `ノーマル` 外，其他都是声线的罗马字，详见：`./charactors/vvx.json`
- - `speedScale`: 语速
- - `pitchScale`: 音高
- - `intonationScale`: 抑扬
- - `volumeScale`: 音量
- - `prePhonemeLength`: 开始无音
- - `postPhonemeLength`: 终了无音
- - `pauseLengthScale`: 停顿长度
- - `text`: 台词的内容
- - - `pinyin`: 拼音，如果为`null`，则使用 `zi` 的值，否则使用 `pinyin` 的值，拼音用空格分割
- - - `zi`: 汉字，如果 `pinyin` 为`null`，则使用 `zi` 的值，否则使用 `pinyin` 的值，
同时也是在 VOICEVOX 中显示的台词文本，可以混用拼音和汉字，拼音用空格分割，一句台词的开头不能有标点符号

修改之后保存

### 3. 更改配置文件

打开 `config.json`，你将看到：
```json
{
	"file": "./examples/example1.hooay-srszw.json",
	"output": "./output/output.vvproj",
	"loaded_charactor_lists": [
		"./charactors/vvx.json"
	],
	"yunMuSpliting": "./yunMuSpliting/spliting.json",
	"zhengTiRenDu": "./zhengTiRenDu/zhenTiRenDu.json",
	"shengDiao": "./shengDiao/puTongHuaShengDiao.json",
	"shengYun": "./shengYunConvInfo/zh_in_jp1.json",
	"noYW": false,
	"pitchRange": [5.0, 6.0],
	"pitchRandom": 0.02,
	"lengthRandom": 0.001
}
```
以下是对各个项的解释：
- `file`: 修改为你保存的 `.hooay-srszw.json` 文件的路径
- `output`: 输出的 VOICEVOX 项目文件的位置
- `loaded_charactor_lists`: 角色列表，默认只有 `vvx.json`，可添加其他基于 VOICEVOX 的引擎（例如 VOICEVOX NEMO）中的角色，需要自己转写，如果不需要其他引擎的角色，则不要修改
- `yunMuSpliting`: 韵母拆分文件，一般不需要修改
- `zhengTiRenDu`: 储存整体认读的文件，一般不需要修改
- `shengDiao`: 储存声调相对音高信息的文件，一般不需要修改
- `shengYun`: 储存声韵转换信息的文件，一般不需要修改
- `noYW`: 不将 `y` 和 `w` 视为声母，为 `true` 时，不将 `y` 和 `w` 视为声母（事实上这个还有问题），为 `false` 时，将 `y` 和 `w` 视为声母
- `pitchRange`: 声调相对音高的范围
- `pitchRandom`: 音高的随机偏移
- `lengthRandom`: 音素长度的随机偏移

修改之后保存

###  4. 运行
1. 运行 `srszw.py`
2. 用 VOICEVOX 打开输出的文件，如果能够正常打开，则说明生成成功

## 图形化界面
### webui
1. 安装webui2
运行 `pip install webui2` 进行安装
2. 运行
`python web-ui.py`

### tkinter
运行 `python tk_ui.py`，有的系统可能要先安装tkinter

> 注：
> - 有些浏览器的单独窗口运行无法弹出弹窗，可以复制终端中的链接用浏览器正常模式下打开
> - 如果生成的朗读起来声音沙哑或无法发声，可尝试修改“音高”和“抑扬”
> - 图形化界面的前端是我使用 AI 生成的，并手动修改 bug
> - 本人代码水平并不好，欢迎批评，但也请保持友善
----------
> 本项目使用 WTFPL 协议，属于自由软件，可以自由使用，无需署名或专门授权。但该项目只负责生成项目文件，若使用 VOICEVOX 一类软件合成音频，仍需要遵循其协议
