import pandas as pd
import torch
from transformers import AutoModelForMaskedLM, AutoTokenizer, Trainer, TrainingArguments
from datasets import Dataset, DatasetDict
import numpy as np

def train_job_embed():
    # Load PhoBERT model and tokenizer
    model_name = "vinai/phobert-base-v2"
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForMaskedLM.from_pretrained(model_name)

    # Freeze all layers except the last layer
    for param in model.base_model.parameters():
        param.requires_grad = False
    for param in model.base_model.encoder.layer[
        -1
    ].parameters():  # Fine-tune only the last layer
        param.requires_grad = True

    # Load your dataset from CSV
    df = pd.read_csv("./data/data.csv")  # Ensure the CSV has the specified columns

    # Combine relevant fields into a single text column
    df["text"] = df.apply(
        lambda x: f"{x['title']} {x['description']} {x['salary']} {x['company']} {x['location']}",
        axis=1,
    )

    # Create a Dataset object using the new 'text' column
    dataset = Dataset.from_pandas(df[["text"]])  # Use only the combined text column

    # Function to randomly mask tokens
    def mask_tokens(inputs, mask_probability=0.15):
        labels = inputs.clone()  # Copy the input tensor
        rand = torch.rand(inputs.shape)  # Random tensor
        mask = rand < mask_probability  # Create mask based on probability
        inputs[mask] = tokenizer.mask_token_id
        labels[~mask] = -100  # Ignore non-masked tokens in loss calculation
        return inputs, labels

    # Tokenize the dataset with labels
    def tokenize_function(examples):
        encoding = tokenizer(
            examples["text"],
            padding="max_length",  # Pad sequences to the max length
            truncation=True,  # Truncate sequences that are too long
            max_length=258,  # Maximum length for PhoBERT
        )

        # Convert input IDs and attention masks to tensors
        input_ids = torch.tensor(encoding["input_ids"])  # Convert to tensor
        attention_mask = torch.tensor(encoding["attention_mask"])  # Convert to tensor

        # Mask tokens and create labels
        masked_input_ids, labels = mask_tokens(input_ids.clone())

        return {
            "input_ids": masked_input_ids,
            "attention_mask": attention_mask,
            "labels": labels,
        }

    # Map the tokenization function to the dataset
    tokenized_datasets = dataset.map(tokenize_function, batched=True)

    # Set the format for PyTorch
    tokenized_datasets.set_format(
        "torch", columns=["input_ids", "attention_mask", "labels"]
    )

    # Split the dataset into training and evaluation
    train_test_split = tokenized_datasets.train_test_split(
        test_size=0.1  # 10% for evaluation
    )
    train_dataset = train_test_split["train"]
    eval_dataset = train_test_split["test"]

    # Training arguments
    training_args = TrainingArguments(
        output_dir="./phobert-finetuned",
        save_strategy="epoch",
        evaluation_strategy="epoch",  # Evaluate at the end of each epoch
        learning_rate=5e-5,
        per_device_train_batch_size=16,
        num_train_epochs=10,
        logging_steps=10,  # Adjusted for less frequent logging
        weight_decay=0.01,
        load_best_model_at_end=True,
        no_cuda=False
    )

    # Create a Trainer instance
    trainer = Trainer(
        model=model,
        args=training_args,
        train_dataset=train_dataset,
        eval_dataset=eval_dataset,  # Pass the evaluation dataset
    )

    # Train the model
    trainer.train()

    # Save the fine-tuned model
    trainer.save_model("./phobert-finetuned")
    tokenizer.save_pretrained("./phobert-finetuned")
