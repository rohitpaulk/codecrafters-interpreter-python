import sys

from app.ast_printer import AstPrinter

from .parser import ParseError, Parser
from .scanner import Scanner


def main():
    if len(sys.argv) < 3:
        print("Usage: ./your_program.sh tokenize <filename>", file=sys.stderr)
        exit(1)

    command = sys.argv[1]
    filename = sys.argv[2]

    match command:
        case "tokenize":
            with open(filename) as file:
                file_contents = file.read()

            scanner = Scanner(file_contents)
            tokens = scanner.scan_tokens()

            for token in tokens:
                print(token)

            exit(65 if scanner.has_errors else 0)
        case "parse":
            with open(filename) as file:
                file_contents = file.read()

            scanner = Scanner(file_contents)
            tokens = scanner.scan_tokens()
            parser = Parser(tokens)
            expression = parser.parse()
            print(AstPrinter().print(expression))

            if parser.has_errors:
                exit(65)
        case _:
            print(f"Unknown command: {command}", file=sys.stderr)
            exit(1)


if __name__ == "__main__":
    main()
