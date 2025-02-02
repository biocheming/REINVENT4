import pytest
from pathlib import Path

import torch

from reinvent.runmodes.TL.run_transfer_learning import run_transfer_learning
from reinvent.runmodes.utils.helpers import set_torch_device


@pytest.fixture
def setup(tmp_path, json_config, pytestconfig):
    device = pytestconfig.getoption("device")
    set_torch_device(device)

    output_model_file = tmp_path / "TL_libinvent.model"

    config = {
        "parameters": {
            "input_model_file": json_config["LIBINVENT_PRIOR_PATH"],
            "smiles_file": json_config["TL_LIBINVENT_SMILES_PATH"],
            "output_model_file": output_model_file,
            "save_every_n_epochs": 5,
            "batch_size": 64,
            "sample_batch_size": 128,
            "num_epochs": 5,
            "num_refs": 5,
        }
    }

    return config


@pytest.mark.integration
def test_transfer_learning(setup, tmp_path, pytestconfig):
    config = setup
    device = pytestconfig.getoption("device")

    run_transfer_learning(config, device)

    checkpoint_files = list(Path(tmp_path).glob("*.chkpt"))

    assert len(checkpoint_files) == 1

    model = torch.load(config["parameters"]["output_model_file"])
    keys = list(model.keys())

    assert keys == ["model_type", "version", "model", "decorator"]

    assert model["model_type"] == "Libinvent"
