import tkinter as tk
from tkinter import filedialog, messagebox
from docx import Document
import nltk, os, re
from collections import Counter
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lex_rank import LexRankSummarizer
from sumy.nlp.stemmers import Stemmer
from sumy.utils import get_stop_words

# === Auto-download NLTK data ===
nltk.data.path.append(os.path.join(os.path.expanduser("~"), "nltk_data"))
for pkg, kind in [("punkt", "tokenizers"), ("stopwords", "corpora")]:
    try:
        nltk.data.find(f"{kind}/{pkg}")
    except LookupError:
        nltk.download(pkg)

# === Simple fallback summarizer ===
def fallback_summary(text, n=5):
    sents = re.split(r'(?<=[.!?]) +', text)
    if not sents: return ""
    words = re.findall(r'\w+', text.lower())
    sw = set(nltk.corpus.stopwords.words("english"))
    freq = Counter(w for w in words if w not in sw)
    scored = [(sum(freq[w] for w in re.findall(r'\w+', s)), i, s) for i, s in enumerate(sents)]
    return "\n".join(s for _, _, s in sorted(sorted(scored, reverse=True)[:n], key=lambda x: x[1]))

# === File Loader ===
def load_file():
    path = filedialog.askopenfilename(filetypes=[("Text", "*.txt"), ("Word", "*.docx")])
    if not path: return
    try:
        if path.endswith(".txt"):
            text = open(path, encoding="utf-8").read()
        else:
            text = "\n".join(p.text for p in Document(path).paragraphs)
        text_input.delete("1.0", tk.END)
        text_input.insert(tk.END, text)
    except Exception as e:
        messagebox.showerror("Error", str(e))

# === Summarizer ===
def summarize():
    raw_text = text_input.get("1.0", tk.END).strip()
    if not raw_text:
        return messagebox.showwarning("No Text", "Enter or load some text first.")
    try:
        parser = PlaintextParser.from_string(raw_text, Tokenizer("english"))
        stemmer = Stemmer("english")
        summarizer = LexRankSummarizer(stemmer)
        summarizer.stop_words = get_stop_words("english")
        summary = "\n".join(str(s) for s in summarizer(parser.document, 5))
    except Exception:
        summary = fallback_summary(raw_text, 5)
    summary_output.delete("1.0", tk.END)
    summary_output.insert(tk.END, summary)

# === GUI ===
root = tk.Tk()
root.title("Text Summarizer")
root.geometry("800x600")

btn_frame = tk.Frame(root); btn_frame.pack(pady=5)
tk.Button(btn_frame, text="Load File", command=load_file).pack(side=tk.LEFT, padx=5)
tk.Button(btn_frame, text="Summarize", command=summarize).pack(side=tk.LEFT, padx=5)

tk.Label(root, text="Input Text").pack()
text_input = tk.Text(root, height=15, wrap=tk.WORD)
text_input.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

tk.Label(root, text="Summary").pack()
summary_output = tk.Text(root, height=10, wrap=tk.WORD, bg="white")
summary_output.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

root.mainloop()
