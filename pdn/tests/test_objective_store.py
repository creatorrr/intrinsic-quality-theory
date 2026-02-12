from pathlib import Path

from persistent_diamonds_v3.data import IQTObjectiveDataStore, ObjectiveRequest, ObjectiveTensorDataset


def test_objective_store_reuse(tmp_path: Path):
    store = IQTObjectiveDataStore(tmp_path / "cache")
    request = ObjectiveRequest(
        objective="mixed",
        num_sequences=8,
        sequence_length=16,
        feature_dim=12,
        seed=42,
    )

    first = store.materialize(request)
    second = store.materialize(request)

    assert first.dataset_path.exists()
    assert first.reused is False
    assert second.reused is True

    ds = ObjectiveTensorDataset(first.dataset_path)
    item = ds[0]
    assert item["observations"].shape == (16, 12)
    assert item["targets"].shape == (16, 12)
    assert item["external_drive"].shape == (16, 12)
