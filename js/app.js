(function () {
  var nav = document.getElementById("nav");
  var btn = document.getElementById("menu");
  var input = document.getElementById("q");
  var count = document.getElementById("count");
  var stages = Array.prototype.slice.call(document.querySelectorAll(".stage"));
  var chips = Array.prototype.slice.call(document.querySelectorAll(".chips .chip"));
  var groups = Array.prototype.slice.call(document.querySelectorAll(".name-group"));
  var nameChips = Array.prototype.slice.call(document.querySelectorAll(".name-chip"));
  var activeGroup = "all";
  var activeKind = "all";

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

  function apply() {
    var q = (input.value || "").trim().toLowerCase();
    var shown = 0;
    stages.forEach(function (stage) {
      var group = stage.getAttribute("data-group") || "";
      var blob = (stage.getAttribute("data-search") || "").toLowerCase();
      var groupOk = activeGroup === "all" || group === activeGroup;
      var textOk = !q || blob.indexOf(q) !== -1;
      var ok = groupOk && textOk;
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

  chips.forEach(function (chip) {
    chip.addEventListener("click", function () {
      activeGroup = chip.getAttribute("data-group") || "all";
      chips.forEach(function (other) {
        other.classList.toggle("on", other === chip);
      });
      apply();
      var first = document.querySelector(".stage:not(.hidden)");
      if (first) first.scrollIntoView({ block: "start" });
    });
  });

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

  function mark() {
    var id = (location.hash || "#overview").slice(1);
    var links = nav.querySelectorAll("a.item");
    links.forEach(function (link) {
      var href = (link.getAttribute("href") || "").slice(1);
      link.classList.toggle("active", href === id);
    });
  }

  window.addEventListener("hashchange", mark);
  mark();
  apply();
})();
