import tkinter as tk
from tkinter import filedialog, messagebox
import os, re, sys
from collections import Counter

# External libraries
import nltk
from docx import Document
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lex_rank import LexRankSummarizer
from sumy.nlp.stemmers import Stemmer
from sumy.utils import get_stop_words


# ========= NLTK Data Setup =========
NLTK_DATA_DIR = os.path.join(os.path.expanduser("~"), "nltk_data")
if NLTK_DATA_DIR not in nltk.data.path:
    nltk.data.path.append(NLTK_DATA_DIR)
os.makedirs(NLTK_DATA_DIR, exist_ok=True)

def ensure_nltk_resource(name, kind="tokenizers"):
    """Ensure NLTK resource is available, download if missing."""
    try:
        if kind == "tokenizers":
            nltk.data.find(f"tokenizers/{name}")
        else:
            nltk.data.find(f"corpora/{name}")
        return True
    except LookupError:
        print(f"Downloading NLTK resource: {name}...")
        nltk.download(name, download_dir=NLTK_DATA_DIR, quiet=False)
        try:
            if kind == "tokenizers":
                nltk.data.find(f"tokenizers/{name}")
            else:
                nltk.data.find(f"corpora/{name}")
            return True
        except LookupError:
            return False


# ========= Fallback Summarizer =========
def simple_fallback_summary(text, n_sent=5):
    """Basic frequency-based extractive summarizer."""
    sents = re.split(r'(?<=[\.\?\!])\s+', text.strip())
    if not sents:
        return ""
    words = re.findall(r'\w+', text.lower())
    try:
        sw = set(nltk.corpus.stopwords.words("english"))
    except Exception:
        sw = set()
    freq = Counter(w for w in words if w not in sw)
    scored = []
    for i, s in enumerate(sents):
        score = sum(freq[w.lower()] for w in re.findall(r'\w+', s) if w.lower() in freq)
        scored.append((score, i, s))
    top = sorted(scored, key=lambda x: (-x[0], x[1]))[:n_sent]
    top_sorted = sorted(top, key=lambda x: x[1])
    return "\n".join(s for _, _, s in top_sorted)


# ========= File Loader =========
def load_file():
    file_path = filedialog.askopenfilename(
        filetypes=[("Text files", "*.txt"), ("Word Documents", "*.docx")]
    )
    if not file_path:
        return

    try:
        if file_path.lower().endswith(".txt"):
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()
        elif file_path.lower().endswith(".docx"):
            doc = Document(file_path)
            content = "\n".join([p.text for p in doc.paragraphs])
        else:
            messagebox.showerror("Error", "Unsupported file type.")
            return

        text_input.delete("1.0", tk.END)
        text_input.insert(tk.END, content)

    except Exception as e:
        messagebox.showerror("Error", f"Could not load file:\n{e}")


# ========= Summarizer =========
def summarize_text():
    try:
        raw_text = text_input.get("1.0", tk.END).strip()
        if not raw_text:
            messagebox.showwarning("No Text", "Please enter or load some text.")
            return

        # Ensure required NLTK data
        ensure_nltk_resource("punkt", kind="tokenizers")
        ensure_nltk_resource("stopwords", kind="corpora")

        try:
            parser = PlaintextParser.from_string(raw_text, Tokenizer("english"))
            stemmer = Stemmer("english")
            summarizer = LexRankSummarizer(stemmer)
            summarizer.stop_words = get_stop_words("english")
            summary_sentences = list(summarizer(parser.document, 5))

            if not summary_sentences:
                summary_text = simple_fallback_summary(raw_text, n_sent=5)
            else:
                summary_text = "\n".join(str(s).strip() for s in summary_sentences)

        except Exception as e:
            print(f"Sumy error: {e}", file=sys.stderr)
            summary_text = simple_fallback_summary(raw_text, n_sent=5)

        # Output the summary
        summary_output.delete("1.0", tk.END)
        summary_output.insert(tk.END, summary_text)

    except Exception as e:
        messagebox.showerror("Error", f"Unexpected error:\n{e}")


# ========= Tkinter GUI =========
root = tk.Tk()
root.title("Text Summarizer")
root.geometry("800x600")

# Buttons
btn_frame = tk.Frame(root)
btn_frame.pack(pady=5)

tk.Button(btn_frame, text="Load File", command=load_file).pack(side=tk.LEFT, padx=5)
tk.Button(btn_frame, text="Summarize", command=summarize_text).pack(side=tk.LEFT, padx=5)

# Input Text Box
tk.Label(root, text="Input Text").pack()
text_input = tk.Text(root, height=15, wrap=tk.WORD)
text_input.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

# Output Text Box
tk.Label(root, text="Summary").pack()
summary_output = tk.Text(root, height=10, wrap=tk.WORD, bg="white")
summary_output.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

root.mainloop()
