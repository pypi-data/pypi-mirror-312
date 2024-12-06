import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
from sklearn.metrics import mean_squared_error, r2_score
import re


class ModelComparator:
    def __init__(self, x, y, custom_models=None):
        """
        Initialise le comparateur avec des données et des modèles intégrés ou personnalisés.

        :param x: array-like, valeurs des abscisses
        :param y: array-like, valeurs des ordonnées
        :param custom_models: dict, modèles supplémentaires {nom: fonction} (optionnel)
        """
        self.x = np.array(x)
        self.y = np.array(y)
        self.results = {}

        # Modèles intégrés par défaut
        self.models = {
            "Linéaire": {
                "function": self.modele_lin,
                "expression": "y = {a} + {b} * x"
            },
            "Quadratique": {
                "function": self.modele_quad,
                "expression": "y = {a} + {b} * x + {c} * x^2"
            },
            "Cubique": {
                "function": self.modele_cubic,
                "expression": "y = {a} + {b} * x + {c} * x^2 + {d} * x^3"
            },
            "Exponentiel": {
                "function": self.modele_exp,
                "expression": "y = {a} * exp({b} * x)"
            },
            "Logarithmique": {
                "function": self.modele_log,
                "expression": "y = {a} + {b} * log(x)"
            },
            "Puissance": {
                "function": self.modele_power,
                "expression": "y = {a} * x^{b}"
            },
            "Sinusoïdal": {
                "function": self.modele_sinus,
                "expression": "y = {a} + {b} * sin({c} * x)"
            },
        }

        # Ajouter des modèles personnalisés si fournis
        if custom_models:
            self.models.update(custom_models)

    # Définition des modèles intégrés
    def modele_lin(self, x, a, b):
        return a + b * x

    def modele_quad(self, x, a, b, c):
        return a + b * x + c * x ** 2

    def modele_cubic(self, x, a, b, c, d):
        return a + b * x + c * x ** 2 + d * x ** 3

    def modele_exp(self, x, a, b):
        return a * np.exp(b * x)

    def modele_log(self, x, a, b):
        return a + b * np.log(x)

    def modele_power(self, x, a, b):
        return a * x ** b

    def modele_sinus(self, x, a, b, c):
        return a + b * np.sin(c * x)

    def is_model_applicable(self, model_name):
        """
        Vérifie si un modèle peut être appliqué aux données.
        :param model_name: nom du modèle
        :return: bool, True si applicable, False sinon
        """
        if model_name == "Logarithmique":
            # Vérifie si x contient des valeurs positives strictes
            return np.all(self.x > 0)
        if model_name == "Puissance":
            # Vérifie si x contient des valeurs strictement positives
            return np.all(self.x > 0)
        return True  # Tous les autres modèles sont considérés comme applicables

    def fit_models(self, round=".2f"):
        """
        Ajuste chaque modèle applicable aux données et calcule les métriques.
        """
        for name, model_info in self.models.items():
            model_function = model_info["function"]

            if not self.is_model_applicable(name):
                print(f"Le modèle '{name}' n'est pas applicable aux données.")
                continue

            try:
                # Ajustement du modèle
                params, _ = curve_fit(model_function, self.x, self.y)

                # Prédictions
                y_pred = model_function(self.x, *params)

                # Vérification des résultats pour éviter les valeurs infinies ou NaN
                if np.any(np.isinf(y_pred)) or np.any(np.isnan(y_pred)):
                    raise ValueError("Prédictions invalides (NaN ou Inf) détectées.")

                # Calcul des métriques
                mse = mean_squared_error(self.y, y_pred)
                r2 = r2_score(self.y, y_pred)

                # Générer l'équation textuelle
                equation = self.format_model_equation(model_info["expression"], params, round)

                # Enregistrer les résultats
                self.results[name] = {
                    "params": params,
                    "mse": mse,
                    "r2": r2,
                    "y_pred": y_pred,
                    "equation": equation
                }
            except (RuntimeError, ValueError) as e:
                print(f"Le modèle '{name}' n'a pas pu être ajusté : {e}")

    def plot_models(self):
        """
        Trace les données originales et les modèles ajustés.
        """
        plt.figure(figsize=(12, 8))
        plt.scatter(self.x, self.y, color="black", label="Données expérimentales")

        for name, result in self.results.items():
            plt.plot(self.x, result["y_pred"], label=f"{name} (R²={result['r2']:.2f}, MSE={result['mse']:.2f})")

        plt.xlabel("x")
        plt.ylabel("y")
        plt.title("Comparaison des modèles d'ajustement")
        plt.legend()
        plt.show()

    def format_model_equation(self, expression, params, round):
        """
        Génère une représentation textuelle de l'équation du modèle avec les paramètres donnés.

        :param expression: Représentation textuelle du modèle (ex : "y = {a} * exp({b} * x)")
        :param params: Liste des paramètres ajustés pour le modèle
        :param precision: Chaîne de format pour arrondir les valeurs des paramètres (ex: '.3f' pour 3 décimales)
        :return: Chaîne de caractères représentant l'équation
        """
        # Utilisation d'une expression régulière pour capturer tous les paramètres entre accolades
        param_names = re.findall(r'\{(.*?)\}', expression)

        # Vérifier la cohérence entre les paramètres de l'expression et ceux fournis
        if len(param_names) != len(params):
            raise ValueError("Le nombre de paramètres ne correspond pas à la définition de l'expression.")

        # Associer les paramètres à leurs valeurs en appliquant le format de précision et formater l'expression
        param_dict = {name: f"{value:{round}}" for name, value in zip(param_names, params)}
        return expression.format(**param_dict)

    def get_best_model(self):
        """
        Retourne le meilleur modèle basé sur la MSE.

        :return: tuple, (nom du modèle, détails du modèle)
        """
        if not self.results:
            raise ValueError("Aucun modèle n'a été ajusté. Exécutez `fit_models()` d'abord.")

        best_model = min(self.results.items(), key=lambda item: item[1]["mse"])
        return best_model

    def summarize_results(self):
        """
        Affiche un résumé des performances des modèles.
        """
        if not self.results:
            raise ValueError("Aucun modèle n'a été ajusté. Exécutez `fit_models()` d'abord.")

        print("\nRésumé des modèles :")
        for model, metrics in self.results.items():
            print(f"{model} : MSE = {metrics['mse']:.4f}, R² = {metrics['r2']:.4f}")
