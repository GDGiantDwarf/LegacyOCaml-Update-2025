# geneweb/__main__.py
from geneweb.cli.parser_gwsetup import GenewebSetupCLI


def main():
    cli = GenewebSetupCLI()
    cli.run()


if __name__ == "__main__":
    main()
