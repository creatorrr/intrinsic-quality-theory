from __future__ import annotations

import json
from pathlib import Path

import torch
import typer

from persistent_diamonds_v3.config import PersistentDiamondsConfig
from persistent_diamonds_v3.data import (
    CachedNarratorTextDataset,
    IQTObjectiveDataStore,
    ObjectiveRequest,
    ObjectiveTensorDataset,
    build_code_cache,
)
from persistent_diamonds_v3.evaluation import compute_iqt_bundle
from persistent_diamonds_v3.evaluation.protocols import (
    result_to_dict,
    run_protocol1,
    run_protocol2,
    run_protocol3,
)
from persistent_diamonds_v3.models import ControlHead, DiscreteNarrator, ModularSSMWorldModel, ReportHead
from persistent_diamonds_v3.data.env.gridworld import GridWorldConfig
from persistent_diamonds_v3.training import (
    DistillationTrainer,
    NarratorTextDataset,
    Stage1JEPATrainer,
    Stage2ShapingTrainer,
    Stage4EmbodiedTrainer,
    build_synthetic_distillation_corpus,
    load_tokenizer,
)

app = typer.Typer(help="Persistent Diamonds v3 (IQT architecture research package)")


def _load_config(config_path: Path) -> PersistentDiamondsConfig:
    if config_path.exists():
        return PersistentDiamondsConfig.from_yaml(config_path)
    cfg = PersistentDiamondsConfig()
    cfg.to_yaml(config_path)
    return cfg


def _build_world_narrator(cfg: PersistentDiamondsConfig):
    world = ModularSSMWorldModel(
        input_dim=cfg.world_model.input_dim,
        latent_dim=cfg.world_model.latent_dim,
        module_count=cfg.world_model.module_count,
        overlap_ratio=cfg.world_model.overlap_ratio,
        hidden_dim=cfg.world_model.hidden_dim,
        action_dim=cfg.world_model.action_dim,
    )
    narrator = DiscreteNarrator(
        latent_dim=cfg.world_model.latent_dim,
        hidden_dim=cfg.narrator.hidden_dim,
        window_size=cfg.narrator.window_size,
        update_hz=cfg.narrator.update_hz,
        codebook_size=cfg.narrator.codebook_size,
        codes_per_step=cfg.narrator.codes_per_step,
        code_dim=cfg.narrator.code_dim,
    )
    return world, narrator


def _build_control_head(cfg: PersistentDiamondsConfig) -> ControlHead:
    narrator_dim = cfg.narrator.codes_per_step * cfg.narrator.code_dim
    return ControlHead(
        narrator_dim=narrator_dim,
        action_dim=cfg.control_head.action_dim,
        hidden_dim=cfg.control_head.hidden_dim,
    )


def _build_report_head(cfg: PersistentDiamondsConfig, *, vocab_size_override: int | None = None) -> ReportHead:
    return ReportHead(
        codebook_size=cfg.narrator.codebook_size,
        vocab_size=vocab_size_override or cfg.report_head.vocab_size,
        model_dim=cfg.report_head.model_dim,
        layer_count=cfg.report_head.layer_count,
        head_count=cfg.report_head.head_count,
        ff_dim=cfg.report_head.ff_dim,
        dropout=cfg.report_head.dropout,
        max_seq_len=cfg.report_head.max_seq_len,
    )


def _load_weights(path: Path):
    try:
        return torch.load(path, map_location="cpu", weights_only=True)
    except TypeError:  # pragma: no cover - for older torch versions.
        return torch.load(path, map_location="cpu")


@app.command("init-config")
def init_config(config_path: Path = Path("pdv3.yaml")):
    cfg = _load_config(config_path)
    typer.echo(f"Config ready: {config_path}")
    typer.echo(f"Teacher model default: {cfg.distillation.teacher_model_name}")


@app.command("prepare-data")
def prepare_data(
    objective: str = "mixed",
    config_path: Path = Path("pdv3.yaml"),
    source_path: Path | None = None,
    num_sequences: int | None = None,
    sequence_length: int | None = None,
    feature_dim: int | None = None,
    seed: int = 17,
    force_generate: bool = False,
):
    cfg = _load_config(config_path)
    store = IQTObjectiveDataStore(cfg.data.cache_dir)

    request = ObjectiveRequest(
        objective=objective,  # type: ignore[arg-type]
        num_sequences=num_sequences or cfg.data.default_num_sequences,
        sequence_length=sequence_length or cfg.data.default_sequence_length,
        feature_dim=feature_dim or cfg.data.feature_dim,
        seed=seed,
        source_path=str(source_path) if source_path else None,
    )
    out = store.materialize(request, force_generate=force_generate)
    typer.echo(f"Dataset: {out.dataset_path}")
    typer.echo(f"Manifest: {out.manifest_path}")
    typer.echo(f"Reused: {out.reused}")


@app.command("train-stage1")
def train_stage1(
    objective: str = "mixed",
    config_path: Path = Path("pdv3.yaml"),
    checkpoint_path: Path = Path("artifacts/world_stage1.pt"),
):
    cfg = _load_config(config_path)
    store = IQTObjectiveDataStore(cfg.data.cache_dir)
    data = store.materialize(
        ObjectiveRequest(
            objective=objective,  # type: ignore[arg-type]
            num_sequences=cfg.data.default_num_sequences,
            sequence_length=cfg.data.default_sequence_length,
            feature_dim=cfg.data.feature_dim,
        )
    )

    dataset = ObjectiveTensorDataset(data.dataset_path)
    world, _ = _build_world_narrator(cfg)

    trainer = Stage1JEPATrainer(
        world,
        latent_dim=cfg.world_model.latent_dim,
        learning_rate=cfg.train.learning_rate,
        weight_decay=cfg.train.weight_decay,
        device=cfg.train.device,
    )
    result = trainer.train(
        dataset,
        batch_size=16,
        max_steps=min(cfg.train.max_steps, 2000),
    )

    checkpoint_path.parent.mkdir(parents=True, exist_ok=True)
    torch.save(world.state_dict(), checkpoint_path)

    typer.echo(f"Stage 1 complete. loss={result.final_loss:.4f} steps={result.steps}")
    typer.echo(f"Saved: {checkpoint_path}")


@app.command("train-stage2")
def train_stage2(
    objective: str = "mixed",
    config_path: Path = Path("pdv3.yaml"),
    world_checkpoint: Path | None = None,
    save_dir: Path = Path("artifacts"),
):
    cfg = _load_config(config_path)
    store = IQTObjectiveDataStore(cfg.data.cache_dir)

    data = store.materialize(
        ObjectiveRequest(
            objective=objective,  # type: ignore[arg-type]
            num_sequences=cfg.data.default_num_sequences,
            sequence_length=cfg.data.default_sequence_length,
            feature_dim=cfg.data.feature_dim,
        )
    )

    dataset = ObjectiveTensorDataset(data.dataset_path)
    world, narrator = _build_world_narrator(cfg)

    if world_checkpoint and world_checkpoint.exists():
        world.load_state_dict(_load_weights(world_checkpoint))

    trainer = Stage2ShapingTrainer(
        world_model=world,
        narrator=narrator,
        input_dim=cfg.world_model.input_dim,
        world_step_hz=cfg.narrator.world_step_hz,
        stage2_weights=cfg.stage2_weights,
        learning_rate=cfg.train.learning_rate,
        weight_decay=cfg.train.weight_decay,
        device=cfg.train.device,
    )

    result = trainer.train(
        dataset,
        batch_size=8,
        max_steps=min(cfg.train.max_steps, 2000),
    )

    save_dir.mkdir(parents=True, exist_ok=True)
    world_out = save_dir / "world_stage2.pt"
    narrator_out = save_dir / "narrator_stage2.pt"
    torch.save(world.state_dict(), world_out)
    torch.save(narrator.state_dict(), narrator_out)

    typer.echo(
        "Stage 2 complete. "
        f"loss={result.final_loss:.4f} rate={result.final_rate_bits_per_sec:.2f}bps steps={result.steps}"
    )
    typer.echo(f"Saved: {world_out}")
    typer.echo(f"Saved: {narrator_out}")


@app.command("train-distill")
def train_distill(
    config_path: Path = Path("pdv3.yaml"),
    objective_data: Path | None = None,
    world_checkpoint: Path | None = None,
    narrator_checkpoint: Path | None = None,
    corpus_path: Path = Path("artifacts/distill/corpus.jsonl"),
    report_out: Path = Path("artifacts/report_head.pt"),
    use_cache: bool = True,
):
    cfg = _load_config(config_path)
    store = IQTObjectiveDataStore(cfg.data.cache_dir)

    if objective_data is None:
        materialized = store.materialize(
            ObjectiveRequest(
                objective="mixed",
                num_sequences=cfg.data.default_num_sequences,
                sequence_length=cfg.data.default_sequence_length,
                feature_dim=cfg.data.feature_dim,
            )
        )
        objective_data = materialized.dataset_path

    world, narrator = _build_world_narrator(cfg)

    if world_checkpoint and world_checkpoint.exists():
        world.load_state_dict(_load_weights(world_checkpoint))
    if narrator_checkpoint and narrator_checkpoint.exists():
        narrator.load_state_dict(_load_weights(narrator_checkpoint))

    if not corpus_path.exists():
        corpus_path.parent.mkdir(parents=True, exist_ok=True)
        build_synthetic_distillation_corpus(objective_data, corpus_path)

    tokenizer = load_tokenizer(cfg.distillation)
    tokenizer_vocab = len(tokenizer)
    if cfg.report_head.vocab_size != tokenizer_vocab:
        typer.echo(
            "Adjusting report-head vocab size to match teacher tokenizer: "
            f"{cfg.report_head.vocab_size} -> {tokenizer_vocab}"
        )

    if use_cache:
        typer.echo("Building/loading code cache...")
        cache_path = build_code_cache(
            corpus_path=corpus_path,
            objective_npz_path=objective_data,
            world_model=world,
            narrator=narrator,
            cache_dir=cfg.distillation.code_cache_dir,
            device=cfg.train.device,
        )
        typer.echo(f"Code cache: {cache_path}")
        dataset = CachedNarratorTextDataset(
            cache_path=cache_path,
            corpus_path=corpus_path,
            tokenizer=tokenizer,
            max_text_length=256,
        )
    else:
        dataset = NarratorTextDataset(
            corpus_path=corpus_path,
            objective_npz_path=objective_data,
            world_model=world,
            narrator=narrator,
            tokenizer=tokenizer,
            device=cfg.train.device,
        )

    report_head = _build_report_head(cfg, vocab_size_override=tokenizer_vocab)
    trainer = DistillationTrainer(report_head, cfg.distillation, device=cfg.train.device)
    result = trainer.train(dataset)

    report_out.parent.mkdir(parents=True, exist_ok=True)
    torch.save(report_head.state_dict(), report_out)
    metadata = report_out.with_suffix(".json")
    metadata.write_text(
        json.dumps(
            {
                "teacher_model": result.teacher_model_name,
                "final_loss": result.final_loss,
                "final_loss_kl": result.final_loss_kl,
                "final_loss_ce": result.final_loss_ce,
                "final_loss_hidden": result.final_loss_hidden,
                "steps": result.steps,
                "objective_data": str(objective_data),
                "corpus": str(corpus_path),
                "hidden_alignment": cfg.distillation.hidden_alignment,
            },
            indent=2,
        )
    )

    typer.echo(
        f"Stage 3 complete. loss={result.final_loss:.4f} teacher={result.teacher_model_name}"
    )
    if cfg.distillation.hidden_alignment:
        typer.echo(f"  KL={result.final_loss_kl:.4f} CE={result.final_loss_ce:.4f} hidden={result.final_loss_hidden:.4f}")
    typer.echo(f"Saved: {report_out}")
    typer.echo(f"Metadata: {metadata}")


@app.command("train-stage4")
def train_stage4(
    config_path: Path = Path("pdv3.yaml"),
    world_checkpoint: Path | None = None,
    narrator_checkpoint: Path | None = None,
    save_dir: Path = Path("artifacts"),
):
    """Stage 4: Embodied grounding via closed-loop gridworld interaction."""
    cfg = _load_config(config_path)
    world, narrator = _build_world_narrator(cfg)

    if world_checkpoint and world_checkpoint.exists():
        world.load_state_dict(_load_weights(world_checkpoint))
    if narrator_checkpoint and narrator_checkpoint.exists():
        narrator.load_state_dict(_load_weights(narrator_checkpoint))

    narrator_dim = cfg.narrator.codes_per_step * cfg.narrator.code_dim
    control_head = ControlHead(
        narrator_dim=narrator_dim,
        action_dim=4,  # gridworld has 4 discrete actions
        hidden_dim=cfg.control_head.hidden_dim,
    )

    trainer = Stage4EmbodiedTrainer(
        world_model=world,
        narrator=narrator,
        control_head=control_head,
        stage4_cfg=cfg.stage4,
        input_dim=cfg.world_model.input_dim,
        learning_rate=cfg.train.learning_rate,
        weight_decay=cfg.train.weight_decay,
        device=cfg.train.device,
    )

    env_config = GridWorldConfig(
        grid_size=cfg.stage4.grid_size,
        max_episode_steps=cfg.stage4.max_episode_steps,
    )

    result = trainer.train(
        max_steps=min(cfg.train.max_steps, 500),
        env_config=env_config,
    )

    save_dir.mkdir(parents=True, exist_ok=True)
    world_out = save_dir / "world_stage4.pt"
    narrator_out = save_dir / "narrator_stage4.pt"
    control_out = save_dir / "control_stage4.pt"
    torch.save(world.state_dict(), world_out)
    torch.save(narrator.state_dict(), narrator_out)
    torch.save(control_head.state_dict(), control_out)

    metadata_path = save_dir / "stage4_result.json"
    metadata_path.write_text(
        json.dumps(
            {
                "final_loss": result.final_loss,
                "mean_episode_reward": result.mean_episode_reward,
                "mean_episode_length": result.mean_episode_length,
                "goal_rate": result.goal_rate,
                "steps": result.steps,
            },
            indent=2,
        )
    )

    typer.echo(
        f"Stage 4 complete. loss={result.final_loss:.4f} "
        f"reward={result.mean_episode_reward:.3f} "
        f"goal_rate={result.goal_rate:.2f} steps={result.steps}"
    )
    typer.echo(f"Saved: {world_out}")
    typer.echo(f"Saved: {narrator_out}")
    typer.echo(f"Saved: {control_out}")
    typer.echo(f"Metadata: {metadata_path}")


@app.command("evaluate")
def evaluate(
    config_path: Path = Path("pdv3.yaml"),
    objective: str = "mixed",
    world_checkpoint: Path | None = None,
):
    cfg = _load_config(config_path)
    store = IQTObjectiveDataStore(cfg.data.cache_dir)
    data = store.materialize(
        ObjectiveRequest(
            objective=objective,  # type: ignore[arg-type]
            num_sequences=128,
            sequence_length=min(cfg.data.default_sequence_length, 128),
            feature_dim=cfg.data.feature_dim,
        )
    )

    dataset = ObjectiveTensorDataset(data.dataset_path)
    batch_count = min(32, len(dataset))
    obs = torch.stack([dataset[i]["observations"] for i in range(batch_count)], dim=0)

    world, _ = _build_world_narrator(cfg)
    if world_checkpoint is not None:
        if not world_checkpoint.exists():
            raise FileNotFoundError(f"World checkpoint not found: {world_checkpoint}")
        world.load_state_dict(_load_weights(world_checkpoint))

    with torch.no_grad():
        world_out = world(obs)
        module_states = list(world.iter_module_views(world_out.states))
        bundle = compute_iqt_bundle(
            world_out.states,
            module_states,
            lags=[1, 2, 4, 8, 16, 32],
        )

    payload = {
        "tau_eff": bundle.tau_eff,
        "unity": bundle.unity,
        "readout_dominance": bundle.readout_dominance,
        "coherence": bundle.coherence,
        "persistence": [
            {
                "lag": p.lag,
                "temporal_mi": p.temporal_mi,
                "effective_dim": p.effective_dim,
                "persistence": p.persistence,
            }
            for p in bundle.persistence
        ],
    }
    typer.echo(json.dumps(payload, indent=2))


def _prepare_eval_obs(cfg: PersistentDiamondsConfig, objective: str = "mixed") -> torch.Tensor:
    """Prepare a small observation batch for protocol evaluation."""
    store = IQTObjectiveDataStore(cfg.data.cache_dir)
    data = store.materialize(
        ObjectiveRequest(
            objective=objective,  # type: ignore[arg-type]
            num_sequences=128,
            sequence_length=min(cfg.data.default_sequence_length, 128),
            feature_dim=cfg.data.feature_dim,
        )
    )
    dataset = ObjectiveTensorDataset(data.dataset_path)
    batch_count = min(32, len(dataset))
    return torch.stack([dataset[i]["observations"] for i in range(batch_count)], dim=0)


@app.command("protocol1")
def protocol1(
    config_path: Path = Path("pdv3.yaml"),
    objective: str = "mixed",
    world_checkpoint: Path | None = None,
    narrator_checkpoint: Path | None = None,
    output_path: Path = Path("artifacts/protocol1.json"),
):
    """Run Protocol 1 analogue: titrated degradation of recurrent gain."""
    cfg = _load_config(config_path)
    obs = _prepare_eval_obs(cfg, objective)

    world, narrator = _build_world_narrator(cfg)
    if world_checkpoint and world_checkpoint.exists():
        world.load_state_dict(_load_weights(world_checkpoint))
    if narrator_checkpoint and narrator_checkpoint.exists():
        narrator.load_state_dict(_load_weights(narrator_checkpoint))

    with torch.no_grad():
        result = run_protocol1(
            world, narrator, obs,
            world_step_hz=cfg.narrator.world_step_hz,
        )

    payload = result_to_dict(result)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(payload, indent=2))
    typer.echo(f"Protocol 1 complete. Fragmentation detected: {result.fragmentation_detected}")
    typer.echo(f"Artifact: {output_path}")


@app.command("protocol2")
def protocol2(
    config_path: Path = Path("pdv3.yaml"),
    objective: str = "mixed",
    world_checkpoint: Path | None = None,
    narrator_checkpoint: Path | None = None,
    output_path: Path = Path("artifacts/protocol2.json"),
):
    """Run Protocol 2 analogue: overlap test with perturbation propagation."""
    cfg = _load_config(config_path)
    obs = _prepare_eval_obs(cfg, objective)

    world, narrator = _build_world_narrator(cfg)
    if world_checkpoint and world_checkpoint.exists():
        world.load_state_dict(_load_weights(world_checkpoint))
    if narrator_checkpoint and narrator_checkpoint.exists():
        narrator.load_state_dict(_load_weights(narrator_checkpoint))

    with torch.no_grad():
        result = run_protocol2(
            world, narrator, obs,
            world_step_hz=cfg.narrator.world_step_hz,
        )

    payload = result_to_dict(result)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(payload, indent=2))
    typer.echo(f"Protocol 2 complete. Dual high persistence: {result.dual_high_persistence}")
    typer.echo(f"O-information: {result.tripartite_o_information:.4f}")
    typer.echo(f"Perturbation containment: {result.perturbation_containment:.4f}")
    typer.echo(f"Artifact: {output_path}")


@app.command("protocol3")
def protocol3(
    config_path: Path = Path("pdv3.yaml"),
    objective: str = "mixed",
    world_checkpoint: Path | None = None,
    narrator_checkpoint: Path | None = None,
    output_path: Path = Path("artifacts/protocol3.json"),
):
    """Run Protocol 3 analogue: timescale manipulation and peak-shift analysis."""
    cfg = _load_config(config_path)
    obs = _prepare_eval_obs(cfg, objective)

    world, narrator = _build_world_narrator(cfg)
    if world_checkpoint and world_checkpoint.exists():
        world.load_state_dict(_load_weights(world_checkpoint))
    if narrator_checkpoint and narrator_checkpoint.exists():
        narrator.load_state_dict(_load_weights(narrator_checkpoint))

    with torch.no_grad():
        result = run_protocol3(
            world, narrator, obs,
            world_step_hz=cfg.narrator.world_step_hz,
        )

    payload = result_to_dict(result)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(payload, indent=2))
    typer.echo(f"Protocol 3 complete. Peak-shift detected: {result.peak_shift_detected}")
    for c in result.conditions:
        typer.echo(f"  {c.condition}: peak_lag={c.peak_lag} auc={c.auc_persistence:.4f}")
    typer.echo(f"Artifact: {output_path}")


if __name__ == "__main__":
    app()
