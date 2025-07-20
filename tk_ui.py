import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import json
import os
import srszw  # 确保 srszw.py 存在

CHARACTORS = {
	"manual": "[手动输入]",
	"shikokumetan": "四国めたん",
	"zundamon": "ずんだもん",
	"kasukabetsumugi": "春日部つむぎ",
	"ameharehau": "雨晴はう",
	"namineritsu": "波音リツ",
	"kurunotakehiro": "玄野武宏",
	"shirakamikotaro": "白上虎太郎",
	"aoyamaryusei": "青山龍星",
	"meimeihimari": "冥鳴ひまり",
	"kyushusora": "九州そら",
	"mochikosan": "もち子さん",
	"kenzakimiyu": "剣崎雌雄",
	"whitecul": "WhiteCUL",
	"goki": "後鬼",
	"no7": "No.7",
	"chibishikijii": "ちび式じい",
	"sakuramiko": "櫻歌ミコ",
	"sayosayo": "小夜/SAYO",
	"nurserobottypet": "ナースロボ＿タイプＴ",
	"seikishibenizakura": "†聖騎士 紅桜†",
	"suzumatsuakashi": "雀松朱司",
	"kigashimasorin": "麒ヶ島宗麟",
	"harukanana": "春歌ナナ",
	"nekotsukaaru": "猫使アル",
	"nekotsukabii": "猫使ビィ",
	"chugokurusagi": "中国うさぎ",
	"kuritamaron": "栗田まろん",
	"aierutan": "あいえるたん",
	"mitsubetsuhanamaru": "満別花丸",
	"kotoyominia": "琴詠ニア",
	"voidoll": "Voidoll",
	"zonko": "ぞん子",
	"chubutsurugi": "中部つるぎ",
	"rito": "離途",
	"kurosawakohaku": "黒沢冴白",
	"yuureichan": "ユーレイちゃん",
	"touhokuzunko": "東北ずん子",
	"touhokukiritan": "東北きりたん",
	"touhokuitako": "東北イタコ"
}

def number(s: str, default:float=0.0):
	try:
		return float(s)
	except ValueError:
		return default

class TalkEntryEditor:
	def __init__(self, parent, index, data, master):
		self.parent = parent
		self.index = index
		self.data = data
		self.master = master

		self.frame = ttk.Frame(parent)
		self.frame.pack(fill="x", padx=5, pady=2)

		self.charactor_var = tk.StringVar(value=CHARACTORS.get(data.get("charactor", "shikokumetan"), "[手动输入]"))
		self.manual_charactor = tk.StringVar(value=data.get("manualCharactor", ""))
		self.style = tk.StringVar(value=str(data.get("style", "")))
		self.zi = tk.StringVar(value=data["text"].get("zi", ""))
		self.pinyin = tk.StringVar(value=data["text"].get("pinyin", ""))
		self.speedScale = tk.StringVar(value=str(data.get("speedScale", 1)))
		self.pitchScale = tk.StringVar(value=str(data.get("pitchScale", 0)))
		self.intonationScale = tk.StringVar(value=str(data.get("intonationScale", 1)))
		self.volumeScale = tk.StringVar(value=str(data.get("volumeScale", 1)))
		self.prePhonemeLength = tk.StringVar(value=str(data.get("prePhonemeLength", 0.1)))
		self.postPhonemeLength = tk.StringVar(value=str(data.get("postPhonemeLength", 0.1)))
		self.pauseLengthScale = tk.StringVar(value=str(data.get("pauseLengthScale", 1)))

		self.create_widgets()

	def create_widgets(self):
		# 角色下拉框
		ttk.Label(self.frame, text="角色:").grid(row=0, column=0, sticky="w")
		self.charactor_combo = ttk.Combobox(self.frame, textvariable=self.charactor_var)
		self.charactor_combo['values'] = list(CHARACTORS.values())
		self.charactor_combo.grid(row=0, column=1, sticky="ew")
		self.charactor_combo.bind("<<ComboboxSelected>>", self.on_charactor_change)

		# 手动输入框
		self.manual_entry = ttk.Entry(self.frame, textvariable=self.manual_charactor)
		self.manual_entry.grid(row=0, column=2, sticky="ew")
		self.manual_charactor.trace("w", lambda *args: self.update_data())  # ✅ 添加 trace
		if self.data.get("charactor") != "manual":
			self.manual_entry.grid_remove()

		# 声线
		ttk.Label(self.frame, text="声线:").grid(row=1, column=0, sticky="w")
		ttk.Entry(self.frame, textvariable=self.style).grid(row=1, column=1, sticky="ew")
		self.style.trace("w", lambda *args: self.update_data())

		# 汉字
		ttk.Label(self.frame, text="汉字:").grid(row=2, column=0, sticky="w")
		ttk.Entry(self.frame, textvariable=self.zi).grid(row=2, column=1, sticky="ew")
		self.zi.trace("w", lambda *args: self.update_data())

		# 拼音
		ttk.Label(self.frame, text="拼音:").grid(row=3, column=0, sticky="w")
		ttk.Entry(self.frame, textvariable=self.pinyin).grid(row=3, column=1, sticky="ew")
		self.pinyin.trace("w", lambda *args: self.update_data())

		# 话速
		ttk.Label(self.frame, text="话速:").grid(row=4, column=0, sticky="w")
		ttk.Entry(self.frame, textvariable=self.speedScale).grid(row=4, column=1, sticky="ew")
		self.speedScale.trace("w", lambda *args: self.update_data())

		# 音高
		ttk.Label(self.frame, text="音高:").grid(row=5, column=0, sticky="w")
		ttk.Entry(self.frame, textvariable=self.pitchScale).grid(row=5, column=1, sticky="ew")
		self.pitchScale.trace("w", lambda *args: self.update_data())

		# 抑扬
		ttk.Label(self.frame, text="抑扬:").grid(row=6, column=0, sticky="w")
		ttk.Entry(self.frame, textvariable=self.intonationScale).grid(row=6, column=1, sticky="ew")
		self.intonationScale.trace("w", lambda *args: self.update_data())

		# 音量
		ttk.Label(self.frame, text="音量:").grid(row=7, column=0, sticky="w")
		ttk.Entry(self.frame, textvariable=self.volumeScale).grid(row=7, column=1, sticky="ew")
		self.volumeScale.trace("w", lambda *args: self.update_data())

		# 开始无音
		ttk.Label(self.frame, text="开始无音:").grid(row=8, column=0, sticky="w")
		ttk.Entry(self.frame, textvariable=self.prePhonemeLength).grid(row=8, column=1, sticky="ew")
		self.prePhonemeLength.trace("w", lambda *args: self.update_data())

		# 终了无音
		ttk.Label(self.frame, text="终了无音:").grid(row=9, column=0, sticky="w")
		ttk.Entry(self.frame, textvariable=self.postPhonemeLength).grid(row=9, column=1, sticky="ew")
		self.postPhonemeLength.trace("w", lambda *args: self.update_data())

		# 停顿长度
		ttk.Label(self.frame, text="停顿长度:").grid(row=10, column=0, sticky="w")
		ttk.Entry(self.frame, textvariable=self.pauseLengthScale).grid(row=10, column=1, sticky="ew")
		self.pauseLengthScale.trace("w", lambda *args: self.update_data())

		# 删除按钮
		ttk.Button(self.frame, text="删除", command=self.remove).grid(row=11, column=0, sticky="ew")

		# ID 显示
		ttk.Label(self.frame, text=f"#{self.index}", foreground="gray").grid(row=11, column=1, sticky="e")

	def on_charactor_change(self, event=None):
		selected_jp = self.charactor_var.get()
		selected_en = next(k for k, v in CHARACTORS.items() if v == selected_jp)
		if selected_en == "manual":
			self.manual_entry.grid()
		else:
			self.manual_entry.grid_remove()
		self.data["charactor"] = selected_en

	def remove(self):
		if messagebox.askokcancel("删除", f"确定删除条目 #{self.index}？"):
			self.master.remove_entry(self.index)

	def update_data(self):
		selected_jp = self.charactor_var.get()
		selected_en = next(k for k, v in CHARACTORS.items() if v == selected_jp)
		self.data["charactor"] = selected_en
		if selected_en == "manual":
			self.data["charactor"] = self.manual_charactor.get()
		else:
			self.data.pop("manualCharactor", None)
		self.data["style"] = self.style.get() if self.style.get() != "" and self.style.get() != "None" else None
		self.data["text"]["zi"] = self.zi.get()
		self.data["text"]["pinyin"] = self.pinyin.get() or None
		self.data["speedScale"] = number(self.speedScale.get(), 1.0)
		self.data["pitchScale"] = number(self.pitchScale.get(), 0.0)
		self.data["intonationScale"] = number(self.intonationScale.get(), 1.0)
		self.data["volumeScale"] = number(self.volumeScale.get(), 1.0)
		self.data["prePhonemeLength"] = number(self.prePhonemeLength.get(), 0.1)
		self.data["postPhonemeLength"] = number(self.postPhonemeLength.get(), 0.1)
		self.data["pauseLengthScale"] = number(self.pauseLengthScale.get(), 1.0)

class App:
	def __init__(self, root):
		self.root = root
		self.root.title("术人术中文跨语种自动生成脚本 UI")
		self.json_data = None
		self.entries = []

		# JSON 输入框
		self.json_input = tk.Text(root, height=10)
		self.json_input.pack(padx=10, pady=5)
		self.json_input.insert("1.0", """{
	"script_version": "0.1",
	"app_version": "0.23.0",
	"talk": []
}""")

		# 加载按钮
		ttk.Button(root, text="加载数据", command=self.load_data).pack(pady=5)

		# 台词输入框
		self.patterns = tk.Text(root, height=5)
		self.patterns.pack(padx=10, pady=5)

		# 读取台词按钮
		ttk.Button(root, text="读取台词", command=self.read_patterns).pack(pady=5)

		# 条目容器
		self.editor_frame = ttk.Frame(root)
		self.editor_frame.pack(fill="both", expand=True, padx=10, pady=5)

		self.canvas = tk.Canvas(self.editor_frame)
		self.scrollbar = ttk.Scrollbar(self.editor_frame, orient="vertical", command=self.canvas.yview)
		self.scrollable_frame = ttk.Frame(self.canvas)

		self.scrollable_frame.bind(
			"<Configure>",
			lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
		)

		self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
		self.canvas.configure(yscrollcommand=self.scrollbar.set)

		self.canvas.pack(side="left", fill="both", expand=True)
		self.scrollbar.pack(side="right", fill="y")

		# 控制按钮
		ttk.Button(root, text="添加新句子", command=self.add_entry).pack(pady=5)
		ttk.Button(root, text="导出 JSON", command=self.save_data).pack(pady=5)
		ttk.Button(root, text="导入 JSON", command=self.import_file).pack(pady=5)
		ttk.Button(root, text="生成", command=self.generate).pack(pady=5)

	def load_data(self):
		try:
			content = self.json_input.get("1.0", "end-1c")
			self.json_data = json.loads(content)
			self.render_editor()
		except json.JSONDecodeError as e:
			messagebox.showerror("错误", f"JSON 格式错误：{e}")

	def render_editor(self):
		for widget in self.scrollable_frame.winfo_children():
			widget.destroy()
		self.entries.clear()
		for idx, item in enumerate(self.json_data["talk"]):
			self.entries.append(TalkEntryEditor(self.scrollable_frame, idx, item, self))

	def add_entry(self):
		if self.json_data is None:
			messagebox.showwarning("警告", "请先加载 JSON 数据！")
			return
		new_entry = {
			"charactor": "shikokumetan",
			"style": None,
			"speedScale": 1,
			"pitchScale": 0,
			"intonationScale": 1,
			"volumeScale": 1,
			"prePhonemeLength": 0.1,
			"postPhonemeLength": 0.1,
			"pauseLengthScale": 1,
			"text": {
				"pinyin": None,
				"zi": "新台词"
			}
		}
		self.json_data["talk"].append(new_entry)
		self.render_editor()

	def remove_entry(self, index):
		del self.json_data["talk"][index]
		self.render_editor()

	def read_patterns(self):
		if self.json_data is None:
			messagebox.showwarning("警告", "请先加载 JSON 数据！")
			return
		lines = self.patterns.get("1.0", "end-1c").splitlines()
		for line in lines:
			if not line.strip():
				continue
			self.json_data["talk"].append({
				"charactor": "shikokumetan",
				"style": None,
				"speedScale": 1,
				"pitchScale": 0,
				"intonationScale": 1,
				"volumeScale": 1,
				"prePhonemeLength": 0.1,
				"postPhonemeLength": 0.1,
				"pauseLengthScale": 1,
				"text": {
					"pinyin": None,
					"zi": line.strip()
				}
			})
		self.render_editor()

	def save_data(self):
		if self.json_data is None:
			messagebox.showwarning("警告", "请先加载 JSON 数据！")
			return
		filename = filedialog.asksaveasfilename(defaultextension=".json", filetypes=[("JSON 文件", "*.json")])
		if filename:
			with open(filename, "w", encoding="utf-8") as f:
				json.dump(self.json_data, f, indent=2, ensure_ascii=False)
			messagebox.showinfo("导出", "JSON 已导出！")

	def import_file(self):
		filename = filedialog.askopenfilename(filetypes=[("JSON 文件", "*.json")])
		if filename:
			with open(filename, "r", encoding="utf-8") as f:
				try:
					self.json_data = json.load(f)
					self.json_input.delete("1.0", tk.END)
					self.json_input.insert("1.0", json.dumps(self.json_data, indent=2, ensure_ascii=False))
					self.render_editor()
				except json.JSONDecodeError:
					messagebox.showerror("错误", "无法解析 JSON 文件")

	def generate(self):
		if self.json_data is None:
			messagebox.showwarning("警告", "请先加载 JSON 数据！")
			return
		srszw.loadConfig()
		try:
			project = srszw.converting(self.json_data)
			output_path = srszw.config["output"]
		except Exception as e:
			messagebox.showerror("错误", f"生成出错：{e}")
			return
		with open(output_path, "w", encoding="utf-8") as f:
			json.dump(project, f, ensure_ascii=False)
		messagebox.showinfo("成功", f"生成完成，已输出至 {output_path}")


if __name__ == "__main__":
	root = tk.Tk()
	app = App(root)
	root.mainloop()