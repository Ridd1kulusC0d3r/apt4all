/* tema claro/escuro: lembra a escolha e nunca quebra se o armazenamento estiver bloqueado */
(function () {
  var K = "apt4all-theme";
  try { var t = localStorage.getItem(K); if (t) document.documentElement.dataset.theme = t; } catch (e) {}
  // rótulos bilíngues do cabeçalho (data-pt / data-en); as páginas chamam window.TEMA_LANG(L)
  window.TEMA_LANG = function (L) {
    document.querySelectorAll("[data-pt][data-en]").forEach(function (e) { e.textContent = e.dataset[L] || e.dataset.pt; });
  };
  document.addEventListener("DOMContentLoaded", function () {
    var L = "pt"; try { L = localStorage.getItem("apt4all-lang") || ((navigator.language || "pt").indexOf("pt") === 0 ? "pt" : "en"); } catch (e) {}
    window.TEMA_LANG(L);
  });
  document.addEventListener("click", function (e) {
    var b = e.target.closest("[data-tema]"); if (!b) return;
    var cur = document.documentElement.dataset.theme ||
      (matchMedia("(prefers-color-scheme:dark)").matches ? "dark" : "light");
    var next = cur === "dark" ? "light" : "dark";
    document.documentElement.dataset.theme = next;
    try { localStorage.setItem(K, next); } catch (x) {}
    document.dispatchEvent(new CustomEvent("apt4all:tema", { detail: next }));
  });
})();
