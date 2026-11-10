"""Preserva atribuição, proveniência e limites do catálogo editorial."""
import csv
import unittest
from copy import deepcopy
from pathlib import Path
from _base import modulo, RAIZ

g = modulo('ferramentas/campanhas/gerar_catalogo.py', 'gerar_catalogo_campanhas')
ROOT = Path(RAIZ)
DADOS = g.ler_json(ROOT / 'dados/campanhas/cybermonitor.json')
ATORES = g.ler_json(ROOT / 'docs/atlas/atores.json')['atores']
TECNICAS = g.ler_json(ROOT / 'docs/atlas/paises.json')['tecnicas']


class TestCampanhas(unittest.TestCase):
    def gera(self, dados=None, notas=()):
        return g.gerar(dados or DADOS, ATORES, TECNICAS, notas)

    def test_publicado_reproduzivel(self):
        with (ROOT / 'dados/brutos/APTnotes.csv').open(encoding='utf-8', newline='') as f:
            notas = list(csv.DictReader(f))
        self.assertEqual(self.gera(notas=notas), g.ler_json(ROOT / 'docs/campanhas/campanhas.json'))

    def test_preserva_datas_divergentes_sem_renovar_evidencia(self):
        c = next(c for c in self.gera()['campanhas'] if c['id'] == 'apt41-dust-2024')
        self.assertEqual(c['publicado_em'], '2024-07-18')
        self.assertEqual(c['referencias_arquivadas'][0]['publicado_em_indice'], '2024-07-19')
        self.assertEqual(c['revisado_em'], '2026-11-09')
        self.assertNotIn('observed_at', c)

    def test_campanha_sem_atribuicao_permanece_sem_ator(self):
        c = next(c for c in self.gera()['campanhas'] if c['id'] == 'spalax-2021')
        self.assertIsNone(c['ator_id'])
        self.assertIsNone(c['ator_nome'])
        self.assertIsNone(c['mitre_id'])

    def test_rejeita_vinculo_inconsistente_com_atlas(self):
        d = deepcopy(DADOS)
        d['campanhas'][0]['ator_id'] = 'volt-typhoon'
        with self.assertRaisesRegex(ValueError, 'Vínculo'):
            self.gera(d)

    def test_rejeita_promocao_sem_testes(self):
        d = deepcopy(DADOS)
        d['campanhas'][0]['status_deteccao'] = 'validada'
        with self.assertRaises(ValueError):
            self.gera(d)

    def test_rejeita_tecnica_ausente(self):
        d = deepcopy(DADOS)
        d['campanhas'][0]['tecnicas'] = ['T9999']
        with self.assertRaisesRegex(ValueError, 'Técnica'):
            self.gera(d)

    def test_rejeita_url_executavel(self):
        d = deepcopy(DADOS)
        d['campanhas'][0]['fonte_primaria'] = 'javascript:alert(1)'
        with self.assertRaisesRegex(ValueError, 'HTTPS'):
            self.gera(d)

    def test_rejeita_url_duplicada_com_barra_final(self):
        d = deepcopy(DADOS)
        d['campanhas'][1]['fonte_primaria'] = d['campanhas'][0]['fonte_primaria'] + '/'
        with self.assertRaisesRegex(ValueError, 'duplicada'):
            self.gera(d)

    def test_rejeita_arquivo_mutavel(self):
        d = deepcopy(DADOS)
        d['campanhas'][0]['arquivo_cybermonitor'] = d['campanhas'][0]['arquivo_cybermonitor'].replace(d['fonte']['commit'], 'master')
        with self.assertRaisesRegex(ValueError, 'commit'):
            self.gera(d)

    def test_rejeita_amostra_no_lugar_de_documento(self):
        d = deepcopy(DADOS)
        d['campanhas'][0]['referencias_arquivadas'][0]['caminho'] += '.exe'
        with self.assertRaisesRegex(ValueError, 'PDF'):
            self.gera(d)

    def test_aptnotes_mesmo_documento_nao_funde_atores(self):
        c = DADOS['campanhas'][0]
        notas = [{'Title': 'Mesmo PDF, outro espelho', 'Link': 'https://example.org/report',
                  'SHA-1': c['referencias_arquivadas'][0]['sha1_declarado']}]
        result = self.gera(notas=notas)
        self.assertEqual(result['meta']['n_com_correspondencia_aptnotes'], 1)
        self.assertEqual(result['campanhas'][0]['aptnotes_correspondencias'][0]['criterio'], 'sha1_declarado')
        self.assertEqual(len(result['campanhas']), len(DADOS['campanhas']))
        self.assertEqual(result['campanhas'][0]['ator_id'], c['ator_id'])
        self.assertNotIn('aptnotes_correspondencias', DADOS['campanhas'][0])

    def test_titulo_igual_nao_prova_mesmo_documento(self):
        notas = [{'Title': DADOS['campanhas'][0]['titulo'], 'Link': 'https://example.org/unrelated', 'SHA-1': ''}]
        self.assertEqual(self.gera(notas=notas)['meta']['n_com_correspondencia_aptnotes'], 0)

    def test_nao_descarta_query_que_identifica_documento(self):
        self.assertNotEqual(g.url_chave('https://example.org/report?id=1'), g.url_chave('https://example.org/report?id=2'))


if __name__ == '__main__':
    unittest.main()
