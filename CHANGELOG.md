# Changelog

Formato baseado em [Keep a Changelog](https://keepachangelog.com/pt-BR/1.1.0/).

## [Não lançado]
- Vínculos entre atores: força de 0 a 100 (fraco, médio, forte) calculada por sete fatores com evidência (técnicas ATT&CK ponderadas pela raridade, ferramentas, relatórios, nomes, setores, motivação, país), na ficha do ator e numa nova vista da Rede. O vínculo mede o que os perfis têm em comum nas fontes; não prova que sejam o mesmo grupo.
- Feed vivo de vulnerabilidades exploradas (CISA KEV) com atribuições curadas, Atom e JSON, ingerido toda semana; seção "Vulnerabilidades exploradas" nos dossiês do Atlas.
- Novo visual em todo o site (papel, tinta e um tom de sinal; claro e escuro; sem fontes externas), cabeçalho único gerado por `ferramentas/site/mastro.py`, favicon, manual com telas refeitas.
- Removido o relatório de testes datado (o CI é a fonte da verdade); banner reduzido de 247 KB para menos de 2 KB.
- Plano de atualização automática (`PLANO-DE-ATUALIZACAO.md`), portão de qualidade (`ferramentas/atualizacao/portao.py`) no workflow semanal, aviso por issue e Dependabot para as Actions.

## [1.2]
- Site navegável completo (`docs/`): Atlas, Recursos, textos com menu lateral, manual ilustrado.

## [1.1]
- Fluxos (Sankey), rede de técnicas, ransomware e correção de números.

## [1.0] — "Sala de Guerra"
- Atlas, recursos, trilha de 9 módulos e ponte com o TCE.
