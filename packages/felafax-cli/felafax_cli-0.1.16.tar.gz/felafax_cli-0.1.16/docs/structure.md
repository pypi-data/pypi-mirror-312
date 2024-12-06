# Structure

```
storage/
├── __init__.py
├── base.py              # Base storage classes and interfaces
├── client.py            # GCS client wrapper
├── models/             # Storage models and schemas
│   ├── __init__.py
│   ├── user.py         # User storage models
│   ├── job.py          # Job storage models
│   ├── dataset.py      # Dataset storage models
│   ├── model.py        # ML model storage models
│   └── billing.py      # Billing storage models
├── handlers/           # Storage operation handlers
│   ├── __init__.py
│   ├── user.py         # User data operations
│   ├── job.py          # Job data operations
│   ├── dataset.py      # Dataset operations
│   ├── model.py        # ML model operations
│   └── billing.py      # Billing data operations
└── utils/             # Utility functions
    ├── __init__.py
    ├── paths.py       # Path generation utilities
    └── validation.py  # Data validation utilities
```

```
felafax-training/
├── pyproject.toml
├── README.md
├── .env.example
├── src/
│ ├── cli/
│ │ ├── __init__.py
│ │ ├── commands/
│ │ │ ├── __init__.py
│ │ │ ├── train.py # Training command implementation
│ │ │ └── serve.py # Serving command implementation
│ │ └── main.py # CLI entry point using click/typer
│ ├── server/
│ │ ├── __init__.py
│ │ ├── api/
│ │ │ ├── __init__.py
│ │ │ ├── routes/
│ │ │ │ ├── __init__.py
│ │ │ │ ├── training.py
│ │ │ │ └── serving.py
│ │ │ └── models/ # Pydantic models for API
│ │ └── main.py # FastAPI application
│ └── core/
│ ├── __init__.py
│ ├── config.py # Shared configuration
│ ├── training/
│ │ ├── __init__.py
│ │ ├── trainer.py # Main training orchestrator
│ │ └── types.py # Training-related type definitions
│ ├── accelerator/
│ │ ├── __init__.py
│ │ ├── base.py # Base accelerator interface
│ │ ├── tpu.py # TPU implementation
│ │ └── gpu.py # Future GPU implementation
│ └── storage/
│ ├── __init__.py
│ ├── base.py # Base storage interface
│ ├── gcs.py # Google Cloud Storage implementation
│ └── s3.py # AWS S3 implementation
```

```py
# CLI
trainer = TrainingJob(
config=TrainingConfig.from_yaml("config.yaml"),
accelerator=TPUProvider(tpu_config),
storage=GCSStorageProvider(gcs_config)
)
await trainer.run()


# API
@router.post("/train")
async def start_training(config: TrainingConfig):
trainer = TrainingJob(
config=config,
accelerator=get_accelerator(),
storage=get_storage()
) # Start training in background task
background_tasks.add_task(trainer.run)
return {"status": "started"}

```

```yaml
model_name: "your-model"
training_data: "gs://your-bucket/data"
hyperparameters:
  learning_rate: 1e-5
  batch_size: 32
output_dir: "gs://your-bucket/output"
```
