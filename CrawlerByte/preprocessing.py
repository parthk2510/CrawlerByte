import nltk
from nltk.tokenize import sent_tokenize, word_tokenize, WordPunctTokenizer
from nltk.stem import WordNetLemmatizer


def preprocess_text(input_text):
    with open("tokenized_output.txt", "r") as file:
        input_text2 = file.read()
    # Lower casing the input text
    input_text = input_text2.lower()

    # Sentence Tokenization
    sentences = sent_tokenize(input_text2)

    # Word Tokenization
    words = word_tokenize(input_text2)

    # WordPunct Tokenization
    word_punct_tokens = WordPunctTokenizer().tokenize(input_text2)

    # Lemmatization
    lemmatizer = WordNetLemmatizer()
    words_lemmatized = [lemmatizer.lemmatize(word) for word in words]

    sentences, words, word_punct_tokens, words_lemmatized = preprocess_text(input_text2)

    # Save preprocessed data to a new file
    with open("preprocessed_output.txt", "w") as file:
        file.write("Sentences:\n")
        file.write("\n".join(sentences))
        file.write("\n\n")

        file.write("Words:\n")
        file.write(" ".join(words))
        file.write("\n\n")

        file.write("WordPunct Tokens:\n")
        file.write(" ".join(word_punct_tokens))
        file.write("\n\n")

        file.write("Words Lemmatized:\n")
        file.write(" ".join(words_lemmatized))
        file.write("\n")

    print("Preprocessed data saved to 'preprocessed_output.txt'")

    return sentences, words, word_punct_tokens, words_lemmatized
