import pytest

def test_main_calls_run(mocker):
    mock_cli = mocker.Mock()
    mocker.patch("geneweb.gwsetup.GenewebSetupCLI", return_value=mock_cli)

    from geneweb.gwsetup import main
    main()

    mock_cli.run.assert_called_once()
