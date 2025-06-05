

# Import the string module (contains punctuation, letters, etc.)
import string

# Paragraph to clean

paragraph = input("Enter a paragraph:\n")

# paragraph = "Hello, world! This is a test."

# Remove punctuation and convert to lowercase
cleaned_paragraph = ''.join([ch for ch in paragraph.lower() if ch not in string.punctuation])


print("Cleaned Paragraph")
print(cleaned_paragraph)



# Split cleaned text into words
words = cleaned_paragraph.split()



# Count Frequencies using Dictionary

word_freq = {}

for word in words:
    if word in word_freq:
        word_freq[word] += 1
    else:
        word_freq[word] = 1



# Print the result
print(words)


print("\nWord Frequencies:\n")
for word, freq in word_freq.items():
    print(f"{word}: {freq}")


# (Optional) Cell 5: Sort by Frequency


print("\nWords sorted by frequency (descending):\n")
# sorted_words = sorted(word_freq.items(), key=lambda x: x[1], reverse=True)


sorted_words = sorted(
    word_freq.items(),      # Get (word, count) tuples
    key=lambda x: x[1],     # Sort by count (2nd item)
    reverse=True            # High to low
)

for word, freq in sorted_words:
    print(f"{word}: {freq}")


