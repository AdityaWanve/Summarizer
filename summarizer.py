from transformers import pipeline

# Load summarization model (English BART)
summarizer_en = pipeline("summarization", model="facebook/bart-large-cnn")

# Load MarianMT translation models
from transformers import MarianMTModel, MarianTokenizer

model_name_hi = "Helsinki-NLP/opus-mt-en-hi"
model_name_mr = "Helsinki-NLP/opus-mt-en-mr"

tokenizer_hi = MarianTokenizer.from_pretrained(model_name_hi)
model_hi = MarianMTModel.from_pretrained(model_name_hi)

tokenizer_mr = MarianTokenizer.from_pretrained(model_name_mr)
model_mr = MarianMTModel.from_pretrained(model_name_mr)

def translate(text, lang):
    if lang == "hi":
        tokenizer, model = tokenizer_hi, model_hi
    elif lang == "mr":
        tokenizer, model = tokenizer_mr, model_mr
    else:
        return text  # English or unsupported

    batch = tokenizer.prepare_seq2seq_batch([text], return_tensors="pt")
    translated = model.generate(**batch)
    tgt_text = tokenizer.batch_decode(translated, skip_special_tokens=True)[0]
    return tgt_text

def generate_summary(text, lang="en"):
    # Summarize in English first
    summary_obj = summarizer_en(text, max_length=150, min_length=30, do_sample=False)
    summary_en = summary_obj[0]["summary_text"]

    if lang in ["hi", "mr"]:
        # Translate summary to Hindi or Marathi
        summary_translated = translate(summary_en, lang)
        return summary_translated
    else:
        return summary_en
