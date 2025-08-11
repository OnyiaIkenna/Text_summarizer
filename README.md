Text Summarizer App

Just a small Python project I made to practice Tkinter and work with text summarization.

It's a desktop app where you can load a .txt or .docx file and it will give you a short summary of the content.

What it does:

- Lets you load text files or Word docs
- Summarizes the text into a few sentences
- Shows the result right inside the app

How I built it:

I used Tkinter for the interface (just buttons, labels, and text boxes)

I used NLTK to:

Split text into sentences (tokenizer)

Remove common words (stopwords) so they don't affect the summary

Sumy library for the main summarizing part (LexRank algorithm).

If Sumy fails for any reason, I made a quick fallback summarizer using word frequency

Why NLTK?
Because without it the app wouldn’t know how to break text into proper sentences or ignore filler words.
Basically, it helps the summarizer focus on important stuff instead of random words like "and", "the", "is" type of words.

pip install -r requirements.txt

