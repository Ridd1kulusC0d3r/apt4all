<div align="center">

<img src="assets/banner.svg" alt="APT4ALL: todo ator, um lugar só" width="100%">

# ◆ APT4ALL

**Todo ator de ameaça, um lugar só.** Atlas aberto e bilíngue de grupos APT, crime cibernético e malware,
com perfil de ameaça por país e setor, curadoria de recursos e trilha de estudo para analistas de CTI.

`1.0 "Sala de Guerra"` · DEIVOSINT · English: [README.en.md](README.en.md)

**leia o padrão · ouça o silêncio · posicione-se e espere**

[![Atlas](https://img.shields.io/badge/Atlas-abrir%20no%20navegador-5EE6C4?style=flat-square)](https://ridd1kulusc0d3r.github.io/apt4all/atlas/)
[![ATT&CK](https://img.shields.io/badge/ATT%26CK-v19.2-F4BE3F?style=flat-square)](https://attack.mitre.org/)
[![Código MIT](https://img.shields.io/badge/c%C3%B3digo-MIT-1F2B29?style=flat-square)](LICENSE)
[![Conteúdo CC BY 4.0](https://img.shields.io/badge/conte%C3%BAdo-CC%20BY%204.0-1F2B29?style=flat-square)](LICENSE-CONTEUDO.md)

</div>

---

> **Comece por aqui, uma coisa só:** abra o [Atlas](https://ridd1kulusc0d3r.github.io/apt4all/atlas/) e clique no Brasil.
> Depois disso, o [COMECE-AQUI.md](COMECE-AQUI.md) leva você ao próximo passo.

## Por que ele existe

Um mesmo grupo tem dez nomes: APT28 é Fancy Bear, Sofacy, Forest Blizzard, STRONTIUM, Sednit... Cada fornecedor batiza do seu jeito, e o analista perde horas cruzando planilha, MISP e ATT&CK. O APT4ALL junta essas fontes abertas, resolve os apelidos com uma regra auditável e entrega tudo em um mapa que responde três perguntas:

1. **Quem é esse ator?** (todos os nomes, país atribuído, motivação, técnicas, ferramentas, operações, relatórios)
2. **Quem ataca organizações como a minha?** (perfil por país e setor, com camada do ATT&CK Navigator)
3. **Por onde eu estudo isso direito?** (186 recursos curados e uma trilha de 9 módulos)

## O que tem aqui

| Porta | O que faz | Onde |
|---|---|---|
| 🗺️ **Atlas de sala de guerra** | Mapa hexagonal por país, dossiê do país, ficha de cada ator, ranking | [`docs/atlas/`](docs/atlas/) · [online](https://ridd1kulusc0d3r.github.io/apt4all/atlas/) |
| 🌊 **Fluxos e Rede** | Sankey país → motivação → tática → técnica; rede de técnicas compartilhadas; o mesmo para ferramentas de 92 gangues de ransomware | [Atlas → Fluxos](https://ridd1kulusc0d3r.github.io/apt4all/atlas/#fluxos) · [Rede](https://ridd1kulusc0d3r.github.io/apt4all/atlas/#rede) |
| 🎯 **Perfil de ameaça** | País + setor → atores prováveis, técnicas a cobrir, camada do Navigator, sinal para o TCE | [Atlas → Perfil](https://ridd1kulusc0d3r.github.io/apt4all/atlas/#perfil) · [`ferramentas/tce/`](ferramentas/tce/) |
| 📚 **Recursos** | 186 links em 21 categorias, bilíngues, com legado marcado, filtro para a sua lista original e verificação mensal | [RECURSOS.md](RECURSOS.md) · [online](https://ridd1kulusc0d3r.github.io/apt4all/recursos/) |
| 🧭 **Trilha** | 9 módulos, do nome do grupo ao dossiê final, cada um com uma ação "faça agora" | [`trilha/`](trilha/) |
| 🔗 **Ponte com o TCE** | Leva o perfil de ameaça para a modelagem de ameaças do ambiente inteiro | [`tce/`](tce/) |
| 📖 **Manual ilustrado** | Passo a passo com telas anotadas, para quem nunca usou | [`docs/manual/`](docs/manual/) · [online](https://ridd1kulusc0d3r.github.io/apt4all/manual/) |

## A base em números

Rodada de 13/10/2026, gerada por [`construir_dados.py`](ferramentas/atlas/construir_dados.py). O detalhe por país está em [`dados/gerados/resumo.md`](dados/gerados/resumo.md).

| | |
|---|---|
| Registros lidos | 2.494 (planilha 411 · MISP 1.060 · ATT&CK 176 · EternalLiberty 847) |
| Atores após resolver os apelidos | **1.355** |
| Apelidos catalogados | 2.598 |
| Atores com perfil ATT&CK | 184 |
| Técnicas ATT&CK ligadas | 498 |
| Relatórios públicos ligados (APTnotes) | 412 |
| Ransomware Tool Matrix | 92 grupos · 347 ferramentas · 1.060 usos (39 ligados a atores do Atlas) |
| Países com atores atribuídos | 43, mais o bloco OTAN / Five Eyes |
| Maiores origens atribuídas | China 289 · Rússia 156 · Irã 82 · Coreia do Norte 25 |
| Sem país atribuído | 638 (quase todos crime cibernético e hacktivismo) |

## Rodar no seu computador (dois cliques)

Precisa só de Python 3.9 ou mais novo. Nada para instalar com `pip`.

| Sistema | Clique duas vezes em |
|---|---|
| Windows | `iniciar-windows.bat` |
| macOS | `iniciar-mac.command` |
| Linux | `iniciar-linux.sh` |

O navegador abre sozinho em `http://localhost:8765`. Para fechar, feche a janela preta do terminal. O [manual](docs/manual/index.html) mostra cada tela.

Pela linha de comando:

```bash
git clone https://github.com/Ridd1kulusC0d3r/apt4all && cd apt4all
python3 -m http.server 8765 --directory docs      # Atlas e recursos
python3 ferramentas/tce/perfil_ameaca.py --pais BR --setor finance --saida saida/br-financas
```

## Como os dados se mantêm vivos

| Quando | O quê | Workflow |
|---|---|---|
| Toda segunda, 06:00 UTC | Baixa MISP, ATT&CK, planilha, EternalLiberty, APTnotes e Ransomware Tool Matrix; reconstrói o Atlas e abre um PR | [`atualizar-dados.yml`](.github/workflows/atualizar-dados.yml) |
| Todo dia 1º | Verifica os 186 links e abre issue se algum morreu | [`verificar-links.yml`](.github/workflows/verificar-links.yml) |
| A cada push e PR | Roda os testes | [`testes.yml`](.github/workflows/testes.yml) |
| A cada push na `main` | Publica `docs/` no GitHub Pages | [`pages.yml`](.github/workflows/pages.yml) |

## Estrutura

```
apt4all/
├── docs/                    site (GitHub Pages)
│   ├── index.html           página inicial
│   ├── atlas/               Atlas de sala de guerra + atores.json, paises.json, mapa.json, ransomware.json
│   ├── recursos/            busca nos recursos
│   └── manual/              manual ilustrado
├── ferramentas/
│   ├── atlas/               construir_dados.py (fontes → base), mapa_hex.py (mapa)
│   ├── recursos/            verificar_links.py, gerar_listas.py
│   ├── ransomware/          construir_matriz.py (Ransomware Tool Matrix → ransomware.json)
│   ├── tce/                 perfil_ameaca.py (ponte com o TCE)
│   └── manual/              capturar_telas.py (telas do manual, opcional)
├── recursos/recursos.json   fonte única dos recursos (edite aqui)
├── trilha/                  trilha de estudo, 9 módulos
├── tce/                     análise do TCE e uso da ponte
├── dados/                   brutos (fontes) e gerados (resumo, links)
├── testes/                  testes com unittest (só biblioteca padrão)
└── iniciar-*                lançadores de dois cliques
```

## Uso responsável

- **Atribuição é afirmação, não fato.** O APT4ALL reúne o que fornecedores e governos dizem, com a fonte de cada dado. Confirme na origem antes de citar.
- **Aqui não tem malware.** Os recursos de amostras apontam para repositórios de terceiros e vêm com aviso: só em laboratório isolado.
- **Nível defensivo.** A trilha ensina a ler, mapear, priorizar e detectar. Procedimento de ataque fica fora.

## Ecossistema

| Projeto | Relação |
|---|---|
| [Cyber-Threat-Context-Modeling (TCE)](https://github.com/Ridd1kulusC0d3r/Cyber-Threat-Context-Modeling) | Modelagem de ameaças do ambiente inteiro; recebe o perfil do APT4ALL como sinal de inteligência |
| [TOCAIA OSINT Linux](https://github.com/Ridd1kulusC0d3r/TOCAIALinux) | Distribuição de OSINT; mesma identidade visual |

## Contribuir, citar, licença

- Como contribuir: [CONTRIBUTING.md](CONTRIBUTING.md) (o caminho mais curto é editar `recursos/recursos.json` e abrir um PR)
- Fontes e licenças de cada dado: [FONTES.md](FONTES.md)
- Como citar: [CITATION.cff](CITATION.cff)
- Código sob [MIT](LICENSE); textos sob [CC BY 4.0](LICENSE-CONTEUDO.md); dados de terceiros com a licença de origem
- Relatório de testes: [RELATORIO-DE-TESTES.md](RELATORIO-DE-TESTES.md)

<div align="center"><sub>® MITRE ATT&CK é marca registrada da The MITRE Corporation. O APT4ALL não tem relação com a MITRE nem com os fornecedores citados.</sub></div>
