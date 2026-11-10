"use strict";
(() => {
  const $ = s => document.querySelector(s);
  const esc = s => String(s ?? "").replace(/[&<>"']/g, c => ({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;","'":"&#39;"}[c]));
  const safe = u => { try { const p = new URL(u); return p.protocol === "https:" && !p.username && !p.password ? p.href : "#"; } catch (_) { return "#"; } };
  let L = "pt", data = null, failed = false;
  try { const saved = localStorage.getItem("apt4all-lang"); L = ["pt", "en"].includes(saved) ? saved : ((navigator.language || "pt").startsWith("pt") ? "pt" : "en"); } catch (_) {}
  const t = (pt, en) => L === "pt" ? pt : en;
  const val = (c, k) => esc(c[k][L]);
  const params = new URLSearchParams(location.search);
  let actor = params.get("ator") || "", campaign = params.get("campanha") || "";
  const link = (u, text) => `<a href="${esc(safe(u))}" target="_blank" rel="noopener noreferrer">${esc(text)} ↗</a>`;
  function render() {
    if (!data) {
      if (failed) $("#cases").textContent = t("Não foi possível carregar campanhas.json. Recarregue a página ou consulte o guia.", "Could not load campanhas.json. Reload the page or consult the guide.");
      return;
    }
    const q = $("#q").value.trim().toLocaleLowerCase();
    const cases = data.campanhas.filter(c => (!actor || c.ator_id === actor) && (!campaign || c.id === campaign)
      && (!$("#scope").value || c.recorte === $("#scope").value)
      && (!$("#year").value || c.publicado_em.startsWith($("#year").value))
      && (!q || q.split(/\s+/).every(w => JSON.stringify(c).toLocaleLowerCase().includes(w))));
    $("#count").textContent = `${cases.length} / ${data.campanhas.length} ` + t("campanhas", "campaigns")
      + ((actor || campaign) ? t(" · recorte do link ativo; use Limpar filtros para ver tudo", " · link filter active; use Clear filters to see all") : "");
    $("#cases").innerHTML = cases.map(c => {
      const profile = c.ator_id ? `<a href="../atlas/index.html#${encodeURIComponent(c.ator_id)}">${esc(c.ator_nome)} · ${esc(c.mitre_id)}</a>` : t("Sem ator atribuído no Atlas", "No attributed actor in the Atlas");
      const steps = [["telemetria", "01 · Telemetria a avaliar", "01 · Telemetry to assess"], ["hipotese", "02 · Hipótese de hunting", "02 · Hunting hypothesis"], ["lacunas", "03 · Lacunas e falsos positivos", "03 · Gaps and false positives"], ["validar", "04 · Como validar", "04 · How to validate"]];
      return `<article class="case" id="${esc(c.id)}">
        <div class="meta">${esc(c.publicado_em)} · ${esc(c.publicador)} · ${val(c,"foco")}</div>
        <h2>${esc(c.titulo)}</h2><p>${profile}</p>
        <p class="evidence">${val(c,"observacao")}</p>
        <div class="links">${link(c.fonte_primaria, t("Relato original", "Original report"))}${link(c.arquivo_cybermonitor, t("Arquivo no commit consultado", "Archive at reviewed commit"))}<a href="?campanha=${encodeURIComponent(c.id)}">${t("Link deste caso", "Case link")}</a></div>
        <details ${campaign === c.id ? "open" : ""}><summary>${t("Examinar evidências e hipótese defensiva", "Examine evidence and defensive hypothesis")}</summary>
        <p class="note"><b>${t("Localizar no relato", "Locate in the report")}:</b> ${esc(c.localizador)}<br><b>${t("Nome usado pela fonte", "Source label")}:</b> ${esc(c.ator_na_fonte)}<br><b>${t("Fonte consultada; hipótese não testada", "Source consulted; hypothesis not tested")}</b></p>
        <div class="steps">${steps.map(([key, pt, en]) => `<section><h3>${t(pt,en)}</h3><p>${val(c,key)}</p></section>`).join("")}</div>
        <p><b>${t("Mapeamento proposto pela curadoria", "Editorial mapping proposal")}:</b> ${c.tecnicas.map(id => link("https://attack.mitre.org/techniques/" + id.replace(".","/") + "/", id)).join(" · ")}</p>
        <p class="note">${val(c,"nota")}</p>
        <p class="note">${t("Publicação original", "Original publication")}: ${esc(c.publicado_em)} · ${t("Diretório do acervo", "Archive directory")}: ${esc(c.data_diretorio)} · ${t("Revisão editorial", "Editorial review")}: ${esc(c.revisado_em)}.<br>${t("Essas datas não são a data de um incidente observado no seu ambiente.", "These dates are not the date of an incident observed in your environment.")}</p>
        ${c.fonte_vinculo_ator ? `<p class="note">${link(c.fonte_vinculo_ator,t("Referência do vínculo ao Atlas", "Atlas relationship reference"))}</p>` : ""}
        ${c.aptnotes_correspondencias.length ? `<p class="note">${t("Correspondência no APTnotes (sem duplicar a base de atores)", "APTnotes cross-reference (without duplicating the actor database)")}: ${c.aptnotes_correspondencias.map(r=>link(r.url,r.titulo)).join(" · ")}</p>` : ""}
        <p class="note">${t("Proveniência e hashes declarados dos documentos estão no JSON. Os PDFs não foram copiados para o APT4ALL.", "Provenance and declared document hashes are available in JSON. PDFs were not copied into APT4ALL.")}</p>
        </details></article>`;
    }).join("") || `<p class="state">${t("Nenhuma campanha neste recorte. Limpe os filtros para voltar ao catálogo.", "No campaigns match. Clear the filters to return to the catalog.")}</p>`;
  }
  function language() {
    document.documentElement.lang = L === "pt" ? "pt-BR" : "en";
    document.title = "APT4ALL · " + t("Campanhas e evidências", "Campaigns and evidence");
    window.TEMA_LANG(L);
    document.querySelectorAll(".seg button").forEach(b => b.setAttribute("aria-pressed", b.dataset.l === L));
    render();
  }
  document.querySelector(".seg").addEventListener("click", e => { const b=e.target.closest("button[data-l]"); if(!b)return;L=b.dataset.l;try{localStorage.setItem("apt4all-lang",L)}catch(_){}language(); });
  ["#q", "#scope", "#year"].forEach(s => $(s).addEventListener("input", render));
  $("#clear").addEventListener("click", () => { actor="";campaign="";$("#q").value="";$("#scope").value="";$("#year").value="";history.replaceState(null,"",location.pathname);render(); });
  language();
  fetch("campanhas.json").then(r=>{if(!r.ok)throw Error(r.status);return r.json()}).then(d=>{
    data=d;
    [["#total","n_campanhas"],["#actors","n_com_ator"],["#latam","n_latam"],["#review","revisado_em"]].forEach(([id,k])=>$(id).textContent=d.meta[k]);
    [...new Set(d.campanhas.map(c=>c.publicado_em.slice(0,4)))].sort().reverse().forEach(y=>{const o=document.createElement("option");o.value=y;o.textContent=y;$("#year").append(o)});
    render();
  }).catch(()=>{failed=true;render();});
})();
