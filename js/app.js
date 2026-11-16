(function () {
  var nav = document.getElementById("nav");
  var btn = document.getElementById("menu");
  var input = document.getElementById("q");
  var count = document.getElementById("count");
  var tree = document.getElementById("route-tree");
  var summary = document.getElementById("route-summary");
  var configNode = document.getElementById("route-config");
  var stages = Array.prototype.slice.call(document.querySelectorAll(".stage"));
  var groups = Array.prototype.slice.call(document.querySelectorAll(".name-group"));
  var nameChips = Array.prototype.slice.call(document.querySelectorAll(".name-chip"));
  var ROUTE = JSON.parse(configNode.textContent);
  var CHOICE_KEY = "srw-f-route-choices";
  var FOLD_KEY = "srw-f-route-folds";
  var activeKind = "all";
  var choices = {};
  var folds = {};

  function setOpen(open) {
    nav.classList.toggle("open", open);
    btn.setAttribute("aria-expanded", open ? "true" : "false");
  }

  btn.addEventListener("click", function () {
    setOpen(!nav.classList.contains("open"));
  });

  nav.addEventListener("click", function (event) {
    if (event.target.closest("a")) setOpen(false);
  });

  function tokensOf(stage) {
    return (stage.getAttribute("data-route") || "").split(/\s+/).filter(Boolean);
  }

  function hiddenByRule(tokens) {
    return ROUTE.hideWhen.some(function (rule) {
      var keys = Object.keys(rule.when);
      for (var i = 0; i < keys.length; i += 1) {
        if ((choices[keys[i]] || "") !== rule.when[keys[i]]) return false;
      }
      return tokens.some(function (token) {
        return rule.tokens.indexOf(token) !== -1;
      });
    });
  }

  function stageMatches(stage) {
    var tokens = tokensOf(stage);
    for (var i = 0; i < ROUTE.dimensions.length; i += 1) {
      var dim = ROUTE.dimensions[i];
      var selected = choices[dim.id] || "";
      if (!selected) continue;
      var prefix = dim.id + "-";
      var mine = tokens.filter(function (token) {
        return token.indexOf(prefix) === 0;
      });
      if (mine.length && mine.indexOf(prefix + selected) === -1) return false;
    }
    return !hiddenByRule(tokens);
  }

  function alignChoicesTo(stage) {
    var tokens = tokensOf(stage);
    ROUTE.dimensions.forEach(function (dim) {
      var prefix = dim.id + "-";
      var mine = tokens.filter(function (token) {
        return token.indexOf(prefix) === 0;
      }).map(function (token) {
        return token.slice(prefix.length);
      });
      if (!mine.length) return;
      var selected = choices[dim.id] || "";
      if (selected && mine.indexOf(selected) === -1) choices[dim.id] = mine[0];
    });
    if (stageMatches(stage)) return;
    ROUTE.hideWhen.forEach(function (rule) {
      var blocked = tokens.some(function (token) {
        return rule.tokens.indexOf(token) !== -1;
      });
      if (!blocked) return;
      var keys = Object.keys(rule.when);
      var active = keys.every(function (key) {
        return (choices[key] || "") === rule.when[key];
      });
      if (!active) return;
      keys.forEach(function (key) {
        choices[key] = "";
      });
    });
  }

  function apply() {
    var q = (input.value || "").trim().toLowerCase();
    var shown = 0;
    stages.forEach(function (stage) {
      var blob = (stage.getAttribute("data-search") || "").toLowerCase();
      var textOk = !q || blob.indexOf(q) !== -1;
      var ok = stageMatches(stage) && textOk;
      stage.classList.toggle("hidden", !ok);
      if (ok) shown += 1;
    });
    count.textContent = shown + " 話";

    groups.forEach(function (group) {
      var kind = group.getAttribute("data-kind") || "";
      var kindOk = activeKind === "all" || kind === activeKind;
      var visible = 0;
      group.querySelectorAll(".name-card").forEach(function (card) {
        var blob = (card.getAttribute("data-search") || "").toLowerCase();
        var textOk = !q || blob.indexOf(q) !== -1;
        var ok = kindOk && textOk;
        card.classList.toggle("hidden", !ok);
        if (ok) visible += 1;
      });
      group.classList.toggle("hidden", visible === 0);
    });
  }

  function summaryText() {
    var parts = [];
    ROUTE.dimensions.forEach(function (dim) {
      var selected = choices[dim.id];
      if (!selected) return;
      dim.choices.forEach(function (choice) {
        if (choice.id === selected) parts.push(choice.label);
      });
    });
    if (!parts.length) return "目前顯示全部路線。";
    return "目前這條路：" + parts.join(" · ");
  }

  function markTree() {
    var id = (location.hash || "").slice(1);
    tree.querySelectorAll("a.ep").forEach(function (ep) {
      var on = (ep.getAttribute("href") || "") === "#" + id;
      ep.classList.toggle("current", on);
      if (on) ep.setAttribute("aria-current", "location");
      else ep.removeAttribute("aria-current");
    });
  }

  function paint() {
    var eva = choices.split === "eva";
    tree.querySelectorAll("[data-dim]").forEach(function (el) {
      if (!el.hasAttribute("data-choice")) return;
      var dim = el.getAttribute("data-dim");
      var choice = el.getAttribute("data-choice") || "";
      var selected = choices[dim] || "";
      var pressed = selected === choice;
      if (el.classList.contains("limb")) {
        el.classList.toggle("on", selected !== "" && pressed);
        el.classList.toggle("off", selected !== "" && !pressed);
        el.classList.toggle("open", selected === "");
      }
      if (el.tagName === "BUTTON") {
        el.setAttribute("aria-pressed", pressed ? "true" : "false");
        el.classList.toggle("is-on", pressed);
      }
    });
    tree.querySelectorAll(".after-split button[data-dim='finale']").forEach(function (el) {
      if (eva) el.setAttribute("aria-disabled", "true");
      else el.removeAttribute("aria-disabled");
    });
    var pathed = ROUTE.dimensions.some(function (dim) {
      return !!choices[dim.id];
    });
    tree.classList.toggle("is-pathed", pathed);
    if (choices.split) tree.dataset.split = choices.split;
    else delete tree.dataset.split;
    summary.textContent = summaryText();
    markTree();
  }

  function persist() {
    try {
      sessionStorage.setItem(CHOICE_KEY, JSON.stringify(choices));
      sessionStorage.setItem(FOLD_KEY, JSON.stringify(folds));
    } catch (err) {
      return;
    }
  }

  function setFold(fork, collapsed) {
    var panel = fork.querySelector(".limbs");
    var foldBtn = fork.querySelector(".fold");
    var title = fork.getAttribute("data-title") || "";
    fork.classList.toggle("is-collapsed", collapsed);
    if (collapsed) panel.setAttribute("hidden", "");
    else panel.removeAttribute("hidden");
    foldBtn.setAttribute("aria-expanded", collapsed ? "false" : "true");
    foldBtn.textContent = collapsed ? "展開話數" : "收合話數";
    foldBtn.setAttribute("aria-label", (collapsed ? "展開" : "收合") + title + "的話數");
    folds[fork.getAttribute("data-fork")] = collapsed;
  }

  function loadChoices() {
    var blank = {};
    ROUTE.dimensions.forEach(function (dim) {
      blank[dim.id] = "";
    });
    try {
      var raw = JSON.parse(sessionStorage.getItem(CHOICE_KEY) || "{}");
      ROUTE.dimensions.forEach(function (dim) {
        var value = raw && raw[dim.id] ? raw[dim.id] : "";
        var known = dim.choices.some(function (choice) {
          return choice.id === value;
        });
        blank[dim.id] = value && known ? value : "";
      });
    } catch (err) {
      return blank;
    }
    return blank;
  }

  function loadFolds() {
    try {
      var raw = JSON.parse(sessionStorage.getItem(FOLD_KEY) || "{}");
      if (!raw || typeof raw !== "object") return {};
      return raw;
    } catch (err) {
      return {};
    }
  }

  function stageFromHash() {
    var id = (location.hash || "").slice(1);
    if (!id) return null;
    var stage = document.getElementById(id);
    if (!stage || !stage.classList.contains("stage")) return null;
    return stage;
  }

  function revealStage(stage, clearSearch) {
    var changed = false;
    if (!stageMatches(stage)) {
      alignChoicesTo(stage);
      changed = true;
    }
    if (clearSearch) {
      var q = (input.value || "").trim().toLowerCase();
      var blob = (stage.getAttribute("data-search") || "").toLowerCase();
      if (q && blob.indexOf(q) === -1) {
        input.value = "";
        changed = true;
      }
    }
    if (!changed) return false;
    persist();
    paint();
    apply();
    return true;
  }

  nameChips.forEach(function (chip) {
    chip.addEventListener("click", function () {
      activeKind = chip.getAttribute("data-kind") || "all";
      nameChips.forEach(function (other) {
        other.classList.toggle("on", other === chip);
      });
      apply();
    });
  });

  input.addEventListener("input", apply);

  tree.addEventListener("click", function (event) {
    if (event.target.closest("#route-reset")) {
      ROUTE.dimensions.forEach(function (dim) {
        choices[dim.id] = "";
      });
      persist();
      paint();
      apply();
      return;
    }
    var foldBtn = event.target.closest(".fold");
    if (foldBtn && tree.contains(foldBtn)) {
      var fork = foldBtn.closest("[data-fork]");
      setFold(fork, foldBtn.getAttribute("aria-expanded") === "true");
      persist();
      return;
    }
    var pick = event.target.closest(".choice, .limb-pick");
    if (pick && tree.contains(pick)) {
      if (pick.getAttribute("aria-disabled") === "true") return;
      var dim = pick.getAttribute("data-dim");
      if (!dim || !Object.prototype.hasOwnProperty.call(choices, dim)) return;
      var choice = pick.getAttribute("data-choice") || "";
      if (pick.classList.contains("limb-pick") && choices[dim] === choice) choice = "";
      choices[dim] = choice;
      persist();
      paint();
      apply();
      return;
    }
    var ep = event.target.closest("a.ep");
    if (!ep || !tree.contains(ep)) return;
    var id = (ep.getAttribute("href") || "").slice(1);
    var stage = document.getElementById(id);
    if (!stage) return;
    var q = (input.value || "").trim().toLowerCase();
    var blob = (stage.getAttribute("data-search") || "").toLowerCase();
    var searchHides = q && blob.indexOf(q) === -1;
    if (stageMatches(stage) && !searchHides) return;
    event.preventDefault();
    revealStage(stage, true);
    window.requestAnimationFrame(function () {
      if (location.hash === "#" + id) stage.scrollIntoView({ block: "start" });
      else location.hash = id;
    });
  });

  tree.addEventListener("keydown", function (event) {
    var horizontal = event.key === "ArrowRight" || event.key === "ArrowLeft";
    var vertical = event.key === "ArrowDown" || event.key === "ArrowUp";
    if (!horizontal && !vertical) return;
    var group = event.target.closest(".choices");
    if (!group || !tree.contains(group)) return;
    var buttons = Array.prototype.slice.call(group.querySelectorAll("button"));
    var index = buttons.indexOf(document.activeElement);
    if (index < 0) return;
    event.preventDefault();
    var delta = event.key === "ArrowRight" || event.key === "ArrowDown" ? 1 : -1;
    buttons[(index + delta + buttons.length) % buttons.length].focus();
  });

  function mark() {
    var id = (location.hash || "#overview").slice(1);
    var links = nav.querySelectorAll("a.item");
    links.forEach(function (link) {
      var href = (link.getAttribute("href") || "").slice(1);
      link.classList.toggle("active", href === id);
    });
    markTree();
  }

  window.addEventListener("hashchange", function () {
    mark();
    var stage = stageFromHash();
    if (!stage) return;
    revealStage(stage, true);
    window.requestAnimationFrame(function () {
      stage.scrollIntoView({ block: "start" });
    });
  });

  choices = loadChoices();
  folds = loadFolds();
  tree.querySelectorAll("[data-fork]").forEach(function (fork) {
    var id = fork.getAttribute("data-fork");
    setFold(fork, !!folds[id]);
  });
  var openingStage = stageFromHash();
  if (openingStage) revealStage(openingStage, false);
  paint();
  apply();
  mark();
  if (openingStage) openingStage.scrollIntoView({ block: "start" });
})();
