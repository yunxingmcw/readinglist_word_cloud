"""Simple runner to generate and save two wordcloud images from a Goodreads-style CSV.

Usage:
  python wordcloud_generator.py --input ../your_goodreads_library_export.csv
"""
import argparse
import pandas as pd
from wordcloud import WordCloud
import re


def generate_wordclouds(file_path, title_column='Title', pages_column='Number of Pages', width=1200, height=800, colormap='viridis'):
    df = pd.read_csv(file_path)
    df = df[~df[pages_column].isna()]
    title_weights = dict(zip(df[title_column], df[pages_column]))

    # Use original titles (not underscores) as frequency keys so words render correctly
    freq_titles = {}
    for title, weight in title_weights.items():
        key = str(title).strip()
        freq_titles[key] = weight

    # Try to use a reliable TTF font to ensure words render correctly
    try:
        from matplotlib import font_manager as fm
        font_path = fm.findfont(fm.FontProperties(family='DejaVu Sans'))
    except Exception:
        font_path = None

    wc1 = WordCloud(
        width=width,
        height=height,
        background_color='white',
        max_words=800,
        colormap=colormap,
        font_path=font_path,
        collocations=False,
        prefer_horizontal=1.0,
    ).generate_from_frequencies(freq_titles)

    # Method 2: build a small frequency dict scaled to a reasonable integer range
    max_pages = max(title_weights.values()) if title_weights else 1
    scaled_freq = {}
    for title, pages in title_weights.items():
        repeat_count = max(1, int((pages / max_pages) * 50))
        scaled_freq[str(title).strip()] = repeat_count

    wc2 = WordCloud(
        width=width,
        height=height,
        background_color='white',
        max_words=800,
        colormap=colormap,
        font_path=font_path,
        collocations=False,
        prefer_horizontal=1.0,
    ).generate_from_frequencies(scaled_freq)

    return wc1, wc2


def save_wordcloud(wordcloud, filename, border_px=10, border_color='black'):
    """Save wordcloud to `filename` and add a border using Pillow.

    Args:
        wordcloud: WordCloud object
        filename: output path (PNG)
        border_px: border thickness in pixels (0 to disable)
        border_color: CSS color or hex for border
    """
    # Save to file first
    wordcloud.to_file(filename)

    if border_px and border_px > 0:
        try:
            from PIL import Image
        except Exception:
            print("Pillow not available; install Pillow to add borders")
            print(f"Saved: {filename}")
            return

        img = Image.open(filename)
        w, h = img.size
        new_w = w + 2 * border_px
        new_h = h + 2 * border_px
        new_img = Image.new(img.mode, (new_w, new_h), border_color)
        new_img.paste(img, (border_px, border_px))
        new_img.save(filename)

    print(f"Saved: {filename}")


def main():
    parser = argparse.ArgumentParser(description='Generate wordclouds from Goodreads CSV')
    parser.add_argument('--input', '-i', default='word_cloud/yun_goodreads_library_export.csv', help='Path to CSV file')
    parser.add_argument('--out1', default='word_cloud/book_titles_method1.png', help='Output path for method1 image')
    parser.add_argument('--out2', default='word_cloud/book_titles_method2.png', help='Output path for method2 image')
    parser.add_argument('--border-px', type=int, default=10, help='Border thickness in pixels (0 to disable)')
    parser.add_argument('--border-color', default='black', help='Border color (name or hex)')
    parser.add_argument('--width', type=int, default=1200, help='Image width in pixels')
    parser.add_argument('--height', type=int, default=800, help='Image height in pixels')
    parser.add_argument('--colormap', default='viridis', help='Matplotlib colormap name')
    args = parser.parse_args()

    try:
        wc1, wc2 = generate_wordclouds(args.input, width=args.width, height=args.height, colormap=args.colormap)
        save_wordcloud(wc1, args.out1, border_px=args.border_px, border_color=args.border_color)
        save_wordcloud(wc2, args.out2, border_px=args.border_px, border_color=args.border_color)
    except FileNotFoundError:
        print(f"File '{args.input}' not found. Please check the path.")
    except Exception as e:
        print(f"Error: {e}")


if __name__ == '__main__':
    main()
