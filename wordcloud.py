from wordcloud import WordCloud
import matplotlib.pyplot as plt
import random

def generate_cyan_wordcloud(words, center_word="AKSHAYA", output_file="wordcloud.png"):
    """
    Generate a colorful cyan-toned word cloud with a prominent center word.
    
    Parameters:
        words (list[str]): list of words to include in the word cloud
        center_word (str): word to emphasize and place centrally
        output_file (str): file name to save the resulting image
    """

    # Ensure the center word is the most prominent one
    text = " ".join(words + [center_word] * 20)

    # Cyan-range color function
    def cyan_color_func(word, font_size, position, orientation, random_state=None, **kwargs):
        # Slightly varied cyan tones
        h = random.randint(170, 190)     # cyan-blue hue range
        s = random.randint(80, 100)      # high saturation
        l = random.randint(40, 70)       # mid-lightness
        return f"hsl({h}, {s}%, {l}%)"

    wc = WordCloud(
        width=1200,
        height=800,
        background_color="white",
        color_func=cyan_color_func,
        collocations=False,
        prefer_horizontal=1.0,
        font_path=None  # You can set to a custom font file path if needed
    )

    wc.generate(text)

    # Save and show
    wc.to_file(output_file)
    plt.imshow(wc, interpolation="bilinear")
    plt.axis("off")
    # plt.title(f"Word Cloud with Center Word: {center_word}", fontsize=16)
    plt.show()

# Example usage
if __name__ == "__main__":
    words = [
        "Kokoh", "kuat", "perkasa", "bandel", "keras", "kukuh", "solid", "tegar", "tabah",
        "sabar", "pantang", "menyerah", "ulet", "gigih", "tekun", "rajin", "bersemangat",
        "tangguh", "berani", "mantap", "tegas", "percaya", "diri", "tahan", "banting", "resilien"
    ]

    generate_cyan_wordcloud(words, center_word="AKSHAYA")
