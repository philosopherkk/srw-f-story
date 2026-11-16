#!/usr/bin/env python3
"""Render data/stages/*.json into a single static index.html."""

import html
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "stages"
OUT = ROOT / "index.html"

REQUIRED = [
    "立ちこめる暗雲",
    "ザ・ストレンジャー",
    "シャングリラ・チルドレン",
    "非情のテロリスト",
    "ヒイロとリリーナ",
    "使徒、出現",
    "対決！？ マジンガーZvsゲッターロボG",
    "空からの衝撃",
    "特訓！大雪山おろし",
    "ポセイダルの襲撃",
    "謎の刺客！敵はガンダム！？",
    "使徒、襲来",
    "エヴァンゲリオン、始動",
    "獣戦機隊出撃",
    "熱血！！獣戦機隊合流",
    "南海の死闘",
    "裏切り",
    "使徒、再び",
    "大ピンチ！！ コン・バトラーV合体不可能！？",
    "浮上",
    "ゴラオン救出",
    "標的はロンド＝ベル",
    "驚異のデビルガンダム",
    "デビルガンダム再び",
    "デビルガンダム出現",
    "グラン・ガラン救出",
    "ロンド＝ベルへの刺客",
    "ゴラオンの危機",
    "敵包囲網を突破せよ",
    "ジェットスクランダー危機一髪！！",
    "狙われた光子力研究所",
    "ネルフ襲撃",
    "ドクーガの野望",
    "ジャブロー侵入（前）",
    "ジャブロー侵入（後）",
    "目覚めよ超獣機神",
    "合体！！超獣機神ダンクーガ",
    "ミーアの決意",
    "大将軍ガルーダの悲劇",
    "その名は東方不敗",
    "流派東方不敗！ マスターアジア登場！",
    "DCの陰謀",
    "アデレード奪回（前）",
    "アデレード奪回（後）",
    "オペレーション・レコンキスタ",
    "コロニーの反逆",
    "ロンド＝ベル、宇宙へ",
    "和平成立",
    "再会のサンクキングダム",
    "ハマーンの影",
    "うずまく悪意（前）",
    "うずまく悪意（後）",
    "フロンティア4の危機（前）",
    "フロンティア4の危機（後）",
    "ラビアンローズ",
    "アクシズの攻防",
    "ザビ家の亡霊",
    "ガラスの王国",
    "アマンダラ・カマンダラ",
    "ティターンズの悪意",
    "訣別（前）",
    "訣別（後）",
    "ティターンズの追撃",
    "絆",
    "ウワサの破嵐万丈",
    "日輪は我にあり",
    "悪意のオーラ",
    "動乱、ヨハネスバーグ",
    "ハイパージェリル",
    "トレーズの救出",
    "トレーズ、立つ",
    "ドモンの危機！！ スーパーモード発動！？",
    "ギアナ高地の修行",
    "ボストンに陽は暮れて",
    "ビヨン・ザ・トッド",
    "新しい力",
    "完成！超闘士",
    "タイムリミット（前）",
    "タイムリミット（後）",
    "野望の果てに",
    "異質なるモノへの挽歌",
    "ソラと大地のケモノ",
    "逃亡のソロシップ",
    "裏切りの月面基地",
    "無限力イデ伝説",
    "灯火は炎となりて",
    "出撃、ガンバスター",
    "解かれた封印",
    "決戦、第2新東京市",
    "運命を紡ぐ者たち",
    "悪魔と呼ばれたガンダム",
    "光瞬く宇宙へ",
    "僕がボクとして生まれた理由",
    "未完のシ者",
    "清算されし過去、そして……",
    "悲しみのカトル",
    "錯綜する想い",
    "理想と現実",
    "光、断つ剣",
    "血塗られし御手",
    "虚構の偶像",
    "復讐の刃",
    "翻る叛旗",
    "ダブル・フェイク",
    "恐怖と恐慌の狭間で",
    "激震の赤い大地",
    "ファイナル・オペレーション",
    "ファイナル・オペレーション－完結－",
    "さまよえる運命の光",
    "砂上の楼閣",
    "愛という名のエゴ",
    "崩壊の序曲",
    "塗りかえられた地図",
    "刻が動きだす時",
    "偽りの協定",
    "招かれざる訪問者",
    "運命の炎のなかで",
    "敗者への凱歌",
    "始まりと終わりが集う場所",
]


def esc(text):
    return html.escape(text, quote=True)


LEX_PATH = ROOT / "data" / "lexicon.json"


def load_lexicon():
    raw = json.loads(LEX_PATH.read_text(encoding="utf-8"))
    blocks = tuple(sorted(raw["blocks"], key=len, reverse=True))
    flat = []
    for entry in raw["entries"]:
        for form in entry["zh"]:
            flat.append((form, entry))
    flat.sort(key=lambda item: len(item[0]), reverse=True)
    return tuple(flat), raw["entries"], blocks


FORMS, ENTRIES, BLOCKS = load_lexicon()
LOOKS = json.loads((ROOT / "data" / "looks.json").read_text(encoding="utf-8"))
_LOOK_IDS = {entry["id"] for entry in ENTRIES if entry["kind"] in ("person", "unit")}
_MISSING_LOOKS = sorted(_LOOK_IDS - set(LOOKS))
_EXTRA_LOOKS = sorted(set(LOOKS) - {entry["id"] for entry in ENTRIES})
if _MISSING_LOOKS or _EXTRA_LOOKS:
    raise SystemExit(
        "looks.json mismatch\nmissing: "
        + ", ".join(_MISSING_LOOKS)
        + "\nextra: "
        + ", ".join(_EXTRA_LOOKS)
    )


def covered_by_block(text, start, length):
    end = start + length
    lo = max(0, start - 8)
    for block in BLOCKS:
        pos = text.find(block, lo, end + len(block))
        while pos != -1 and pos < end:
            if pos + len(block) > start:
                return True
            pos = text.find(block, pos + 1, end + len(block))
    return False


def _match_at(text, index):
    for form, entry in FORMS:
        if text.startswith(form, index) and not covered_by_block(text, index, len(form)):
            return form, entry
    return None


def annotate(text, seen):
    if not text:
        return ""
    out = []
    i = 0
    n = len(text)
    while i < n:
        hit = _match_at(text, i)
        if hit is None:
            out.append(esc(text[i]))
            i += 1
            continue
        form, entry = hit
        show = form != entry["ja"] and entry["id"] not in seen
        if show:
            out.append(
                f'<span class="term">{esc(form)}<i lang="ja">{esc(entry["ja"])}</i></span>'
            )
            seen.add(entry["id"])
        else:
            out.append(esc(form))
        i += len(form)
    return "".join(out)


def paras(items, seen):
    return "\n".join(f"<p>{annotate(p, seen)}</p>" for p in items)


def annotate_html(source):
    seen = set()
    out = []
    i = 0
    n = len(source)
    while i < n:
        if source[i] == "<":
            j = source.find(">", i)
            if j < 0:
                out.append(source[i:])
                break
            out.append(source[i : j + 1])
            i = j + 1
            continue
        j = source.find("<", i)
        if j < 0:
            j = n
        out.append(annotate(source[i:j], seen))
        i = j
    return "".join(out)


def matched_names(text):
    found = []
    seen = set()
    i = 0
    n = len(text)
    while i < n:
        hit = _match_at(text, i)
        if hit is None:
            i += 1
            continue
        form, entry = hit
        if entry["id"] not in seen:
            seen.add(entry["id"])
            found.append(entry["ja"])
            found.extend(entry["zh"])
        i += len(form)
    return found


KIND_LABEL = (
    ("person", "角色"),
    ("unit", "機體"),
    ("org", "勢力"),
    ("place", "地名"),
)


def render_names():
    groups = {kind: [] for kind, _label in KIND_LABEL}
    for entry in ENTRIES:
        groups[entry["kind"]].append(entry)
    chips = ['<div class="name-filters">']
    chips.append('<button type="button" class="name-chip on" data-kind="all">全部</button>')
    for kind, label in KIND_LABEL:
        chips.append(
            f'<button type="button" class="name-chip" data-kind="{kind}">{label}</button>'
        )
    chips.append("</div>")
    parts = ["".join(chips)]
    for kind, label in KIND_LABEL:
        cards = []
        for entry in sorted(groups[kind], key=lambda item: item["zh"][0]):
            alias = ""
            if len(entry["zh"]) > 1:
                rest = "、".join(esc(name) for name in entry["zh"][1:])
                alias = f'<p class="alias">亦作 {rest}</p>'
            note = entry.get("note") or ""
            if entry["ja"] == entry["zh"][0] and not note:
                note = "日文用同一組漢字。"
            note_html = f'<p class="aside">{esc(note)}</p>' if note else ""
            look = LOOKS.get(entry["id"]) or ""
            look_html = f'<p class="look">{esc(look)}</p>' if look else ""
            blob = " ".join(entry["zh"] + [entry["ja"], note, look, label])
            cards.append(
                f'''<article class="name-card" data-kind="{kind}" data-search="{esc(blob)}">
  <p class="kind">{label}</p>
  <h3>{esc(entry["zh"][0])}</h3>
  {alias}
  <p class="ja" lang="ja">{esc(entry["ja"])}</p>
  {look_html}
  {note_html}
</article>'''
            )
        parts.append(
            f'<div class="name-group" data-kind="{kind}"><h3>{label}</h3>'
            f'<div class="name-grid">{"".join(cards)}</div></div>'
        )
    return "".join(parts)


def load_stages():
    stages = []
    for path in sorted(DATA.glob("*.json")):
        stages.extend(json.loads(path.read_text(encoding="utf-8")))
    return stages


def titles_of(stage):
    names = [stage["titleJa"]]
    names.extend(stage.get("alsoJa") or [])
    return names


ROUTES_PATH = ROOT / "data" / "routes.json"

EXPECTED_ROUTES = {
    "opening-real": [
        "f-r01", "f-r02", "f-r03", "f-r04", "f-r05", "f-r06",
        "f-r08", "f-16gr", "f-14kr", "f-23r", "f-26r", "f-34r",
        "ff-r35", "ff-r36", "ff-45r", "ff-56",
    ],
    "opening-super": [
        "f-s01", "f-s02", "f-s03", "f-s04", "f-s05", "f-s06",
        "f-s08", "f-16gs", "f-14ks", "f-23s", "f-26s", "f-34s",
        "ff-s35", "ff-s36", "ff-45s", "ff-56s",
    ],
    "rescue-goraon": ["f-14g", "f-15g", "f-16gr", "f-16gs"],
    "rescue-grangalan": ["f-14kr", "f-14ks", "f-15k", "f-16k"],
    "detour-direct": ["f-17", "f-18j"],
    "detour-detour": ["f-18p"],
    "todd-success": ["ff-55a"],
    "todd-fail": ["ff-55b"],
    "split-space": ["ff-sp62", "ff-sp63", "ff-sp64", "ff-sp65", "ff-sp66"],
    "split-earth": ["ff-ea62", "ff-ea63", "ff-ea64", "ff-ea65", "ff-ea66"],
    "split-eva": ["ff-eva64", "ff-eva65"],
    "finale-dc": [
        "ff-dc69", "ff-dc70", "ff-dc71", "ff-dc72", "ff-dc73", "ff-dc74",
        "ff-dc75", "ff-dc76", "ff-dc77", "ff-dc78", "ff-dc79", "ff-dc80",
    ],
    "finale-guest": [
        "ff-g69", "ff-g70", "ff-g71", "ff-g72", "ff-g73", "ff-g74",
        "ff-g75", "ff-g76", "ff-g77", "ff-g78", "ff-g79",
    ],
    "reunion": ["ff-67", "ff-68"],
}


def load_routes():
    return json.loads(ROUTES_PATH.read_text(encoding="utf-8"))


def token_order(routes):
    order = []
    for dim in routes["dimensions"]:
        for choice in dim["choices"]:
            order.append(f"{dim['id']}-{choice['id']}")
    order.append("reunion")
    return order


def tokens_for(stage_id, routes):
    membership = routes["membership"]
    return [token for token in token_order(routes) if stage_id in membership[token]]


def choice_meta(routes, dimension_id, choice_id):
    for dim in routes["dimensions"]:
        if dim["id"] != dimension_id:
            continue
        for choice in dim["choices"]:
            if choice["id"] == choice_id:
                return dim, choice
    raise SystemExit(f"unknown choice {dimension_id}/{choice_id}")


def place_tokens(tree):
    placed = {}

    def add(stage_id, tokens):
        if stage_id in placed:
            raise SystemExit(f"stage {stage_id} appears twice in the route tree")
        placed[stage_id] = set(tokens)

    for node in tree:
        if node["kind"] == "spine":
            extra = set(node.get("tokens") or [])
            for stage_id in node["stages"]:
                add(stage_id, extra)
            continue
        if node["kind"] != "fork":
            raise SystemExit(f"unknown tree node {node.get('kind')}")
        dimension = node["dimension"]
        for limb in node["limbs"]:
            limb_tokens = {f"{dimension}-{limb['choice']}"}
            for stage_id in limb.get("stages") or []:
                add(stage_id, limb_tokens)
            for block in limb.get("blocks") or []:
                if block.get("kind") == "subfork":
                    subdimension = block["dimension"]
                    for sub in block["limbs"]:
                        sub_tokens = limb_tokens | {f"{subdimension}-{sub['choice']}"}
                        for stage_id in sub.get("stages") or []:
                            add(stage_id, sub_tokens)
                else:
                    for stage_id in block.get("stages") or []:
                        add(stage_id, limb_tokens)
    return placed


def check_routes(stages, routes):
    ids = [stage["id"] for stage in stages]
    idset = set(ids)
    if len(ids) != 119:
        raise SystemExit(f"expected 119 stages, got {len(ids)}")
    membership = routes["membership"]
    if list(membership) != list(EXPECTED_ROUTES):
        raise SystemExit("route membership key order drifted from the build check")
    if set(membership) != set(token_order(routes)):
        raise SystemExit("route membership keys do not match dimensions")
    for token, expected in EXPECTED_ROUTES.items():
        got = membership.get(token)
        if got != expected:
            raise SystemExit(f"{token} does not match the stage list in tools/build.py")
        unknown = [stage_id for stage_id in got if stage_id not in idset]
        if unknown:
            raise SystemExit(f"{token} cites unknown stages: {', '.join(unknown)}")
    for dim in routes["dimensions"]:
        seen = {}
        for choice in dim["choices"]:
            token = f"{dim['id']}-{choice['id']}"
            for stage_id in membership[token]:
                if stage_id in seen:
                    raise SystemExit(f"{stage_id} is on both {seen[stage_id]} and {token}")
                seen[stage_id] = token
    known = set(EXPECTED_ROUTES)
    for rule in routes["hideWhen"]:
        for token in rule["tokens"]:
            if token not in known:
                raise SystemExit(f"hideWhen cites unknown token {token}")
        for dim_id, choice_id in rule["when"].items():
            choice_meta(routes, dim_id, choice_id)
    fork_ids = []
    for node in routes["tree"]:
        if node["kind"] == "fork":
            fork_ids.append(node["id"])
            choice_meta(routes, node["dimension"], node["limbs"][0]["choice"])
    if len(fork_ids) != len(set(fork_ids)):
        raise SystemExit("duplicate fork ids in the route tree")
    placed = place_tokens(routes["tree"])
    if set(placed) != idset:
        missing = sorted(idset - set(placed))
        extra = sorted(set(placed) - idset)
        raise SystemExit(f"tree coverage missing={missing} extra={extra}")
    for stage in stages:
        got = set(tokens_for(stage["id"], routes))
        if placed[stage["id"]] != got:
            raise SystemExit(
                f"{stage['id']} tree tokens {sorted(placed[stage['id']])} "
                f"!= membership {sorted(got)}"
            )


def render_episodes(stage_ids, by_id):
    parts = []
    for stage_id in stage_ids:
        stage = by_id[stage_id]
        ja = "／".join(titles_of(stage))
        parts.append(
            f'<a class="ep" href="#{esc(stage_id)}">'
            f'<span class="ep-zh">{esc(stage["titleZh"])}</span>'
            f'<small class="ep-ja" lang="ja">{esc(ja)}</small>'
            f"</a>"
        )
    return "".join(parts)


def render_limb_body(limb, by_id, routes):
    chunks = []
    if limb.get("stages"):
        chunks.append(f'<div class="limb-nodes">{render_episodes(limb["stages"], by_id)}</div>')
    for block in limb.get("blocks") or []:
        if block.get("kind") == "subfork":
            chunks.append(render_subfork(block, by_id, routes))
        else:
            chunks.append(
                f'<div class="limb-nodes">{render_episodes(block["stages"], by_id)}</div>'
            )
    if limb.get("end"):
        chunks.append(f'<p class="dead-end">{esc(limb["end"])}</p>')
    return "".join(chunks)


def render_limb(limb, dimension, by_id, routes):
    _dim, choice = choice_meta(routes, dimension, limb["choice"])
    body = render_limb_body(limb, by_id, routes)
    return (
        f'<div class="limb open" data-dim="{esc(dimension)}" data-choice="{esc(choice["id"])}" '
        f'data-tone="{esc(choice["tone"])}">'
        f'<button type="button" class="limb-pick" data-dim="{esc(dimension)}" '
        f'data-choice="{esc(choice["id"])}" data-tone="{esc(choice["tone"])}" aria-pressed="false">'
        f'{esc(choice["label"])}</button>'
        f"{body}</div>"
    )


def render_subfork(block, by_id, routes):
    limbs = "".join(
        render_limb(limb, block["dimension"], by_id, routes) for limb in block["limbs"]
    )
    return f'<div class="subfork">{limbs}</div>'


def render_choices(dim):
    buttons = [
        f'<button type="button" class="choice is-on" data-dim="{esc(dim["id"])}" '
        f'data-choice="" aria-pressed="true">{esc(dim["neutral"])}</button>'
    ]
    for choice in dim["choices"]:
        buttons.append(
            f'<button type="button" class="choice" data-dim="{esc(dim["id"])}" '
            f'data-choice="{esc(choice["id"])}" data-tone="{esc(choice["tone"])}" '
            f'aria-pressed="false">{esc(choice["label"])}</button>'
        )
    return "".join(buttons)


def render_fork(node, by_id, routes):
    dim, _choice = choice_meta(routes, node["dimension"], node["limbs"][0]["choice"])
    limbs = "".join(
        render_limb(limb, node["dimension"], by_id, routes) for limb in node["limbs"]
    )
    extra = " after-split" if node.get("afterSplit") else ""
    note = (
        '<p class="cut-note">EVA 壞結局在上一叉結束，這裡不會發生。</p>'
        if node.get("afterSplit")
        else ""
    )
    panel = f'fork-panel-{node["id"]}'
    return (
        f'<li class="spine-stop tree-fork{extra}" data-fork="{esc(node["id"])}" '
        f'data-title="{esc(node["title"])}">'
        f'<div class="fork-card">{note}'
        f'<div class="fork-bar">'
        f"<h3>{esc(node['title'])}</h3>"
        f'<div class="choices" role="group" aria-label="{esc(node["title"])}">'
        f"{render_choices(dim)}</div>"
        f'<button type="button" class="fold" aria-expanded="false" aria-controls="{esc(panel)}" '
        f'aria-label="展開{esc(node["title"])}的話數">展開話數</button>'
        f"</div>"
        f'<div class="limbs" id="{esc(panel)}" hidden>{limbs}</div>'
        f"</div></li>"
    )


def render_spine(node, by_id):
    extra = " after-split" if node.get("afterSplit") else ""
    note = (
        '<p class="cut-note">EVA 壞結局在上一叉結束，這裡不會發生。</p>'
        if node.get("afterSplit")
        else ""
    )
    label = f'<p class="stop-label">{esc(node["label"])}</p>' if node.get("label") else ""
    episodes = render_episodes(node["stages"], by_id)
    return (
        f'<li class="spine-stop{extra}"><div class="stop-card">{note}{label}'
        f'<div class="limb-nodes">{episodes}</div></div></li>'
    )


def render_route_tree(routes, by_id):
    stops = []
    for node in routes["tree"]:
        if node["kind"] == "spine":
            stops.append(render_spine(node, by_id))
        else:
            stops.append(render_fork(node, by_id, routes))
    config = {
        "dimensions": [
            {
                "id": dim["id"],
                "label": dim["label"],
                "neutral": dim["neutral"],
                "choices": [{"id": choice["id"], "label": choice["label"]} for choice in dim["choices"]],
            }
            for dim in routes["dimensions"]
        ],
        "hideWhen": routes["hideWhen"],
    }
    blob = json.dumps(config, ensure_ascii=False).replace("<", "\\u003c")
    return (
        '<div class="route-tree" id="route-tree">'
        '<div class="tree-tools">'
        '<button type="button" class="tree-reset" id="route-reset">顯示全部路線</button>'
        '<p class="route-summary" id="route-summary" aria-live="polite">目前顯示全部路線。</p>'
        "</div>"
        '<ol class="spine" aria-label="路線分岐">'
        f'{"".join(stops)}'
        "</ol></div>"
        f'<script type="application/json" id="route-config">{blob}</script>'
    )


def render_stage(stage, routes):
    seen = set()
    bits = []
    for key in ("joins", "leaves", "flags"):
        for item in stage.get(key) or []:
            bits.append(f'<span class="tag">{annotate(item, seen)}</span>')
    meta = f'<div class="meta">{"".join(bits)}</div>' if bits else ""
    thin = ""
    if stage.get("thin"):
        thin = f'<p class="thin">{annotate(stage["thin"], seen)}</p>'
    note = ""
    if stage.get("note"):
        note = f'<p class="note">{annotate(stage["note"], seen)}</p>'
    ja = "／".join(titles_of(stage))
    plain = " ".join(
        [
            stage["titleZh"],
            ja,
            stage.get("route", ""),
            stage.get("game", ""),
            " ".join(stage.get("joins") or []),
            " ".join(stage.get("leaves") or []),
            " ".join(stage.get("flags") or []),
            stage.get("thin") or "",
            stage.get("note") or "",
            " ".join(stage.get("before") or []),
            " ".join(stage.get("during") or []),
            " ".join(stage.get("after") or []),
        ]
    )
    search = plain + " " + " ".join(matched_names(plain))
    route = esc(" ".join(tokens_for(stage["id"], routes)))
    return f"""
<article class="stage" id="{esc(stage["id"])}" data-group="{esc(stage["group"])}" data-route="{route}" data-search="{esc(search)}">
  <header>
    <p class="kicker">{esc(stage["game"])} · {esc(stage["route"])}</p>
    <h3>{annotate(stage["titleZh"], seen)}</h3>
    <p class="ja" lang="ja">{esc(ja)}</p>
  </header>
  {meta}
  {thin}
  <h4>戰前</h4>
  {paras(stage["before"], seen)}
  <h4>戰鬥中的轉折</h4>
  {paras(stage["during"], seen)}
  <h4>戰後</h4>
  {paras(stage["after"], seen)}
  {note}
</article>
"""


def check(stages):
    found = []
    for stage in stages:
        found.extend(titles_of(stage))
    missing = [title for title in REQUIRED if title not in found]
    if missing:
        raise SystemExit("missing titles:\n" + "\n".join(missing))
    ids = [stage["id"] for stage in stages]
    dupes = {i for i in ids if ids.count(i) > 1}
    if dupes:
        raise SystemExit("duplicate ids: " + ", ".join(sorted(dupes)))
    for stage in stages:
        for key in ("before", "during", "after"):
            if len(stage.get(key) or []) < 1:
                raise SystemExit(f"{stage['id']} missing {key}")


TEMPLATE_HEAD = r"""<!DOCTYPE html>
<html lang="zh-Hant">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>超級機器人大戰F／F完結編 故事導讀</title>
  <meta name="description" content="超級機器人大戰F與F完結編全話故事導讀。繁體中文正文，話名與角色並記日文。涵蓋即時系、超級系、全部分岐與結局。">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Noto+Sans+TC:wght@400;500;600&family=Noto+Serif+TC:wght@500;600&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="css/style.css">
</head>
<body class="hide-ruby">
<a class="skip" href="#content">跳到正文</a>
<div class="layout">
<nav class="nav" id="nav" aria-label="章節">
  <a class="brand" href="#overview"><small>スーパーロボット大戦</small><strong>超級機器人大戰 F<br>F完結編 故事</strong></a>
  <div class="nav-group">導讀</div>
  <a class="item" href="#overview">總覽</a>
  <a class="item" href="#flow">路線圖</a>
  <a class="item" href="#names">角色與機體</a>
  <a class="item" href="#endings">結局</a>
  <a class="item" href="#sources">出典</a>
  <div id="path-nav">
    <div class="nav-group">從哪一段讀</div>
    <p class="nav-hint">選好路線後，這裡改成那一條路的話，由上到下。</p>
    <a class="item" href="#f-r01">即時系開幕</a>
    <a class="item" href="#f-s01">超級系開幕</a>
    <a class="item" href="#f-07">合流之後</a>
    <a class="item" href="#f-14g">哥拉昂／古蘭加蘭</a>
    <a class="item" href="#f-17">繞路與否</a>
    <a class="item" href="#f-34r">F 的收束</a>
    <a class="item" href="#ff-r35">完結編開幕</a>
    <a class="item" href="#ff-45r">托德與超鬥士</a>
    <a class="item" href="#ff-61">天空或大地</a>
    <a class="item" href="#ff-eva64">EVA 壞結局</a>
    <a class="item" href="#ff-67">再會</a>
    <a class="item" href="#ff-dc69">DC 篇</a>
    <a class="item" href="#ff-g69">蓋斯特・波賽達爾篇</a>
  </div>
</nav>
<div class="main">
  <div class="topbar">
    <button class="menu-btn" id="menu" type="button" aria-expanded="false" aria-controls="nav">目錄</button>
    <input class="search" id="q" type="search" placeholder="搜尋話名、角色、機體或日文" aria-label="搜尋話數與名字">
    <button class="ruby-btn" id="ruby" type="button" aria-pressed="false">括號日文</button>
    <span class="count" id="count" aria-live="polite"></span>
  </div>
  <div class="reader" id="reader" hidden>
    <button type="button" id="reader-prev">上一話</button>
    <a id="reader-now" href="#stages"></a>
    <button type="button" id="reader-next">下一話</button>
  </div>
  <div class="page" id="content">
"""

TEMPLATE_INTRO = r"""
<section id="overview">
  <div class="hero">
    <p class="eyebrow">故事導讀</p>
    <h1>超級機器人大戰 F／F完結編</h1>
    <p class="ja-line">スーパーロボット大戦F／スーパーロボット大戦F完結編</p>
    <nav class="start" aria-label="從這裡開始">
      <a href="#flow">用分岐樹選話</a>
      <a href="#names">角色與機體</a>
      <a href="#f-r01">從第一話讀起</a>
    </nav>
  </div>
  <div class="prose">
  <p class="lede">這是一部給長文閱讀用的故事導讀。正文是重新寫過的繁體中文，不錄遊戲對白。每一話的標題、以及正文裡第一次需要對上原文的角色，都同時留下日文。路線以官方全話表為骨架：F 單周目 33 至 34 話，F完結編 45 至 46 話，兩作通算 78 至 80 話。多出來的那些標題不是灌水關卡，而是你沒有走上的另一邊。</p>
  <p>時間點接在 DC 戰爭和拉·吉亞斯事件之後。隆德貝爾曾經是地球的治安部隊，人卻被捲離地表；回來時聯邦已經換了做法。賈米托夫推動的泰坦斯收編 DC 殘黨，殖民衛星被重稅逼向反聯邦。彭塔戈納的波賽達爾軍、自稱蓋斯特的外星勢力、拜斯頓·威爾浮上的聖戰士、以及使徒，幾乎同時壓到地球圈。神聖十字軍（DC）沒有因為比安之死而消失，哈曼與薩比家的名字稍後會重新把它撐起來。</p>
  <p>開局先選主角的類型。即時系走宇宙與機動戰士的入口，後期機是休凱拜因；超級系走光子力研究所與超機的入口，後期機是古倫加斯特。兩條線在「福音戰士，始動」之後不斷交會，但有幾話的標題、參戰時機和隱藏條件仍然分開。中盤要先救哥拉昂還是古蘭加蘭，再決定要不要繞過拉薩。完結編則在「天空與大地的野獸」分成宇宙與地上，地上還藏著一條看到「未完的使者」就結束的 EVA 壞結局；正常打完之後，再選擇先打 DC，或先打蓋斯特與波賽達爾。</p>
  </div>
</section>

<section id="flow" class="block">
  <h2>路線圖</h2>
  <div class="prose">
    <ol class="howto">
      <li>先在每一叉選一邊。沒選的留在「兩邊」或「全部」，兩邊都走得到的話會留著。</li>
      <li>話數先收著。要看標題再按「展開話數」，免得一頁塞滿。</li>
      <li>點標題就進正文。讀的時候用下方的上一話、下一話，左邊目錄會改成這一條路。</li>
    </ol>
    <p>點到一話若正被收起，會先把路線撥過去。選擇會留在這一頁。</p>
  </div>
  <!--ROUTE_TREE-->
</section>

<section id="names" class="block">
  <h2>角色與機體</h2>
  <p class="prose">正文用香港通行的中文。每一話第一次寫到的角色、機體、勢力和地名，後面附上日文；同一話裡再出現就只留中文，避免括號把長句切斷。下面可以按類別看，頁首的搜尋框也認日文。角色和機體各有一行外形：髮色、衣服、裝甲和輪廓，按公開畫面能對上的特徵重寫，不放遊戲圖。</p>
  <!--NAME_INDEX-->
</section>
"""

TEMPLATE_END = r"""
<section id="endings" class="prose">
  <h2>結局</h2>
  <p>正常打完的結局，和三條會把故事停掉或改掉收束的路，條件不要併成一份「最可能」的清單。各來源的字面不完全一樣。超級機器人大戰維基的隱藏要素頁自己也寫過：攻略本常常漏條件，該頁亦不能保證每一條都分毫不差。下面先寫故事上發生什麼，再把條件按出處分開。</p>
  <h3>通常結局</h3>
  <p>外星人與人類談妥一條不必再靠武力往前走的路。隆德貝爾解散，地球上算得上武器的東西被封存。空間接受了，地球也正要跟上。莉莉娜走向總體和平，殖民衛星聯合在和平之下解散國界；這份和平站在死者身上，包括同伴。第三避難所把蓋斯特／波賽達爾篇寫成必然進入這個結局，不必再滿足隱藏旗標。DC 篇則要梅基博斯活著，並且一起把火星的事做完。維基的寫法更窄一點：在「恐怖與恐慌之間」第七回合出現的選擇裡，不要選「打倒梅基博斯、轉去打蓋斯特」。</p>
  <h3>全面戰爭結局</h3>
  <p>只存在於 DC 篇。特使梅基博斯死在火星之前的選擇裡。蓋斯特本國的仗暫時停了，和平卻是用力量換來的。甲兒問大家到底為了什麼而戰。隆德貝爾沒有解散，武器也沒有封存。攻略記載這條結局沒有結束 CG，音樂是「レクレイム」，不是通常結局的「結局二」。維基把觸發寫成：該話第七玩家階段的選項裡，選打倒梅基博斯。這個選項要先出現，也就是洛夫、塞蒂、澤布三人在第七回合開始時都還活著；若提前擊破其中一人，三人會先撤，梅基博斯仍會登艦，走的是通常結局那邊。第三避難所把條件簡化成「打倒格雷特金II、梅基博斯死亡」，沒有寫三人的存活與「再等一下」的選項。</p>
  <h3>EVA 壞結局</h3>
  <p>澤勒的計畫藉初號機往前走。渚薰作為第四適格者與使徒出現，真嗣親手送走他，然後關進自己的殼裡。世界在「誰都看不見我，那就全部消失」的句子裡崩掉。卡特爾因為從未成為同伴，只以一個轉為憎恨的幻影出現。遊戲在「未完的使者」結束，後面的清算、卡特爾的悲傷、DC 篇與蓋斯特篇都不會發生。第三避難所寫明這不算完整通關，畫面上有動畫再現，之後如何則沒有下文。</p>
  <p>條件各說各話，本站不把它們捏成第五份：</p>
  <ul>
    <li>維基「隱藏要素／F・F完結編」：沒有拉攏卡特爾；在「異質之物的輓歌」不要觸發真嗣擅自出擊的事件（卡特爾未加入、芙歐被帶走、而且開場沒有把真嗣編進出擊名單時，他會自己跑出來，這個成長會擋掉壞結局）；到「被解開的封印」為止，初號機從 F 累計暴走五次或以上，但「福音戰士，始動」那次強制暴走不算；在「決戰，第二新東京市」真嗣的同步率超過零。另外，在「救出托雷茲」八回合內擊破巴斯克、或在「阿克西斯攻防」拉攏卡特爾，都會使這條結局不再成立。</li>
    <li>SRWorld 與同一作者的可選情節頁：到地上篇「被解開的封印」開始之前暴走五次（不含最初事件）；「阿克西斯攻防」不說服卡特爾；「異質之物的輓歌」開場就選真嗣出擊；進入「決戰，第二新東京市」之前，真嗣同步率是三人中最高，因此由他擔任對第五使徒的炮手。達成後，該話後半改成零號機自爆。</li>
    <li>第三避難所：不拉攏卡特爾；「異質之物的輓歌」讓真嗣出擊；「天空與大地的野獸」選地上；到「決戰，第二新東京市」為止暴走五次以上，而且同步率同時高過零和明日香。作者另外寫過，芙歐死亡時多蒙會斥責真嗣，若不讓真嗣出擊他就會自己出戰並稍微成長，成長會擋住分岐；這一段作者標成自己不能完全確定。同步率必須在進入該話之前就高過另外兩人，地圖前半升級不算進後半事件。作者確認能走到的路徑是：不收卡特爾、讓芙歐死、並讓真嗣出擊。</li>
    <li>遊戲什麼都的流程圖：不在「阿克西斯攻防」說服卡特爾；「異質之物的輓歌」讓真嗣出擊；「被解開的封印」結束時已暴走五次以上，且同步率高過零（沒有寫明日香）；「決戰，第二新東京市」的八島作戰裡，陽電子炮充能結束前零號機仍然生存，以觸發零的自爆。</li>
  </ul>
  <p>幾份資料一致的部分只有這些：不收卡特爾、人在地上篇、初號機反覆暴走、真嗣的同步率壓過零、並且讓他在關鍵場面站到炮手的位置。暴走次數的結算點、要不要同時壓過明日香、芙歐死亡算不算必要、以及零號機要不要被單獨寫成一條條件，來源之間並沒有統一。直接從完結編開始時，維基注明「始動」那次暴走本來就不計入，樣本資料也不會幫你帶上 F 裡累積的次數。</p>
  <h3>伊迪結局</h3>
  <p>伊迪放棄沒有希望的人類，把所有生命吹到因果地平的另一邊。百士、哈塔利、喬利巴有配音，最後接的曲子是「與你一起在宇宙」。第三避難所與維基都把它寫成遊戲結束，而不是通關。條件是伊迪安已經加入隆德貝爾之後：伊迪槽升到伊迪自己發動，或是駕駛已經變成伊迪時把伊迪安擊墜。維基補充，槽從第六階段起有暴走的可能，第七階段起有發動的可能。這和兩條最終話裡「祈禱讓伊迪停住小行星」的離別不是同一件事。完結編中盤讓伊迪安去火星或留在地球，攻略寫成幾乎不影響劇情，不要把它當成這條結局的開關。</p>
</section>

<section id="sources" class="prose">
  <h2>出典</h2>
  <p>劇情按這些公開頁面整理，再用自己的句子重寫。沒有把攻略正文或遊戲對白整段搬過來。某一話若只有戰術表、沒有把前因寫清楚，正文會縮短並標出來。</p>
  <ul class="sources">
    <li><a href="https://srw.wiki.cre.jp/wiki/%E5%85%A8%E8%A9%B1%E4%B8%80%E8%A6%A7/F">超級機器人大戰維基：全話一覧／F</a>。話名、即時系與超級系的並排、哥拉昂與古蘭加蘭、繞路造成的 33／34 話。</li>
    <li><a href="https://srw.wiki.cre.jp/wiki/%E5%85%A8%E8%A9%B1%E4%B8%80%E8%A6%A7/F%E5%AE%8C%E7%B5%90%E7%B7%A8">全話一覧／F完結編</a>。45 至 46 話、通算 78 至 80 話，以及 PS 版把「裏切りの月面基地」改成「裏切りの月面都市」的註腳。</li>
    <li><a href="https://srw.wiki.cre.jp/wiki/%E9%9A%A0%E3%81%97%E8%A6%81%E7%B4%A0/F%E3%83%BBF%E5%AE%8C%E7%B5%90%E7%B7%A8">隱藏要素／F・F完結編</a>。托德、哈曼、卡特爾、芙歐、EVA 壞結局、全面戰爭、伊迪結局的條件。該頁聲明攻略本常有錯漏。</li>
    <li><a href="http://gamenandemo.stweb.jp/ss/srw_f/shinario1.htm">遊戲什麼都：F 流程圖</a>與 <a href="http://gamenandemo.stweb.jp/ss/srw_f/shinario2.htm">F完結編流程圖</a>。分岐形狀，以及流程圖自己列出的 EVA 條件。</li>
    <li><a href="http://www.srworld.net/gonglue/srw/srwf/srwfsddd.htm">SRWorld：F 超長攻略（SDDD）</a>，即時系與超級系分冊。各話戰前戰後的公開轉述。</li>
    <li><a href="http://www.srworld.net/gonglue/srw/srwff/walkthrough/srwff01.htm">SRWorld：F完結編分話攻略</a>，由 <a href="http://www.srworld.net/gonglue/srw/srwff/walkthrough/srwff01.htm">srwff01</a> 至 srwff65，含絆與比永·扎·托德的分頁；可選情節見 <a href="http://www.srworld.net/gonglue/srw/srwff/intro/12-OptionalEvents.htm">12 - 可選情節</a>。</li>
    <li><a href="https://daisanhinanjo.nobody.jp/%E7%AC%AC%E4%B8%89%E9%81%BF%E9%9B%A3%E6%89%80.jp/suparobo_f/srwffinal_sce005.html">第三避難所：F完結編結局</a>。通常結局、全面戰爭的壞收束、伊迪發動、EVA 結局的另一套條件與演出說明。</li>
    <li>交叉用過的單話頁包括 <a href="https://mr-blade.sakura.ne.jp/srw_F.html">mr-blade 的 F 話數索引</a>、<a href="http://srwf.tuzigiri.com/">スーパーロボット大戦F攻略データベース</a> 的參戰時機，以及 <a href="https://srw.wiki.cre.jp/wiki/%E3%82%B9%E3%83%BC%E3%83%91%E3%83%BC%E3%83%AD%E3%83%9C%E3%83%83%E3%83%88%E5%A4%A7%E6%88%A6F">作品條目</a>對前後篇氣力懲罰、即時系／超級系差異的說明。這些頁面用來核對誰在哪一話登場，不用來搬句子。</li>
  </ul>
  <p>已知比較薄、或來源互相打架的地方：基輔先行時超級系的「グラン・ガラン救出」沒有獨立的長篇轉述，攻略只說與另一條路線的古蘭加蘭戰鬥大致相同；「噴射飛行翼千鈞一髮」與「被鎖定的光子力研究所」在官方表上分屬繞路兩側，中文攻略卻把炸彈、戴安娜A與神西格瑪合流寫成同一場、並說繞路只是少打拉薩。這兩話的正文都標了這個落差。EVA 壞結局的結算回合與同步率對象，見上方結局一節，沒有取平均。</p>
</section>
<footer class="colophon">
  <p>靜態頁面。日文話名保留官方表的寫法；PS 與土星只有「背叛的月面基地／月面都市」這一題被維基注明改過名。角色和機體在每一話第一次出現時附上日文，全表見「角色與機體」。中文從香港習慣，不代表遊戲內的中文版用字——這兩作沒有官方中文。</p>
</footer>
"""

TEMPLATE_TAIL = r"""
  </div>
</div>
</div>
<a class="totop" href="#overview">回到頂部</a>
<script src="js/app.js"></script>
</body>
</html>
"""


def main():
    stages = load_stages()
    routes = load_routes()
    check(stages)
    check_routes(stages, routes)
    by_id = {stage["id"]: stage for stage in stages}
    intro = annotate_html(TEMPLATE_INTRO).replace("<!--NAME_INDEX-->", render_names())
    intro = intro.replace("<!--ROUTE_TREE-->", render_route_tree(routes, by_id))
    body = [TEMPLATE_HEAD, intro, '<section id="stages" class="block"><h2>全話</h2>']
    body.append("".join(render_stage(stage, routes) for stage in stages))
    body.append("</section>")
    body.append(annotate_html(TEMPLATE_END))
    body.append(TEMPLATE_TAIL)
    OUT.write_text("".join(body), encoding="utf-8")
    print(f"wrote {OUT} with {len(stages)} stages")


if __name__ == "__main__":
    main()
