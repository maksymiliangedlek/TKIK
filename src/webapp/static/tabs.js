// Switch HTML / CSS / Preview tabs
var tabs = document.querySelectorAll(".tab");

for (var i = 0; i < tabs.length; i++) {
  tabs[i].addEventListener("click", function () {
    var name = this.getAttribute("data-tab");
    for (var j = 0; j < tabs.length; j++) {
      tabs[j].classList.toggle("active", tabs[j].getAttribute("data-tab") === name);
    }
    document.getElementById("htmlOut").classList.toggle("active", name === "html");
    document.getElementById("cssOut").classList.toggle("active", name === "css");
    document.getElementById("previewOut").classList.toggle("active", name === "preview");
  });
}

// Editor line numbers + error-line emphasis
var textarea = document.getElementById("source");
var gutter = document.getElementById("gutter");
var errorLines = new Set();

if (window.ERROR_LINES) {
  window.ERROR_LINES.split(",").forEach(function (s) {
    var n = parseInt(s, 10);
    if (n > 0) errorLines.add(n);
  });
}

function lineCount(text) {
  if (!text) return 1;
  return text.split("\n").length;
}

function renderGutter() {
  if (!textarea || !gutter) return;
  var total = lineCount(textarea.value);
  var html = "";
  for (var n = 1; n <= total; n++) {
    var cls = errorLines.has(n) ? "line error" : "line";
    html += '<span class="' + cls + '">' + n + "</span>";
  }
  gutter.innerHTML = html;
}

function syncGutterScroll() {
  if (!textarea || !gutter) return;
  gutter.scrollTop = textarea.scrollTop;
}

if (textarea) {
  renderGutter();
  textarea.addEventListener("input", renderGutter);
  textarea.addEventListener("scroll", syncGutterScroll);
}

// Jump to error line when clicking an error message
var errorList = document.getElementById("errorList");
if (errorList) {
  errorList.addEventListener("click", function (event) {
    var item = event.target.closest("[data-line]");
    if (!item) return;
    var line = parseInt(item.getAttribute("data-line"), 10);
    if (!line) return;
    var textarea = document.getElementById("source");
    var lines = textarea.value.split("\n");
    var pos = 0;
    for (var k = 0; k < line - 1 && k < lines.length; k++) {
      pos += lines[k].length + 1;
    }
    textarea.focus();
    var len = (lines[line - 1] || "").length;
    textarea.setSelectionRange(pos, pos + len);
    textarea.classList.add("error-focus");
    setTimeout(function () {
      textarea.classList.remove("error-focus");
    }, 1200);
    var lineHeight = parseFloat(getComputedStyle(textarea).lineHeight) || 18;
    textarea.scrollTop = Math.max(0, (line - 1) * lineHeight - textarea.clientHeight * 0.35);
    syncGutterScroll();
  });
}
