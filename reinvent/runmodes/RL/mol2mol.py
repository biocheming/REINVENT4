"""The Mol2Mol optimization algorithm"""

from __future__ import annotations

__all__ = ["Mol2MolLearning"]
import logging
from typing import TYPE_CHECKING

import torch
import numpy as np

from .learning import Learning
from reinvent.models.model_factory.mol2mol_adapter import SampledSequencesDTO
from reinvent.models.model_factory.sample_batch import SmilesState

if TYPE_CHECKING:
    from reinvent.scoring import ScoreResults

logger = logging.getLogger(__name__)


def get_distance_to_prior(likelihood, distance_threshold: float) -> np.ndarray:
    # FIXME: the datatype should not be variable
    if isinstance(likelihood, torch.Tensor):
        ones = torch.ones_like(likelihood, requires_grad=False)
        mask = torch.where(likelihood < distance_threshold, ones, distance_threshold / likelihood)
        mask = mask.cpu().numpy()
    else:
        ones = np.ones_like(likelihood)
        mask = np.where(likelihood < distance_threshold, ones, distance_threshold / likelihood)

    return mask


class Mol2MolLearning(Learning):
    """Mol2Mol optimization"""

    def score(self):
        """Compute the score for the SMILES stings."""

        prior_nll = self.prior.likelihood_smiles(self.sampled).likelihood
        distance_penalty = get_distance_to_prior(prior_nll, self.distance_threshold)

        mask = np.where(self.sampled.states == SmilesState.VALID, True, False)
        results = self.scoring_function(self.sampled.smilies, mask)
        results.total_scores *= distance_penalty

        return results

    def update(self, results: ScoreResults):
        likelihood_dto = self._state.agent.likelihood_smiles(self.sampled)
        batch = likelihood_dto.batch

        prior_nlls = self.prior.likelihood(
            batch.input, batch.input_mask, batch.output, batch.output_mask
        )

        agent_nlls = likelihood_dto.likelihood

        return self.reward_nlls(
            agent_nlls,
            prior_nlls,
            results.total_scores,
            self.inception,
            results.smilies,
            self._state.agent,
            np.argwhere(self.sampled.states == SmilesState.VALID).flatten(),
        )
