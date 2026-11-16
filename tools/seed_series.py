#!/usr/bin/env python3
"""Official scenario charts for the Alpha pages.

Titles follow スーパーロボット大戦Wiki 全話一覧. Each stage is placed on the
route tree exactly once. Story paragraphs are written separately.
"""

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
WORKS = ROOT / "data" / "works"


def fork(node_id, dimension, title, limbs):
    return {"kind": "fork", "id": node_id, "dimension": dimension, "title": title, "limbs": limbs}


def limb(choice, stages=None, blocks=None):
    item = {"choice": choice}
    if blocks is not None:
        item["blocks"] = blocks
    else:
        item["stages"] = stages
    return item


def spine(node_id, label, stages, tokens=None):
    node = {"kind": "spine", "id": node_id, "label": label, "stages": stages}
    if tokens:
        node["tokens"] = tokens
    return node


def subfork(dimension, limbs):
    return {"kind": "subfork", "dimension": dimension, "limbs": limbs}


def tree_order(nodes):
    found = []
    for node in nodes:
        if node["kind"] == "spine":
            found.extend(node["stages"])
            continue
        if node["kind"] != "fork":
            raise SystemExit(node["kind"])
        for item in node["limbs"]:
            found.extend(item.get("stages") or [])
            for block in item.get("blocks") or []:
                if block.get("kind") == "subfork":
                    for sub in block["limbs"]:
                        found.extend(sub.get("stages") or [])
                else:
                    found.extend(block.get("stages") or [])
    return found


TONES = ("super", "real", "earth", "space", "accent", "good", "bad")


def fill_choices(dimensions):
    for dim in dimensions:
        if "label" not in dim and "title" in dim:
            dim["label"] = dim.pop("title")
        dim.setdefault("neutral", "全部")
        for index, choice in enumerate(dim["choices"]):
            choice.setdefault("tone", TONES[index % len(TONES)])


def dump(slug, work, dimensions, tree, catalog, hide=None, extra=None):
    import importlib.util

    spec = importlib.util.spec_from_file_location("srwbuild", ROOT / "tools" / "build.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    seen = tree_order(tree)
    by_row = {row[0]: row for row in catalog}
    if len(seen) != len(set(seen)):
        dupes = sorted({stage_id for stage_id in seen if seen.count(stage_id) > 1})
        raise SystemExit(f"{slug}: placed twice: {', '.join(dupes)}")
    if set(seen) != set(by_row):
        missing = sorted(set(by_row) - set(seen))
        extra_ids = sorted(set(seen) - set(by_row))
        raise SystemExit(f"{slug}: missing={missing} extra={extra_ids}")
    catalog = [by_row[stage_id] for stage_id in seen]
    known = [row[0] for row in catalog]
    fill_choices(dimensions)
    placed = mod.place_tokens(tree)
    order = []
    for dim in dimensions:
        for choice in dim["choices"]:
            order.append(f"{dim['id']}-{choice['id']}")
    for token in extra or []:
        if token not in order:
            order.append(token)
    membership = {}
    for token in order:
        membership[token] = [stage_id for stage_id in known if token in placed[stage_id]]
    routes = {
        "page": work["page"],
        "dimensions": dimensions,
        "membership": membership,
        "hideWhen": hide or [],
        "tree": tree,
    }
    if extra:
        routes["extra"] = extra
    out = WORKS / slug
    out.mkdir(parents=True, exist_ok=True)
    (out / "routes.json").write_text(json.dumps(routes, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    (out / "catalog.json").write_text(
        json.dumps(
            [{"id": a, "titleJa": b, "titleZh": c, "route": d} for a, b, c, d in catalog],
            ensure_ascii=False,
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )
    (out / "work.json").write_text(json.dumps(work, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"{slug}: {len(catalog)} stages")


def alpha():
    S = "超級系"
    R = "即時系"
    rows = []

    def add(stage_id, ja, zh, route):
        rows.append((stage_id, ja, zh, route))

    add("a01s", "鋼鉄のコクピット", "鋼鐵的座艙", f"開幕 · {S}")
    add("a01r", "バニシング・トルーパー", "消逝的士兵", f"開幕 · {R}")
    add("a02s", "マジンガーZ絶体絶命", "魔神Z絕體絕命", f"開幕 · {S}")
    add("a02r", "黒いガンダム", "黑色高達", f"開幕 · {R}")
    add("a03s", "ゲッターチーム出撃せよ！", "蓋特小隊出擊", f"開幕 · {S}")
    add("a03r", "ホワイトベース救出", "救出白色基地", f"開幕 · {R}")
    add("a04s", "ジオン再臨", "吉翁再臨", f"開幕 · {S}")
    add("a04r", "死神と呼ばれたG", "被稱為死神的 G", f"開幕 · {R}")
    add("a05s", "シークレット・ナンバーズ", "秘密番號", f"開幕 · {S}")
    add("a05r", "ジオンの亡霊", "吉翁的亡靈", f"開幕 · {R}")
    add("a06s", "アーガマ撃墜命令", "亞加瑪擊墜命令", f"開幕 · {S}")
    add("a06r", "対決、極東基地", "對決，極東基地", f"開幕 · {R}")
    add("a07", "レッツ！コンバイン", "來吧，合體", "合流")
    add("a08", "出撃！その名はジャイアント・ロボ", "出擊，他的名字是鐵甲人", "合流")
    add("a09s", "風を呼ぶ者", "喚風的人", f"第9話 · {S}")
    add("a09r", "未知なる災い", "未知的災禍", f"第9話 · {R}")
    add("a10s", "目覚めよ、勇者", "醒來吧，勇者", "南阿塔利亞")
    add("a10r", "アムロ再び", "阿姆羅再次出擊", "賈布羅")
    add("a11s", "ガンダム強奪", "高達被搶走", "南阿塔利亞")
    add("a11r", "白いモビルスーツ", "白色機動戰士", "賈布羅")
    add("a12s", "野望の男", "野心的男人", "南阿塔利亞")
    add("a12r", "戦いは誰のために", "戰鬥是為了誰", "賈布羅")
    add("a13s", "少女が見た流星", "少女看見的流星", "南阿塔利亞")
    add("a13r", "翼を持ったガンダム", "長了翅膀的高達", "賈布羅")
    add("a14", "父との約束", "與父親的約定", "合流")
    add("a15", "使徒、襲来", "使徒來襲", "合流")
    add("a16", "咆哮、EVA初号機", "咆哮，EVA 初號機", "合流")
    add("a17", "GR対GR2", "鐵甲人對鐵甲人2", "合流")
    add("a18s", "紅い稲妻 空飛ぶマジンガー", "紅電，會飛的魔神", f"第18話 · {S}")
    add("a18r", "ゼータの鼓動", "Z 的鼓動", f"第18話 · {R}")
    add("a19s", "激突！ゲッターロボVSゲッターロボG", "蓋特對蓋特 G", f"第19話 · {S}")
    add("a19r", "第二次直上会戦", "第二次直上會戰", f"第19話 · {R}")
    add("a20", "決戦、第2新東京市", "決戰，第二新東京市", "合流")
    add("a21a", "ホンコン・シティ", "香港市", "隆德·貝爾")
    add("a21b", "獣を超え、人を超え、いでよ神の戦士", "超越獸，超越人，神之戰士出來", "極東")
    add("a21c", "聖戦士たち", "聖戰士們", "亞加瑪")
    add("a22a", "ガンダム、星の海へ", "高達，去星之海", "隆德·貝爾")
    add("a22b", "戦いの海へ", "到戰鬥的海", "極東")
    add("a22c", "エレの霊力", "艾爾的靈力", "亞加瑪")
    add("a23a", "始動ダブルゼータ", "ZZ 啟動", "隆德·貝爾")
    add("a23b", "マジンガーZ対暗黒大将軍", "魔神Z對黑暗大將軍", "極東")
    add("a23c", "ナの国の女王", "娜之國的女王", "亞加瑪")
    add("a24a", "ソロモンの悪夢", "所羅門的惡夢", "隆德·貝爾")
    add("a24b", "ボルテス起死回生", "霹靂合體起死回生", "極東")
    add("a24c", "オーラロード", "氣力之路", "亞加瑪")
    add("a25a", "クロスボーン・バンガード", "骸骨先鋒隊", "隆德·貝爾")
    add("a25b", "シャーキン悪魔の戦い", "夏金，惡魔的戰鬥", "極東")
    add("a25c", "東京上空", "東京上空", "亞加瑪")
    add("a26a", "海からのマレビト", "海上來的客人", "隆德·貝爾")
    add("a26b", "紅いエヴァンゲリオン", "紅色的福音戰士", "極東")
    add("a27", "マシン展開", "機械展開", "合流")
    add("a28", "EOTの島", "EOT 之島", "合流")
    add("a29s", "心に念じる見えない刃", "心裡念著的看不見的刃", f"第29話 · {S}")
    add("a29r", "黒い超闘士", "黑色超鬥士", f"第29話 · {R}")
    add("a30a", "瞬間、心かさねて", "瞬間，心疊在一起", "同步率")
    add("a30b", "精霊憑依", "精靈憑依", "硬上")
    add("a31a", "ブービー・トラップ", "詭雷", "擊落")
    add("a31b", "奇跡の価値は", "奇蹟的價值", "接住")
    add("a32a", "カウント・ダウン", "倒數", "擊落")
    add("a32b", "スペース・フォールド", "空間折疊", "接住")
    add("a33a", "トランス・フォーメーション", "變形", "擊落")
    add("a33b", "アームド・アタック", "武裝攻擊", "接住")
    add("a34a", "隠された殺意", "藏起來的殺意", "擊落")
    add("a34b", "天敵との遭遇", "遇上天敵", "接住")
    add("a35a", "サタン・ファイト", "撒旦之戰", "擊落")
    add("a35b", "イングラムの真意", "英格拉姆的真意", "接住")
    add("a36a", "リン・ミンメイ", "林明美", "擊落")
    add("a36b", "ミス・マクロス", "麥克羅斯小姐", "接住")
    add("a37a", "ジュピトリアン", "木星人", "擊落")
    add("a37b", "木星からの逃亡者", "來自木星的逃亡者", "接住")
    add("a38a", "帝国の女王", "帝國的女王", "擊落")
    add("a38b", "人類を導く者", "引導人類的人", "接住")
    add("a39a", "終末への前奏曲", "走向終末的前奏", "擊落")
    add("a39b", "ファースト・コンタクト", "第一次接觸", "接住")
    add("a40", "ビッグ・エスケープ", "大逃亡", "合流")
    add("a41", "バイバイ・マルス", "再見，火星", "合流")
    add("a42a", "アクシズからの使者", "來自阿克西斯的使者", "利恩·霍斯 Jr.")
    add("a42b", "ジュピター・ゴースト", "木星幽靈", "古蘭·加蘭")
    add("a42c", "父よ地球は近い", "父親啊，地球很近", "哥拉翁")
    add("a43a", "プルとアクシズと", "普露與阿克西斯", "利恩·霍斯 Jr.")
    add("a43b", "宇宙に咲く妖花", "宇宙裡開的妖花", "古蘭·加蘭")
    add("a43c", "静止した闇の中で", "在靜止的黑暗裡", "哥拉翁")
    add("a44a", "リィナの血", "莉娜的血", "利恩·霍斯 Jr.")
    add("a44b", "ゼロと呼ばれたガンダム", "被叫做零的高達", "古蘭·加蘭")
    add("a44c", "赤い髪の女", "紅頭髮的女人", "哥拉翁")
    add("a45a", "漆黒の天使来たりて", "漆黑的天使來了", "利恩·霍斯 Jr.")
    add("a45b", "強襲、阻止限界点", "強襲，阻止界限點", "古蘭·加蘭")
    add("a45c", "神か、悪魔か…", "是神，還是惡魔", "哥拉翁")
    add("a46s", "龍と虎", "龍與虎", f"第46話 · {S}")
    add("a46r", "第三の力", "第三股力量", f"第46話 · {R}")
    add("a47", "男の戰い", "男人的戰鬥", "合流")
    add("a48", "誰がために鐘は踊る", "鐘為誰而跳", "合流")
    add("a49", "進路に光明、退路に絶望", "前路有光，退路是絕望", "合流")
    add("a50", "ヴァリアブル・フォーメーション", "可變陣形", "合流")
    add("a51a", "ガラスの王国", "玻璃王國", "古蘭·加蘭")
    add("a51b", "ダカールの日", "達卡的日子", "拉·凱拉姆")
    add("a51c", "あしゅら男爵、散る", "阿修羅男爵散去", "哥拉翁")
    add("a52a", "王国崩壊", "王國崩塌", "古蘭·加蘭")
    add("a52b", "バイブレーション", "震動", "拉·凱拉姆")
    add("a52c", "魔神皇帝", "魔神皇帝", "哥拉翁")
    add("a53a", "クロス・ファイト", "交叉戰鬥", "古蘭·加蘭")
    add("a53b", "ソロモン攻略戦", "所羅門攻略戰", "拉·凱拉姆")
    add("a53c", "地球を賭けた一騎討ち", "以地球為賭注的一騎討", "哥拉翁")
    add("a54a", "異邦人たちの帰還", "異邦人回來", "古蘭·加蘭")
    add("a54b", "女たちの戦場", "女人們的戰場", "拉·凱拉姆")
    add("a54c", "思い出を未来へ", "把回憶帶去未來", "哥拉翁")
    add("a55a", "女王リリーナ", "女王莉莉娜", "古蘭·加蘭")
    add("a55b", "駆け抜ける嵐", "奔過去的嵐", "拉·凱拉姆")
    add("a55c", "父の胸の中で泣け！", "在父親懷裡哭吧", "哥拉翁")
    add("a56", "ジオンの幻像", "吉翁的幻像", "合流")
    add("a57", "天使の輪の上で", "在天使之輪上面", "合流")
    add("a58a", "神の国への誘惑", "對神之國的誘惑", "阿克西斯")
    add("a58b", "勝者と敗者に祝福を", "祝福勝者和敗者", "天使之環")
    add("a59a", "クロス・ターゲット", "交叉目標", "阿克西斯")
    add("a59b", "せめて、人間らしく", "至少，像個人", "天使之環")
    add("a60a", "戦士、再び…", "戰士，再次", "阿克西斯")
    add("a60b", "最後のシ者", "最後的使徒", "天使之環")
    add("a61", "運命の矢", "命運之箭", "合流")
    add("a62", "愛・おぼえていますか", "愛，你還記得嗎", "合流")
    add("a63", "終わりの始まり", "結束的開始", "對話")
    add("a64", "Air", "Air", "合流")
    add("a65", "ギア・オブ・デスティニー", "命運的齒輪", "合流")
    add("a66h", "絶望の宴は今から始まる", "絕望的宴席現在開始", "熟練度高")
    add("a66l", "人類に逃げ場なし", "人類沒有逃處", "熟練度低")
    add("a67h", "この星の明日のために", "為了這顆星的明天", "熟練度高")
    add("a67l", "鋼の魂", "鋼之魂", "熟練度低")
    add("a66d", "シト新生", "使徒新生", "DC 追加")
    add("a67d", "閉じ行く世界", "正在關上的世界", "DC 追加")
    add("a68", "全能なる調停者（前）", "全能的調停者（前）", "DC 追加")
    add("a69", "全能なる調停者（後）", "全能的調停者（後）", "DC 追加")
    add("a70", "神々の黄昏", "諸神的黃昏", "DC 追加")

    dims = [
        {"id": "opening", "title": "開局路線", "choices": [
            {"id": "super", "label": "超級系", "hint": "魔神、蓋特、霹靂合體"},
            {"id": "real", "label": "即時系", "hint": "高達、新世紀福音戰士"},
        ]},
        {"id": "early", "title": "第10話", "choices": [
            {"id": "atalia", "label": "南阿塔利亞", "hint": "勇者那邊"},
            {"id": "jaburo", "label": "賈布羅", "hint": "阿姆羅那邊"},
        ]},
        {"id": "fleet", "title": "第21話，三支艦隊", "choices": [
            {"id": "londo", "label": "隆德·貝爾", "hint": "利加·米利迪亞"},
            {"id": "east", "label": "極東", "hint": "龍勢、兜甲兒"},
            {"id": "argama", "label": "亞加瑪", "hint": "卡繆、聖戰士"},
        ]},
        {"id": "eva", "title": "第30話，使徒", "choices": [
            {"id": "sync", "label": "同步率", "hint": "兩台 EVA"},
            {"id": "force", "label": "硬上", "hint": "精靈憑依"},
        ]},
        {"id": "bullet", "title": "第31話，子彈", "choices": [
            {"id": "shoot", "label": "擊落", "hint": "把子彈打下來"},
            {"id": "catch", "label": "接住", "hint": "EVA 接住"},
        ]},
        {"id": "ship", "title": "第42話，乘哪艘", "choices": [
            {"id": "lean", "label": "利恩·霍斯 Jr.", "hint": "阿克西斯方向"},
            {"id": "gran", "label": "古蘭·加蘭", "hint": "木星幽靈"},
            {"id": "gora", "label": "哥拉翁", "hint": "父親的船"},
        ]},
        {"id": "endship", "title": "第51話", "choices": [
            {"id": "gran", "label": "古蘭·加蘭", "hint": "玻璃王國"},
            {"id": "ra", "label": "拉·凱拉姆", "hint": "達卡"},
            {"id": "gora", "label": "哥拉翁", "hint": "阿修羅男爵"},
        ]},
        {"id": "closing", "title": "第58話", "choices": [
            {"id": "axis", "label": "阿克西斯", "hint": "神之國"},
            {"id": "angel", "label": "天使之環", "hint": "最後的使徒"},
        ]},
        {"id": "version", "title": "平台", "choices": [
            {"id": "ps", "label": "PS", "hint": "正史，看熟練度"},
            {"id": "dc", "label": "DC 追加", "hint": "使徒新生到諸神黃昏"},
        ]},
        {"id": "skill", "title": "熟練度", "choices": [
            {"id": "high", "label": "45 以上", "hint": "為了這顆星的明天"},
            {"id": "low", "label": "44 以下", "hint": "鋼之魂"},
        ]},
    ]
    tree = [
        fork("open", "opening", "開幕", [
            limb("super", [f"a0{n}s" for n in range(1, 7)]),
            limb("real", [f"a0{n}r" for n in range(1, 7)]),
        ]),
        spine("s07", "合流", ["a07", "a08"]),
        fork("open9", "opening", "第9話", [limb("super", ["a09s"]), limb("real", ["a09r"])]),
        fork("early", "early", "第10話", [
            limb("atalia", ["a10s", "a11s", "a12s", "a13s"]),
            limb("jaburo", ["a10r", "a11r", "a12r", "a13r"]),
        ]),
        spine("s14", "合流", ["a14", "a15", "a16", "a17"]),
        fork("open18", "opening", "第18話", [
            limb("super", ["a18s", "a19s"]),
            limb("real", ["a18r", "a19r"]),
        ]),
        spine("s20", "合流", ["a20"]),
        fork("fleet", "fleet", "第21話", [
            limb("londo", ["a21a", "a22a", "a23a", "a24a", "a25a", "a26a"]),
            limb("east", ["a21b", "a22b", "a23b", "a24b", "a25b", "a26b"]),
            limb("argama", ["a21c", "a22c", "a23c", "a24c", "a25c"]),
        ]),
        spine("s27", "合流", ["a27", "a28"]),
        fork("open29", "opening", "第29話", [limb("super", ["a29s"]), limb("real", ["a29r"])]),
        fork("eva", "eva", "第30話", [limb("sync", ["a30a"]), limb("force", ["a30b"])]),
        fork("bullet", "bullet", "第31話", [
            limb("shoot", [f"a{n}a" for n in range(31, 40)]),
            limb("catch", [f"a{n}b" for n in range(31, 40)]),
        ]),
        spine("s40", "合流", ["a40", "a41"]),
        fork("ship", "ship", "第42話", [
            limb("lean", ["a42a", "a43a", "a44a", "a45a"]),
            limb("gran", ["a42b", "a43b", "a44b", "a45b"]),
            limb("gora", ["a42c", "a43c", "a44c", "a45c"]),
        ]),
        fork("open46", "opening", "第46話", [limb("super", ["a46s"]), limb("real", ["a46r"])]),
        spine("s47", "合流", ["a47", "a48", "a49", "a50"]),
        fork("endship", "endship", "第51話", [
            limb("gran", ["a51a", "a52a", "a53a", "a54a", "a55a"]),
            limb("ra", ["a51b", "a52b", "a53b", "a54b", "a55b"]),
            limb("gora", ["a51c", "a52c", "a53c", "a54c", "a55c"]),
        ]),
        spine("s56", "合流", ["a56", "a57"]),
        fork("closing", "closing", "第58話", [
            limb("axis", ["a58a", "a59a", "a60a"]),
            limb("angel", ["a58b", "a59b", "a60b"]),
        ]),
        spine("s61", "終盤", ["a61", "a62", "a63", "a64", "a65"]),
        fork("version", "version", "平台", [
            limb("ps", blocks=[
                subfork("skill", [
                    limb("high", ["a66h", "a67h"]),
                    limb("low", ["a66l", "a67l"]),
                ])
            ]),
            limb("dc", ["a66d", "a67d", "a68", "a69", "a70"]),
        ]),
    ]
    work = {
        "file": "alpha.html",
        "page": "alpha",
        "game": "α",
        "brand": ["超級機器人大戰 α", "故事"],
        "jumps": [
            {"id": "a01s", "label": "超級系開幕"},
            {"id": "a01r", "label": "即時系開幕"},
            {"id": "a07", "label": "合流"},
            {"id": "a21a", "label": "三支艦隊"},
            {"id": "a42a", "label": "三艘船"},
            {"id": "a66h", "label": "熟練度高"},
            {"id": "a66l", "label": "熟練度低"},
            {"id": "a66d", "label": "DC 追加"},
        ],
        "kicker": "PS · 1999 ／ DC · 2001",
        "title": "超級機器人大戰 α",
        "titleJa": "スーパーロボット大戦α",
        "description": "超級機器人大戰 α 的路線、各話發生的事，和結局差在哪裡。",
        "paragraphs": [
            "這是利加·米利迪亞的第一仗。巴爾馬戰爭把超級系和即時系的人拉到同一張地圖上。龍勢·達特、萊·蒂絲奈、亞伊·小林開 SRX，阿姆羅、卡繆、真嗣、兜甲兒、源堂都在這支臨時艦隊裡。",
            "開局先選超級系或即時系。第10話去南阿塔利亞或賈布羅。第21話艦隊拆成隆德·貝爾、極東、亞加瑪。第31話決定把子彈擊落，還是讓 EVA 接住。後面再選船，最後用熟練度決定結尾。",
            "正史是 PS 版。熟練度 45 以上走到「為了這顆星的明天」，44 以下走到「鋼之魂」。DC 版多五話，從「使徒新生」走到「諸神的黃昏」，人被送到 NERV。本頁以 PS 的話名為準，DC 只收這條追加路線，不把 67 話再抄一遍。",
        ],
        "endings": [
            {"h": "為了這顆星的明天", "p": ["熟練度 45 以上。第66話是「絕望的宴席現在開始」，第67話是「為了這顆星的明天」。英格拉姆的計畫被擋下，利加·米利迪亞留下。"]},
            {"h": "鋼之魂", "p": ["熟練度 44 以下。第66話改成「人類沒有逃處」，第67話是「鋼之魂」。場面更慘，結尾仍把巴爾馬的手擋在地球外面。"]},
            {"h": "諸神的黃昏", "p": ["只有 DC。第66話起換成使徒新生、正在關上的世界、全能的調停者前後篇，最後是諸神的黃昏。這條把戰場接到 NERV，不取代 PS 的兩個結尾。"]},
        ],
        "sources": [
            {"href": "https://srw.wiki.cre.jp/wiki/全話一覧/α", "text": "全話一覧／α"},
            {"href": "https://srw.wiki.cre.jp/wiki/全話一覧/α_for_DC", "text": "全話一覧／α for DC"},
            {"href": "https://srw.wiki.cre.jp/wiki/隠し要素/α", "text": "隠し要素／α"},
        ],
    }
    dump("alpha", work, dims, tree, rows)


if __name__ == "__main__":
    alpha()
