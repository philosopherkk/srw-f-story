# 超級機器人大戰故事導讀

繁體中文的長文導讀。F／F完結編在 `index.html`。α、α外傳、第2次α、第3次α 在同目錄的 `alpha.html`、`alpha-gaiden.html`、`alpha2.html`、`alpha3.html`，頁首可以互跳。每一話的標題留下日文。角色、機體、勢力和地名在每一話第一次出現時附上日文，全表在「角色與機體」，資料在 `data/lexicon.json`，α 系列追加的名字在 `data/series-lexicon.json`。角色和機體的外形寫在 `data/looks.json` 和 `data/series-looks.json`，是按公開畫面重寫的文字，不是遊戲圖。路線圖是一棵可切換的分岐樹。

F 的正文寫在 `data/stages/*.json`，分岐寫在 `data/routes.json`。另外四部的話名和分岐在 `data/works/<作品>/`，各話正文在該目錄的 `stages/`。`tools/build.py` 把它們編成靜態 HTML，瀏覽時不再向伺服器要資料，所以可以直接放上 Vercel。話名還沒寫齊的作品會跳過，不影響 F 那一頁。

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
