/* Força e fatores do vínculo entre dois atores.
   Atribuição é hipótese: o vínculo mede o que dois perfis TÊM EM COMUM nas fontes, não prova que sejam o mesmo grupo nem que se coordenem.
   Cada fator é mostrado com a evidência (os itens em comum), para o analista conferir. Sem dependências; roda no navegador e no Node. */
(function (raiz, fabrica) {
  if (typeof module === "object" && module.exports) module.exports = fabrica();
  else raiz.Vinculos = fabrica();
})(typeof self !== "undefined" ? self : this, function () {
  "use strict";
  // pesos somam 100; o limiar separa fraco, médio e forte
  var FATORES = [
    { id: "tecnicas", peso: 35 }, { id: "ferramentas", peso: 20 }, { id: "relatorios", peso: 15 },
    { id: "nomes", peso: 10 }, { id: "setores", peso: 10 }, { id: "motivo", peso: 5 }, { id: "pais", peso: 5 }
  ];
  var LIMIAR = { forte: 30, medio: 22, fraco: 16 };

  function conj(v) { var s = new Set(); (v || []).forEach(function (x) { if (x) s.add(String(x).trim().toLowerCase()); }); return s; }
  function inter(a, b) { var r = []; a.forEach(function (x) { if (b.has(x)) r.push(x); }); return r; }

  // peso de cada técnica = quão rara ela é entre os atores com ATT&CK (técnica comum a todo mundo não prova vínculo)
  function contexto(atores) {
    var df = {}, n = 0;
    atores.forEach(function (a) {
      if (!a.mitre || !a.mitre.tecnicas || !a.mitre.tecnicas.length) return;
      n++; new Set(a.mitre.tecnicas).forEach(function (t) { df[t] = (df[t] || 0) + 1; });
    });
    var idf = function (t) { return Math.log((n + 1) / ((df[t] || 0) + 1)) + 0.1; };
    return { n: n, idf: idf };
  }

  function nomes(a) { var s = conj([a.nome].concat(a.aliases || [])); return s; }

  function vinculo(a, b, ctx) {
    var ck = a.id < b.id ? a.id + "|" + b.id : b.id + "|" + a.id;
    ctx.cache = ctx.cache || new Map();
    if (ctx.cache.has(ck)) return ctx.cache.get(ck);
    var f = {}, ev = {};
    var ta = new Set((a.mitre && a.mitre.tecnicas) || []), tb = new Set((b.mitre && b.mitre.tecnicas) || []);
    var com = inter(ta, tb), uniao = new Set([].concat(Array.from(ta), Array.from(tb)));
    var num = 0, den = 0;
    uniao.forEach(function (t) { var w = ctx.idf(t); den += w; if (ta.has(t) && tb.has(t)) num += w; });
    f.tecnicas = den ? num / den : 0; ev.tecnicas = com;
    var fa = conj(a.ferramentas), fb = conj(b.ferramentas), fc = inter(fa, fb);
    f.ferramentas = (fa.size + fb.size - fc.length) ? fc.length / (fa.size + fb.size - fc.length) : 0; ev.ferramentas = fc;
    var ra = conj((a.relatorios || []).map(function (r) { return r.link; })), rb = conj((b.relatorios || []).map(function (r) { return r.link; })), rc = inter(ra, rb);
    f.relatorios = Math.min(1, rc.length / 3); ev.relatorios = rc;
    var na = nomes(a), nb = nomes(b), nc = inter(na, nb);
    f.nomes = nc.length ? 1 : 0; ev.nomes = nc;
    var sa = conj(a.setores), sb = conj(b.setores), sc = inter(sa, sb);
    f.setores = (sa.size + sb.size - sc.length) ? sc.length / (sa.size + sb.size - sc.length) : 0; ev.setores = sc;
    var ma = conj((a.motivos || []).filter(function (m) { return m !== "indefinido"; })), mb = conj((b.motivos || []).filter(function (m) { return m !== "indefinido"; })), mc = inter(ma, mb);
    f.motivo = mc.length ? 1 : 0; ev.motivo = mc;
    var mesmo = a.pais && a.pais !== "??" && a.pais === b.pais;
    f.pais = mesmo ? 1 : 0; ev.pais = mesmo ? [a.pais] : [];
    var score = 0, fatores = [];
    FATORES.forEach(function (x) {
      var pts = f[x.id] * x.peso; score += pts;
      fatores.push({ id: x.id, peso: x.peso, valor: f[x.id], pontos: pts, evidencia: ev[x.id] });
    });
    score = Math.round(score);
    var nivel = score >= LIMIAR.forte ? "forte" : score >= LIMIAR.medio ? "medio" : score >= LIMIAR.fraco ? "fraco" : "nenhum";
    // só país/motivo/setor em comum não é vínculo: exige ao menos um fator de conteúdo
    var conteudo = f.tecnicas > 0 || f.ferramentas > 0 || f.relatorios > 0 || f.nomes > 0;
    if (!conteudo) nivel = "nenhum";
    var res = { a: a.id, b: b.id, score: score, nivel: nivel, fatores: fatores };
    ctx.cache.set(ck, res);
    return res;
  }

  // vínculos de um ator com todos os outros, do mais forte ao mais fraco
  function relacionados(ator, atores, ctx, max, minimo) {
    var out = [];
    atores.forEach(function (b) {
      if (b.id === ator.id) return;
      var v = vinculo(ator, b, ctx);
      if (v.nivel !== "nenhum" && v.score >= (minimo || LIMIAR.fraco)) out.push(v);
    });
    out.sort(function (x, y) { return y.score - x.score || (x.b < y.b ? -1 : 1); });
    return out.slice(0, max || 8);
  }

  // os N atores mais bem ligados ENTRE SI (para o grafo): parte do par mais forte e vai somando quem tem mais
  // vínculo com o grupo já escolhido; assim o desenho é um aglomerado conectado, não pares soltos
  function nucleo(atores, ctx, n, minimo) {
    var peso = {}, melhor = null;
    function chave(x, y) { return x < y ? x + "|" + y : y + "|" + x; }
    for (var i = 0; i < atores.length; i++) for (var j = i + 1; j < atores.length; j++) {
      var v = vinculo(atores[i], atores[j], ctx);
      if (v.nivel === "nenhum" || v.score < minimo) continue;
      peso[chave(v.a, v.b)] = v.score;
      if (!melhor || v.score > melhor.score || (v.score === melhor.score && v.a + v.b < melhor.a + melhor.b)) melhor = v;
    }
    if (!melhor) return [];
    var ids = [melhor.a, melhor.b];
    while (ids.length < n) {
      var cand = null, soma = 0;
      for (var k = 0; k < atores.length; k++) {
        var id = atores[k].id; if (ids.indexOf(id) >= 0) continue;
        var t = 0; ids.forEach(function (o) { t += peso[chave(id, o)] || 0; });
        if (t > soma || (t === soma && t > 0 && cand && id < cand)) { soma = t; cand = id; }
      }
      if (!cand) break;
      ids.push(cand);
    }
    return ids;
  }

  return { nucleo: nucleo, FATORES: FATORES, LIMIAR: LIMIAR, contexto: contexto, vinculo: vinculo, relacionados: relacionados };
});
