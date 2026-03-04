from geneweb.cli.parser_gwsetup import GenewebSetupCLI


def test_default_port():
    cli = GenewebSetupCLI()
    args = cli.parser.parse_args([])
    assert args.port == 2316


def test_custom_port():
    cli = GenewebSetupCLI()
    args = cli.parser.parse_args(
        ["-p", "9090"]
    )
    assert args.port == 9090


def test_default_lang():
    cli = GenewebSetupCLI()
    args = cli.parser.parse_args([])
    assert args.lang == "fr"
