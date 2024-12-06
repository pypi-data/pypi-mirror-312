# Felafax CLI

A command-line interface for fine-tuning and managing large language models.

## Installation

```bash
pip install felafax-cli
```

## Quick Start

1. Login with your authentication token:
```bash
felafax-cli auth login --token <your-token>
```

2. Initialize a fine-tuning configuration:
```bash
felafax-cli tune init-config
```

3. Upload your training data:
```bash
felafax-cli files upload path/to/data.jsonl
```

4. Start fine-tuning:
```bash
felafax-cli tune start --model <model_name> --config config.yml --dataset <dataset_id>
```

## Available Commands

### Authentication
```bash
# Login with your token
felafax-cli auth login --token <your-token> [--force]
```

### Model Management
```bash
# List available fine-tuned models
felafax-cli model list

# Start an interactive chat session with a model
felafax-cli model chat <model_id> [--system-prompt "Your custom prompt"]

# Get detailed information about a model
felafax-cli model info <model_id>

# Delete a fine-tuned model
felafax-cli model delete <model_id>
```

### Training Management
```bash
# Initialize a new config file
felafax-cli tune init-config

# Start a new fine-tuning job
felafax-cli tune start \
    --model <model_name> \
    --config path/to/config.yml \
    --dataset <dataset_id>

# List all training jobs
felafax-cli tune list

# Check job status
felafax-cli tune status --job-id <id>

# Stop a running job
felafax-cli tune stop --job-id <id>
```

### File Management
```bash
# List files in storage
felafax-cli files list [--prefix <prefix>] [--limit <number>]

# Upload training data
felafax-cli files upload <file_path>

# Delete a file
felafax-cli files delete <file_path>
```

## Configuration Example

When you run `felafax-cli tune init-config`, it creates a YAML file with the following structure:

```yaml
hyperparameters:
  learning_rate: 1.0e-05
  batch_size: 32
  n_epochs: 4
  warmup_ratio: 0.0
lora:
  enabled: false
  r: 8
  alpha: 8
  dropout: 0.0
```

## Support

For more information, visit our documentation at https://docs.felafax.ai

## License

MIT License