import os

def read_conll(file_path):
    sentences, labels = [], []
    sentence, label = [], []
    
    with open(file_path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:  # ngắt câu
                if sentence:
                    sentences.append(sentence)
                    labels.append(label)
                    sentence, label = [], []
                continue
            token, tag = line.split(" ")
            sentence.append(token)
            label.append(tag)
    
    # thêm câu cuối
    if sentence:
        sentences.append(sentence)
        labels.append(label)
    return sentences, labels

train_sentences, train_labels = read_conll("/home/lychien/Desktop/test/CD_4_DM_4_4_NER.txt")
print(train_sentences[0])
print(train_labels[0])

unique_labels = sorted(set(tag for doc in train_labels for tag in doc))
label2id = {label: i for i, label in enumerate(unique_labels)}
id2label = {i: label for label, i in label2id.items()}
print(label2id)

from transformers import AutoTokenizer

model_checkpoint = "vinai/phobert-base"
tokenizer = AutoTokenizer.from_pretrained(model_checkpoint, use_fast=False)
from datasets import Dataset

train_data = Dataset.from_dict({"tokens": train_sentences, "ner_tags": train_labels})

def tokenize_and_align_labels(examples):
    tokenized_inputs = tokenizer(examples["tokens"], is_split_into_words=True, truncation=True, padding="max_length", max_length=128)
    
    labels = []
    for i, label in enumerate(examples["ner_tags"]):
        word_ids = tokenized_inputs.word_ids(batch_index=i)
        previous_word_idx = None
        label_ids = []
        for word_idx in word_ids:
            if word_idx is None:
                label_ids.append(-100)
            else:
                label_ids.append(label2id[label[word_idx]])
        labels.append(label_ids)
    tokenized_inputs["labels"] = labels
    return tokenized_inputs

tokenized_train = train_data.map(tokenize_and_align_labels, batched=True)

from transformers import AutoModelForTokenClassification, TrainingArguments, Trainer
import evaluate

model = AutoModelForTokenClassification.from_pretrained(model_checkpoint, num_labels=len(label2id), id2label=id2label, label2id=label2id)

args = TrainingArguments(
    output_dir="./ner-legal",
    evaluation_strategy="epoch",
    save_strategy="epoch",
    learning_rate=2e-5,
    per_device_train_batch_size=16,
    num_train_epochs=5,
    weight_decay=0.01,
    logging_dir="./logs",
)

metric = evaluate.load("seqeval")

def compute_metrics(eval_preds):
    logits, labels = eval_preds
    predictions = logits.argmax(-1)
    
    true_labels = [[id2label[l] for l in label if l != -100] for label in labels]
    true_preds = [[id2label[p] for (p, l) in zip(pred, label) if l != -100] for pred, label in zip(predictions, labels)]
    
    results = metric.compute(predictions=true_preds, references=true_labels)
    return results

trainer = Trainer(
    model=model,
    args=args,
    train_dataset=tokenized_train,
    eval_dataset=tokenized_train,  # Nếu chưa có tập valid thì tạm dùng train
    tokenizer=tokenizer,
    compute_metrics=compute_metrics,
)

trainer.train()

example = "Điều 1 Luật số 65/2006/QH11 có hiệu lực"
tokens = tokenizer(example.split(), return_tensors="pt", is_split_into_words=True)
outputs = model(**tokens).logits
preds = outputs.argmax(-1).squeeze().tolist()

for token, pred in zip(example.split(), preds[1:len(example.split())+1]):  # bỏ [CLS], [SEP]
    print(token, id2label[pred])
