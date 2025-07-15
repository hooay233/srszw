from webui import webui
import os
import json
import srszw

def generate(e: webui.event):
	srszw.loadConfig()
	with open(f"tmp/tmp_{port}.hooay-srszw.json", "w", encoding="utf-8") as f:
		f .write(e.get_string())
	with open(f"tmp/tmp_{port}.hooay-srszw.json", "r", encoding="utf-8") as f:
		project = json.load(f)
	try:
		vvproj = srszw.converting(project)
	except Exception as e:
		win.run(f"alert(`Error:\n{str(e)}`)")
		return
	with open(srszw.config["output"], "w", encoding="utf-8") as f:
		json.dump(vvproj, f, ensure_ascii=False)

webui.set_config(webui.Config.multi_client, True)
webui.set_config(webui.Config.use_cookies, True)
win = webui.Window()
win.bind("generate", generate)
win.set_root_folder("./ui")
win.show('./index.html')

port = win.get_port()
print(f"http://127.0.0.1:{port}")

webui.wait()

if os.path.exists(f"tmp/tmp_{port}.hooay-srszw.json"):
	os.remove(f"tmp/tmp_{port}.hooay-srszw.json")