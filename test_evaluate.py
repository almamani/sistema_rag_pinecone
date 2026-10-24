import unittest

from evaluate import calcular_metricas


class TestMetricas(unittest.TestCase):
    def test_recuperacion_completa(self):
        resultado = calcular_metricas(
            ids_recuperados=["A", "B"],
            ids_relevantes=["A", "B"],
            k=2,
        )

        self.assertAlmostEqual(resultado["precision"], 1.0)
        self.assertAlmostEqual(resultado["recall"], 1.0)

    def test_recuperacion_parcial(self):
        resultado = calcular_metricas(
            ids_recuperados=["A", "C", "D", "E", "F"],
            ids_relevantes=["A", "B"],
            k=5,
        )

        self.assertAlmostEqual(resultado["precision"], 0.2)
        self.assertAlmostEqual(resultado["recall"], 0.5)

    def test_documentos_repetidos(self):
        resultado = calcular_metricas(
            ids_recuperados=["A", "A", "B"],
            ids_relevantes=["A", "B"],
            k=2,
        )

        self.assertAlmostEqual(resultado["precision"], 1.0)
        self.assertAlmostEqual(resultado["recall"], 1.0)

    def test_sin_aciertos(self):
        resultado = calcular_metricas(
            ids_recuperados=["C", "D"],
            ids_relevantes=["A"],
            k=2,
        )

        self.assertEqual(resultado["precision"], 0.0)
        self.assertEqual(resultado["recall"], 0.0)

    def test_relevante_fuera_del_top_k(self):
        resultado = calcular_metricas(
            ids_recuperados=["A", "B", "C"],
            ids_relevantes=["C"],
            k=2,
        )

        self.assertEqual(resultado["precision"], 0.0)
        self.assertEqual(resultado["recall"], 0.0)

    def test_menos_resultados_que_k(self):
        resultado = calcular_metricas(
            ids_recuperados=["A"],
            ids_relevantes=["A"],
            k=5,
        )

        self.assertAlmostEqual(resultado["precision"], 0.2)
        self.assertAlmostEqual(resultado["recall"], 1.0)

    def test_k_invalido(self):
        for k in [0, -1]:
            with self.subTest(k=k):
                with self.assertRaises(ValueError):
                    calcular_metricas(["A"], ["A"], k)

    def test_referencia_vacia(self):
        with self.assertRaises(ValueError):
            calcular_metricas(["A"], [], k=5)


if __name__ == "__main__":
    unittest.main()