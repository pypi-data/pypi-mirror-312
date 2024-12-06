from aleksis.core.util.apps import AppConfig


class DefaultConfig(AppConfig):
    name = "aleksis.apps.evalu"
    verbose_name = "EvaLU (Evaluation of teaching and lesson quality)"
    dist_name = "AlekSIS-App-EvaLU"

    urls = {
        "Repository": "https://edugit.org/katharineum/AlekSIS-App-EvaLU",
    }
    licence = "EUPL-1.2+"
    copyright_info = (([2021, 2022, 2023], "Jonathan Weth", "dev@jonathanweth.de"),)
