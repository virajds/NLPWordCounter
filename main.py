from wordCounter import count_words

def parse_arguments():
    """Parse arguments for cmd line application."""
    import argparse
    parser = argparse.ArgumentParser(
        description="""Main entry point for command line app to count words \n
        in a paragraph given by a parameter of text files located in a Dir \n
        which also the path passed by a parameter.""")
    parser.add_argument('--path', type=str,
                        help='Path for the text files. (Must be with .txt \
                         file extension.')
    parser.add_argument('--words', type=str,
                        help='List of word specially should look for.')
    parser.add_argument('--paragraph', type=str,
                        help='Paragraph to pass as a variable.')
    return parser.parse_args()

def main(path=None, words=None, paragraph=None):
    """Main entry point for count words command line app.

    path :: Full path to the text file Dir ("String" - Unix format file path)

    words :: List of word specially should look for ("String" - Comma separated word list).
    Will count everything other than stop words, if not passed

    paragraph :: Paragraph to pass as a variable. Will use the file Dir if not passed.
    """
    count_words(path, words, paragraph)

if __name__ == '__main__':
    args = parse_arguments()
    main(path=args.path,
         words=args.words,
         paragraph=args.paragraph)