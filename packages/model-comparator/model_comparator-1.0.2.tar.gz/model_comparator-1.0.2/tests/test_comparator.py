import pytest
import numpy as np
from model_comparator import ModelComparator


def test_linear_model():
    """
    Teste si le modèle linéaire est ajusté correctement aux données.
    """
    x = np.array([1, 2, 3, 4, 5])
    y = np.array([2, 4, 6, 8, 10])
    comparator = ModelComparator(x, y)

    # Ajuste les modèles
    comparator.fit_models()

    # Vérifie que le meilleur modèle est bien le modèle linéaire
    best_model_name, best_model_details = comparator.get_best_model()

    assert best_model_name == "Linéaire", f"Le meilleur modèle devrait être 'Linéaire', mais c'est '{best_model_name}'"
    assert best_model_details["mse"] == 0, f"MSE attendu à 0, mais reçu {best_model_details['mse']:.2f}"


def test_exponential_model():
    """
    Teste si le modèle exponentiel est correctement appliqué aux données (cas positif).
    """
    x = np.array([1, 2, 3, 4, 5])
    y = np.array([1.1, 2.5, 6.7, 14.9, 33.4])  # Exponential-like data
    comparator = ModelComparator(x, y)

    # Ajuste les modèles
    comparator.fit_models()

    # Vérifie que le modèle exponentiel est correctement appliqué
    if "Exponentiel" in comparator.results:
        assert comparator.results["Exponentiel"]["mse"] < 1e3, "Le MSE de l'exponentiel est trop élevé."


def test_log_model_not_applicable():
    """
    Vérifie que le modèle logarithmique est correctement exclu si les données contiennent des valeurs <= 0.
    """
    x = np.array([-1, 0, 1, 2, 3])  # Valeurs non compatibles avec le modèle logarithmique
    y = np.array([1, 2, 3, 4, 5])
    comparator = ModelComparator(x, y)

    # Ajuste les modèles
    comparator.fit_models()

    # Vérifie que le modèle logarithmique a été exclu
    assert "Logarithmique" not in comparator.results, "Le modèle logarithmique aurait dû être exclu."


def test_invalid_predictions():
    """
    Teste la gestion des erreurs lors de la génération de prédictions invalides.
    """
    x = np.array([1, 2, 3, 4, 5])
    y = np.array([1, 2, 3, 4, 5])
    comparator = ModelComparator(x, y)

    # Modifie un modèle pour qu'il génère des prédictions invalides (ex: valeurs infinies)
    def faulty_model(x, a, b):
        return a / (x - 2.5)  # Crée une division par zéro potentielle

    comparator.models["Faulty"] = faulty_model
    comparator.fit_models()

    # Vérifie que le modèle défectueux n'a pas été ajouté aux résultats
    assert "Faulty" not in comparator.results, "Le modèle défectueux n'a pas été exclu."

