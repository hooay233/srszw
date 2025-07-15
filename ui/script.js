let jsonData = null;


function loadData() {
  try {
    const input = document.getElementById("jsonInput").value;
    jsonData = JSON.parse(input);
    renderEditor();
  } catch (e) {
    alert("JSON 格式错误，请检查");
  }
}

function renderEditor() {
    const container = document.getElementById("editor");
    container.innerHTML = "";

    jsonData.talk.forEach((item, index) => {
        const div = document.createElement("div");
        div.className = "entry";

        const manualCharactor = item.charactor === "manual" ? item.manualCharactor || '' : '';
        const displayStyle = item.charactor === "manual" ? "inline-block" : "none";
div.innerHTML = `
      <label>角色:
        <select data-index="${index}" class="charactor">
		<option value="manual" ${item.charactor === "manual" ? "selected" : ""}>[手动输入]</option>
		<option value="shikokumetan" ${item.charactor === "shikokumetan" ? "selected" : ""}>四国めたん</option>
          <option value="zundamon" ${item.charactor === "zundamon" ? "selected" : ""}>ずんだもん</option>
          <option value="kasukabetsumugi" ${item.charactor === "kasukabetsumugi" ? "selected" : ""}>春日部つむぎ</option>
		  <option value="ameharehau" ${item.charactor === "ameharehau" ? "selected" : ""}>雨晴はう</option>
		  <option value="namineritsu" ${item.charactor === "namineritsu" ? "selected" : ""}>波音リツ</option>
		  <option value="kurunotakehiro" ${item.charactor === "kurunotakehiro" ? "selected" : ""}>玄野武宏</option>
		  <option value="shirakamikotaro" ${item.charactor === "shirakamikotaro" ? "selected" : ""}>白上虎太郎</option>
		  <option value="aoyamaryusei" ${item.charactor === "aoyamaryusei" ? "selected" : ""}>青山龍星</option>
		  <option value="meimeihimari" ${item.charactor === "meimeihimari" ? "selected" : ""}>冥鳴ひまり</option>
		  <option value="kyushusora" ${item.charactor === "kyushusora" ? "selected" : ""}>九州そら</option>
		  <option value="mochikosan" ${item.charactor === "mochikosan" ? "selected" : ""}>もち子さん</option>
		  <option value="kenzakimiyu" ${item.charactor === "kenzakimiyu" ? "selected" : ""}>剣崎雌雄</option>
		  <option value="whitecul" ${item.charactor === "whitecul" ? "selected" : ""}>WhiteCUL</option>
		  <option value="goki" ${item.charactor === "goki" ? "selected" : ""}>後鬼</option>
		  <option value="no7" ${item.charactor === "no7" ? "selected" : ""}>No.7</option>
		  <option value="chibishikijii" ${item.charactor === "chibishikijii" ? "selected" : ""}>ちび式じい</option>
		  <option value="sakuramiko" ${item.charactor === "sakuramiko" ? "selected" : ""}>櫻歌ミコ</option>
		  <option value="sayosayo" ${item.charactor === "sayosayo" ? "selected" : ""}>小夜/SAYO</option>
		  <option value="nurserobottypet" ${item.charactor === "nurserobottypet" ? "selected" : ""}>ナースロボ＿タイプＴ</option>
		  <option value="seikishibenizakura" ${item.charactor === "seikishibenizakura" ? "selected" : ""}>†聖騎士 紅桜†</option>
		  <option value="suzumatsuakashi" ${item.charactor === "suzumatsuakashi" ? "selected" : ""}>雀松朱司</option>
		  <option value="kigashimasorin" ${item.charactor === "kigashimasorin" ? "selected" : ""}>麒ヶ島宗麟</option>
		  <option value="harukanana" ${item.charactor === "harukanana" ? "selected" : ""}>春歌ナナ</option>
		  <option value="nekotsukaaru" ${item.charactor === "nekotsukaaru" ? "selected" : ""}>猫使アル</option>
		  <option value="nekotsukabii" ${item.charactor === "nekotsukabii" ? "selected" : ""}>猫使ビィ</option>
		  <option value="chugokurusagi" ${item.charactor === "chugokurusagi" ? "selected" : ""}>中国うさぎ</option>
		  <option value="kuritamaron" ${item.charactor === "kuritamaron" ? "selected" : ""}>栗田まろん</option>
		  <option value="aierutan" ${item.charactor === "aierutan" ? "selected" : ""}>あいえるたん</option>
		  <option value="mitsubetsuhanamaru" ${item.charactor === "mitsubetsuhanamaru" ? "selected" : ""}>満別花丸</option>
		  <option value="kotoyominia" ${item.charactor === "kotoyominia" ? "selected" : ""}>琴詠ニア</option>
		  <option value="voidoll" ${item.charactor === "voidoll" ? "selected" : ""}>Voidoll</option>
		  <option value="zonko" ${item.charactor === "zonko" ? "selected" : ""}>ぞん子</option>
		  <option value="chubutsurugi" ${item.charactor === "chubutsurugi" ? "selected" : ""}>中部つるぎ</option>
        </select>
		</label>
		<input type="text" data-index="${index}" class="manualCharactorInput" value="${item.charactor !== "manual" ? "" : item.manualCharactor || ''}" style="display: ${item.charactor === "manual" ? "inline-block" : "none"}; width: 90%;"><br />

      <label>声线:<br>
        <input type="text" data-index="${index}" class="style" value="${item.style || ''}" style="width:90%">
      </label><br>

      <label>汉字:<br>
        <input type="text" data-index="${index}" class="zi" value="${item.text.zi}" style="width:90%">
      </label>
      <label>拼音:<br>
        <input type="text" data-index="${index}" class="pinyin" value="${item.text.pinyin || ''}" style="width:90%">
      </label><br>

      <label>话速:
        <input type="number" step="0.1" data-index="${index}" class="speedScale" value="${item.speedScale}">
      </label>
      <label>音高:
        <input type="number" step="0.1" data-index="${index}" class="pitchScale" value="${item.pitchScale}">
      </label>
      <label>抑扬:
        <input type="number" step="0.1" data-index="${index}" class="intonationScale" value="${item.intonationScale}">
      </label>
      <label>音量:
        <input type="number" step="0.1" data-index="${index}" class="volumeScale" value="${item.volumeScale}">
      </label>
      <label>开始无音:
        <input type="number" step="0.1" data-index="${index}" class="prePhonemeLength" value="${item.prePhonemeLength}">
      </label>
      <label>终了无音:
        <input type="number" step="0.1" data-index="${index}" class="postPhonemeLength" value="${item.postPhonemeLength}">
      </label>
      <label>停顿长度:
        <input type="number" step="0.1" data-index="${index}" class="pauseLengthScale" value="${item.pauseLengthScale}">
      </label><br />
	  
      <button onclick="removeEntry(${index})">删除</button>
	  <span class="id">#${index}</span>
    `;
        container.appendChild(div);
    });

    bindEvents();
}

function bindEvents() {
  document.querySelectorAll(".charactor").forEach(el => {
    el.addEventListener("change", e => {
      const idx = parseInt(e.target.dataset.index);
      jsonData.talk[idx].charactor = e.target.value;
    });
  });

document.querySelectorAll(".charactor").forEach(el => {
    el.addEventListener("change", e => {
        const idx = parseInt(e.target.dataset.index);
        const val = e.target.value;
        const inputBox = e.target.closest('.entry').querySelector('.manualCharactorInput');

        if (val === 'manual') {
            inputBox.style.display = 'inline-block';
            jsonData.talk[idx].manualCharactor = inputBox.value;
        } else {
            inputBox.style.display = 'none';
            jsonData.talk[idx].charactor = val;
            delete jsonData.talk[idx].manualCharactor;
        }
    });
});

document.querySelectorAll(".manualCharactorInput").forEach(el => {
    el.addEventListener("input", e => {
        const idx = parseInt(e.target.dataset.index);
        jsonData.talk[idx].manualCharactor = e.target.value;
    });
});

  document.querySelectorAll(".style").forEach(el => {
    el.addEventListener("input", e => {
      const idx = parseInt(e.target.dataset.index);
      const val = e.target.value || null;
      jsonData.talk[idx].style = val;
    });
  });

  document.querySelectorAll(".zi").forEach(el => {
    el.addEventListener("input", e => {
      const idx = parseInt(e.target.dataset.index);
      jsonData.talk[idx].text.zi = e.target.value;
    });
  });

  document.querySelectorAll(".pinyin").forEach(el => {
    el.addEventListener("input", e => {
      const idx = parseInt(e.target.dataset.index);
      const val = e.target.value || null;
      jsonData.talk[idx].text.pinyin = val;
    });
  });

  document.querySelectorAll(".speedScale").forEach(el => {
    el.addEventListener("input", e => {
      const idx = parseInt(e.target.dataset.index);
      jsonData.talk[idx].speedScale = parseFloat(e.target.value);
    });
  });

  document.querySelectorAll(".pitchScale").forEach(el => {
    el.addEventListener("input", e => {
      const idx = parseInt(e.target.dataset.index);
      jsonData.talk[idx].pitchScale = parseFloat(e.target.value);
    });
  });

  document.querySelectorAll(".intonationScale").forEach(el => {
    el.addEventListener("input", e => {
      const idx = parseInt(e.target.dataset.index);
      jsonData.talk[idx].intonationScale = parseFloat(e.target.value);
    });
  });

  document.querySelectorAll(".volumeScale").forEach(el => {
    el.addEventListener("input", e => {
      const idx = parseInt(e.target.dataset.index);
      jsonData.talk[idx].volumeScale = parseFloat(e.target.value);
    });
  });

  document.querySelectorAll(".prePhonemeLength").forEach(el => {
    el.addEventListener("input", e => {
      const idx = parseInt(e.target.dataset.index);
      jsonData.talk[idx].prePhonemeLength = parseFloat(e.target.value);
    });
  });

  document.querySelectorAll(".postPhonemeLength").forEach(el => {
    el.addEventListener("input", e => {
      const idx = parseInt(e.target.dataset.index);
      jsonData.talk[idx].postPhonemeLength = parseFloat(e.target.value);
    });
  });

  document.querySelectorAll(".pauseLengthScale").forEach(el => {
    el.addEventListener("input", e => {
      const idx = parseInt(e.target.dataset.index);
      jsonData.talk[idx].pauseLengthScale = parseFloat(e.target.value);
    });
  });
}

function readPatterns() {
  const patternsInput = document.getElementById("patterns");
  const lines = patternsInput.value.split('\n').map(line => line.trim()).filter(line => line !== "");

  if (!jsonData) {
    alert("请先加载 JSON 数据！");
    return;
  }

  lines.forEach(line => {
    const newEntry = {
      "charactor": "shikokumetan",
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
        "zi": line
      }
    };
    jsonData.talk.push(newEntry);
  });

  renderEditor();
}

function addEntry() {
  if (!jsonData) {
    alert("请先加载 JSON 数据！");
    return;
  }

  const newEntry = {
    "charactor": "shikokumetan",
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
      "zi": "新台词"
    }
  };

  jsonData.talk.push(newEntry);
  renderEditor();
}

function removeEntry(index) {
  if (confirm("确定删除这一条？")) {
    jsonData.talk.splice(index, 1);
    renderEditor();
  }
}

function saveData() {
  const blob = new Blob([JSON.stringify(jsonData, null, 2)], { type: "application/json" });
  const url = URL.createObjectURL(blob);

  const a = document.createElement("a");
  a.href = url;
  a.download = "edited_script.json";
  a.click();

  URL.revokeObjectURL(url);
}

function importFile(event) {
  const file = event.target.files[0];
  const reader = new FileReader();
  reader.onload = function(e) {
    try {
      jsonData = JSON.parse(e.target.result);
      document.getElementById("jsonInput").value = e.target.result;
      renderEditor();
    } catch (err) {
      alert("无法解析 JSON 文件");
    }
  };
  reader.readAsText(file);
}