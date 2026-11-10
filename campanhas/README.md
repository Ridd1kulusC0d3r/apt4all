# Campanhas: da fonte à hipótese defensiva

[Abrir o caderno de campanhas](https://ridd1kulusc0d3r.github.io/apt4all/campanhas/) · [English](README.en.md) · [Fonte de dados editorial](../dados/campanhas/cybermonitor.json)

O CyberMonitor já fazia parte dos recursos do APT4ALL. Esta integração acrescenta uma seleção de relatos com aplicação analítica: fonte primária → observação → telemetria → hipótese de hunting → lacunas → plano de validação. O catálogo complementa os perfis do Atlas sem alterar sua resolução de aliases ou sua pontuação de ameaça.

## Seleção inicial

| Caso | Publicador e data original | Perfil existente | Objetivo do exercício |
|---|---|---|---|
| [APT41 / DUST](https://cloud.google.com/blog/topics/threat-intelligence/apt41-arisen-from-dust) | Mandiant, 18/07/2024 | APT41 · G0096 | Correlacionar eventos do servidor, banco de dados e tráfego de saída |
| [Volt Typhoon](https://www.microsoft.com/en-us/security/blog/2023/05/24/volt-typhoon-targets-us-critical-infrastructure-with-living-off-the-land-techniques/) | Microsoft, 24/05/2023 | Volt Typhoon · G1017 | Distinguir administração autorizada de sequências suspeitas |
| [FoggyWeb](https://www.microsoft.com/security/blog/2021/09/27/foggyweb-targeted-nobelium-malware-leads-to-persistent-backdoor/) | Microsoft, 27/09/2021 | APT29 · G0016; nome na fonte: NOBELIUM | Avaliar visibilidade no servidor de federação |
| [Turla / Crutch](https://www.welivesecurity.com/2020/12/02/turla-crutch-keeping-back-door-open/) | ESET, 02/12/2020 | Turla · G0010 | Examinar uso anômalo de armazenamento externo |
| [Machete](https://www.welivesecurity.com/2019/08/05/sharpening-machete-cyberespionage/) | ESET, 05/08/2019 | Machete · G0095 | Construir uma linha do tempo de e-mail e endpoint na investigação regional |
| [Operation Spalax](https://www.welivesecurity.com/2021/01/12/operation-spalax-targeted-malware-attacks-colombia/) | ESET, 12/01/2021 | Sem vínculo atribuído no Atlas | Investigar uma campanha sem transformar malware compartilhado em identidade de ator |

Os IDs de técnicas são mapeamentos propostos pela curadoria do APT4ALL. A validação estrutural confirma sua presença na base local; não demonstra cobertura de detecção. Os links de ator são editoriais e explícitos. No caso NOBELIUM, consulte a associação descrita na [página ATT&CK de APT29](https://attack.mitre.org/groups/G0016/); nomes associados não são uma equivalência universal entre todos os clusters dos fornecedores.

## Como usar

1. Escolha o caso pelo problema do seu ambiente. Use busca, recorte regional ou ano no caderno.
2. Abra o relato original e confira a seção indicada em cada ficha. Registre evidência e interpretação separadamente.
3. Verifique quais campos e eventos realmente existem no seu SIEM/EDR. Registre coleta ausente como lacuna, não como cobertura.
4. Escreva uma hipótese com escopo, janela de tempo, entidades correlacionadas e comportamento esperado.
5. Monte eventos sintéticos positivos e controles benignos. Registre resultado, falsos positivos, versão do backend e ajustes.
6. Só então desenvolva uma regra Sigma, KQL, SPL ou Wazuh adequada à telemetria disponível. Conversão de sintaxe, isoladamente, não comprova eficácia.

Entregáveis: [ficha de relatório](../trilha/modelos/ficha-relatorio.md), [tabela de cobertura](../trilha/modelos/cobertura.md) e [registro de triagem](../trilha/modelos/registro-triagem.md). Para a modelagem do ambiente, leve as evidências revisadas para a [ponte TCE](../tce/README.md).

## O que foi aproveitado do HTML fornecido

`APT_Intelligence_Hub.html` foi lido como material de referência. Seu SHA-256 está no manifesto para identificar a versão analisada.

| Elemento | Decisão |
|---|---|
| Telemetria, justificativa e lacunas por caso | Incorporados como campos bilíngues e plano de validação |
| Busca e acesso à ficha do ator | Integrados ao caderno e à navegação do Atlas |
| Base embutida de 636 entidades | Não importada: há sobreposição com o Atlas e correspondências por alias que exigiriam revisão independente |
| 19 regras e conversões apresentadas como validadas | Não promovidas a regras do projeto: faltam os testes e resultados reproduzíveis; 17 das 19 regras não têm campo `references` |
| Catálogo genérico de 292 ferramentas IR | Não duplicado; o APT4ALL já tem curadoria temática de recursos |
| Contagens de amostras e agregados de técnicas | Não usados como pontuação de ameaça ou cobertura operacional |

Um exemplo concreto do limite das regras: a regra de password spraying no anexo seleciona falhas de login, enquanto a correlação entre usuários e janela temporal aparece em consultas separadas. A regra de Outlook menciona WebDAV no título, mas sua seleção de portas contém apenas 445 e 139. Esses pontos precisam de revisão semântica, além de validação de sintaxe.

## Proveniência e limites

- Acervo consultado: [CyberMonitor/APT_CyberCriminal_Campagin_Collections](https://github.com/CyberMonitor/APT_CyberCriminal_Campagin_Collections), commit `cbf136e24f5d2a4d89619580455aae8b9b0aeadb`, de 25/07/2024. É um recorte histórico, não um feed de atividade atual.
- A seleção usa o README para descoberta e o `index.csv` para metadados de documentos. Os links de arquivo estão fixados no commit consultado; os links primários continuam apontando aos publicadores.
- O JSON preserva publicação original, data do diretório, data declarada no índice e revisão editorial. APT41/DUST exemplifica a divergência: 18/07/2024 na página original e 19/07/2024 no acervo. A revisão em 09/11/2026 não indica atividade da campanha nessa data.
- `sha1_declarado` vem do índice; `git_blob_sha` identifica o objeto Git. Eles são campos diferentes. Os bytes dos PDFs não foram baixados para confirmar seus hashes.
- Não foi encontrada licença geral na raiz da coleção. A integração publica referências, metadados selecionados e sínteses próprias; documentos de terceiros permanecem na origem e conservam seus direitos. PDFs, amostras, códigos de ataque e listas de IOCs não foram espelhados.
- O gerador procura correspondências por URL normalizada ou SHA-1 declarado com APTnotes. A correspondência é registrada; não cria uma segunda evidência independente nem muda a base de atores. Ausência de correspondência exata não prova ineditismo do relato.
- As seis fontes primárias foram consultadas. As hipóteses de detecção não foram testadas em SIEM. Associação histórica ao ator não atribui um alerta atual a esse ator.
- Machete e Spalax enriquecem o recorte latino-americano; não foram classificadas como operações de origem brasileira.

## Manutenção

A fonte única é `dados/campanhas/cybermonitor.json`. Para acrescentar um caso, confira a fonte primária, a versão do acervo, possíveis duplicatas, o ator (ou ausência de atribuição), as datas e a distinção entre observação e proposta defensiva. Inclua textos PT/EN.

```bash
python3 ferramentas/campanhas/gerar_catalogo.py
python3 ferramentas/site/mastro.py
python3 ferramentas/site/gerar_paginas.py
python3 -m unittest discover -s testes -p 'test_campanhas.py' -v
```

O workflow semanal recompila a seleção já revisada; não importa automaticamente novas campanhas. O gerador falha se o vínculo ao Atlas ou os IDs de técnicas deixarem de existir, evitando uma associação silenciosa após mudanças na base. Não usa a data de execução para renovar a data editorial.
