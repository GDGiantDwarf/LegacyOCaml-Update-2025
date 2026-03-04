from geneweb.cli.parser_gwd import GenewebCLI


def test_default_port():
    cli = GenewebCLI()
    args = cli.parser.parse_args([])
    assert args.port == 2317


def test_custom_port():
    cli = GenewebCLI()
    args = cli.parser.parse_args(["-p", "8080"])
    assert args.port == 8080


def test_default_lang():
    cli = GenewebCLI()
    args = cli.parser.parse_args([])
    assert args.lang == "en"


def test_custom_lang():
    cli = GenewebCLI()
    args = cli.parser.parse_args(["-lang", "fr"])
    assert args.lang == "fr"


def test_debug():
    cli = GenewebCLI()
    args = cli.parser.parse_args(["-debug"])
    assert args.debug is True


def test_version_flag():
    cli = GenewebCLI()
    args = cli.parser.parse_args(["-version"])
    assert args.version is True
