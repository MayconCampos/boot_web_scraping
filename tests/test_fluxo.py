# Alterado pelo Codex: testes locais, sem acessar DataCG, banco ou Shift.
import importlib
import unittest
from datetime import date
from unittest.mock import Mock


class TestFluxo(unittest.TestCase):
    def test_dia20_executa_consolidado_depois_das_criticas(self):
        main = importlib.import_module('main')
        eventos = []
        main.executar(date(2026, 10, 20),
                      executar_criticas=lambda m, a: eventos.append(('criticas', m, a)),
                      executar_consolidado=lambda m, a: eventos.append(('consolidado', m, a)))
        self.assertEqual(eventos, [('criticas', 'Outubro', 2026), ('consolidado', 'Outubro', 2026)])

    def test_janeiro_antes_do_corte_preserva_periodos(self):
        main = importlib.import_module('main')
        critica, consolidado = Mock(), Mock()
        main.executar(date(2026, 1, 10), critica, consolidado)
        self.assertEqual([c.args for c in critica.call_args_list], [('Dezembro', 2025), ('Janeiro', 2026)])
        consolidado.assert_not_called()

    def test_falha_criticas_impede_consolidado(self):
        main = importlib.import_module('main')
        consolidado = Mock()
        with self.assertRaises(RuntimeError):
            main.executar(date(2026, 10, 20), Mock(side_effect=RuntimeError('falha')), consolidado)
        consolidado.assert_not_called()

    def test_etl_importavel_sem_executar(self):
        modulo = importlib.import_module('Ajuste_base_consolidado.df_consolidado')
        self.assertTrue(callable(modulo.transformar_consolidado))


if __name__ == '__main__':
    unittest.main()
