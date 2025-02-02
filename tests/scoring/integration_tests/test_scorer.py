import numpy as np
import pytest
from reinvent.scoring.scorer import Scorer
from numpy.testing import assert_array_almost_equal


@pytest.mark.integration
def test_geo_scorer():
    smiles = ["NCc1ccccc1", "NCc1ccccc1C(=O)O", "NCc1ccccc1C(F)", "NCc1ccccc1C(=O)F"]
    scorer_config_geo_mean = {
        "type": "geometric_mean",
        "component": [
            {
                "custom_alerts": {
                    "endpoint": [
                        {"name": "Unwanted SMARTS", "weight": 1, "params": {"smarts": ["F"]}}
                    ]
                }
            },
            {
                "MolecularWeight": {
                    "endpoint": [
                        {
                            "name": "Molecular weight",
                            "weight": 1,
                            "transform": {
                                "type": "double_sigmoid",
                                "high": 175.0,
                                "low": 25.0,
                                "coef_div": 500.0,
                                "coef_si": 20.0,
                                "coef_se": 20.0,
                            },
                        }
                    ]
                }
            },
            {"QED": {"endpoint": [{"name": "QED", "weight": 0.5}]}},
            {
                "MatchingSubstructure": {
                    "endpoint": [
                        {
                            "name": "MatchingSubstructure inline C=O",
                            "weight": 1,
                            "params": {"smarts": "C=O", "use_chirality": False},
                        }
                    ]
                }
            },
        ],
    }

    expected_result_geo_mean = [0.414360615, 0.810667745, 0, 0]
    geo_scorer = Scorer(scorer_config_geo_mean)
    geo_results = geo_scorer.compute_results(smiles, np.full(len(smiles), True, dtype=bool))

    assert_array_almost_equal(geo_results.total_scores, expected_result_geo_mean)
    assert (
        len(geo_results.completed_components) == 4
    )  # molecularweight, qed, custom alerts, matching subs


def test_arth_scorer():
    smiles = ["NCc1ccccc1", "NCc1ccccc1C(=O)O", "NCc1ccccc1C(F)", "NCc1ccccc1C(=O)F"]
    scorer_config_arth_mean = {
        "type": "arithmetic_mean",
        "component": [
            {
                "custom_alerts": {
                    "endpoint": [
                        {"name": "Unwanted SMARTS", "weight": 1, "params": {"smarts": ["F"]}}
                    ]
                }
            },
            {
                "MolecularWeight": {
                    "endpoint": [
                        {
                            "name": "Molecular weight",
                            "weight": 1,
                            "transform": {
                                "type": "double_sigmoid",
                                "high": 175.0,
                                "low": 25.0,
                                "coef_div": 500.0,
                                "coef_si": 20.0,
                                "coef_se": 20.0,
                            },
                        }
                    ]
                }
            },
            {"QED": {"endpoint": [{"name": "QED", "weight": 0.5}]}},
            {
                "MatchingSubstructure": {
                    "endpoint": [
                        {
                            "name": "MatchingSubstructure inline C=O",
                            "weight": 1,
                            "params": {"smarts": "C=O", "use_chirality": False},
                        }
                    ]
                }
            },
        ],
    }

    expected_result_arth_mean = [0.427841757, 0.819208403, 0, 0]
    arth_scorer = Scorer(scorer_config_arth_mean)
    arth_results = arth_scorer.compute_results(smiles, np.full(len(smiles), True, dtype=bool))
    assert_array_almost_equal(arth_results.total_scores, expected_result_arth_mean)
    assert (
        len(arth_results.completed_components) == 4
    )  # molecularweight, qed, custom alerts, matching subs
