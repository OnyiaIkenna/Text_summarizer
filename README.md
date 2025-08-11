Text Summarizer (Tkinter + NLTK + Sumy)
This is a small Python GUI app I built to practice Tkinter and work with text summarization.

It lets you:

Load a .txt or .docx file

Summarize the content into a shorter version

Read the summary right inside the app

How It Works

The GUI is made with Tkinter (Python's built-in UI library).

I used NLTK (Natural Language Toolkit) for:

Breaking text into sentences (punkt tokenizer)

Removing common words (stopwords) so they don't affect scoring

For summarizing, I used Sumy’s LexRank algorithm.

If Sumy fails (e.g., missing resources or parsing issues), the app falls back to a simple frequency-based summarizer I coded.

Why NLTK?
NLTK is a Python library for natural language processing. In this project, I use it because:

The summarizer needs to tokenize text (split it into sentences and words).

I also need to remove stopwords (common words like "the", "and", "is") so the summary focuses on important words.

It's lightweight and works well with Sumy.
