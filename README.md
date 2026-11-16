# 超級機器人大戰 F／F完結編 故事導讀

繁體中文的長文導讀。每一話的標題留下日文。角色、機體、勢力和地名在每一話第一次出現時附上日文，全表在「角色與機體」，資料在 `data/lexicon.json`。路線圖是一棵可切換的分岐樹，用來打開或收起話數：即時系與超級系、哥拉昂與古蘭加蘭、拉薩繞路、托德、宇宙與地上、EVA 壞結局，以及 DC 與蓋斯特／波賽達爾兩條最終篇。

正文寫在 `data/stages/*.json`，分岐寫在 `data/routes.json`。`tools/build.py` 把它編成單一的 `index.html`，瀏覽時不再向伺服器要資料，所以可以直接放上 Vercel。

## 本地預覽

用瀏覽器打開倉庫根目錄的 `index.html` 即可。若要走本機伺服器：

```bash
python3 -m http.server 8000
```

改完話數資料之後，重新產生頁面：

```bash
python3 tools/gen_f_open.py
python3 tools/gen_f_rest.py
python3 tools/gen_ff_early.py
python3 tools/gen_ff_late.py
python3 tools/build.py
```

## Vercel

`vercel.json` 把 framework 留空，不設定建置指令。Vercel 直接用倉庫根目錄的 `index.html`、`css/` 和 `js/`。不需要安裝套件，也不需要伺服端程式。
