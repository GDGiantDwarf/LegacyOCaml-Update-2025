import pytest
from unittest.mock import patch
import geneweb.gwd

def test_main_calls_run(mocker):
    mock_cli = mocker.Mock()
    mocker.patch("geneweb.gwd.GenewebCLI", return_value=mock_cli)

    from geneweb.gwd import main
    main()

    mock_cli.run.assert_called_once()
