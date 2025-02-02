import unittest

import torch.utils.data as tud

from reinvent.models.linkinvent.dataset.dataset import Dataset
from tests.test_data import WARHEAD_PAIR
from tests.models.unit_tests.linkinvent.fixtures import mocked_linkinvent_model


class TestLinkInventModel(unittest.TestCase):
    def setUp(self):

        self.smiles = WARHEAD_PAIR
        self._model = mocked_linkinvent_model()

        ds1 = Dataset([self.smiles], self._model.vocabulary.input)
        self.data_loader_1 = tud.DataLoader(
            ds1, batch_size=32, shuffle=False, collate_fn=Dataset.collate_fn
        )

        ds2 = Dataset([self.smiles] * 2, self._model.vocabulary.input)
        self.data_loader_2 = tud.DataLoader(
            ds2, batch_size=32, shuffle=False, collate_fn=Dataset.collate_fn
        )

        ds3 = Dataset([self.smiles] * 3, self._model.vocabulary.input)
        self.data_loader_3 = tud.DataLoader(
            ds3, batch_size=32, shuffle=False, collate_fn=Dataset.collate_fn
        )

    def _sample_linker(self, data_loader):
        for batch in data_loader:
            return self._model.sample(*batch)

    def test_single_warheads_input(self):
        results = self._sample_linker(self.data_loader_1)

        self.assertEqual(1, len(results[0]))
        self.assertEqual(1, len(results[1]))
        self.assertEqual(1, len(results[2]))

    def test_double_warheads_input(self):
        results = self._sample_linker(self.data_loader_2)

        self.assertEqual(2, len(results[0]))
        self.assertEqual(2, len(results[1]))
        self.assertEqual(2, len(results[2]))

    def test_triple_warheads_input(self):
        results = self._sample_linker(self.data_loader_3)

        self.assertEqual(3, len(results[0]))
        self.assertEqual(3, len(results[1]))
        self.assertEqual(3, len(results[2]))
