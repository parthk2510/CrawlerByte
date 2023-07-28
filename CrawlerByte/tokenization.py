from nltk.tokenize import sent_tokenize, word_tokenize, WordPunctTokenizer


def tokenize_text(input_text):
    # Sentence Tokenization
    sentences = sent_tokenize(input_text)

    # Word Tokenization
    words = word_tokenize(input_text)

    # WordPunct Tokenization
    word_punct_tokens = WordPunctTokenizer().tokenize(input_text)

    return sentences, words, word_punct_tokens


if __name__ == "__main__":
    input_text = """
    The Process of breaking the given text, into the smaller units called tokens, is called tokenization.
    These tokens can be the words, numbers or punctuation marks.
    It is also called word segmentation.
    NLTK module provides different packages for tokenization.
    """

    sentences, words, word_punct_tokens = tokenize_text(input_text)

    # Save tokenized data to a new file
    with open("tokenized_output.txt", "w") as file:
        file.write("Sentences:\n")
        file.write("\n".join(sentences))
        file.write("\n\n")

        file.write("Words:\n")
        file.write(" ".join(words))
        file.write("\n\n")

        file.write("WordPunct Tokens:\n")
        file.write(" ".join(word_punct_tokens))
        file.write("\n")

    print("Tokenized data saved to 'tokenized_output.txt'")
