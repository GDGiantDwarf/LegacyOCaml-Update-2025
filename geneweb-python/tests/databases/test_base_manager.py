import pytest
from pathlib import Path
from geneweb.core.database import BaseManager

# ------------------------------------------------------
# FIXTURES
# ------------------------------------------------------


@pytest.fixture
def base_dir(tmp_path) -> Path:
    """Crée un dossier temporaire pour les tests."""
    d = tmp_path / "bases"
    d.mkdir()
    return d


# ------------------------------------------------------
# TESTS DE BASES CRUD
# ------------------------------------------------------


def test_create_and_list_and_delete_base(base_dir):
    """Crée, liste, renomme, nettoie et supprime une base."""
    # Dossier vide au départ
    assert BaseManager.list_bases(base_dir) == []

    # Création
    BaseManager.create_base("alpha", base_dir)
    assert "alpha" in BaseManager.list_bases(base_dir)

    # Renommage
    BaseManager.rename_base("alpha", "beta", base_dir)
    bases = BaseManager.list_bases(base_dir)
    assert "beta" in bases
    assert "alpha" not in bases

    # Nettoyage
    BaseManager.cleanup_base("beta", base_dir)
    assert "beta" in BaseManager.list_bases(base_dir)

    # Suppression
    BaseManager.delete_base("beta", base_dir)
    assert BaseManager.list_bases(base_dir) == []


# ------------------------------------------------------
# TESTS D'ERREURS ET VALIDATIONS
# ------------------------------------------------------


def test_create_existing_base_raises(base_dir):
    """Créer deux fois la même base doit lever une erreur."""
    BaseManager.create_base("dup", base_dir)
    with pytest.raises(FileExistsError):
        BaseManager.create_base("dup", base_dir)


def test_delete_nonexistent_base_raises(base_dir):
    """Supprimer une base inexistante doit lever FileNotFoundError."""
    with pytest.raises(FileNotFoundError):
        BaseManager.delete_base("ghost", base_dir)


def test_rename_to_existing_target_raises(base_dir):
    """Renommer vers une base déjà existante doit échouer."""
    BaseManager.create_base("a", base_dir)
    BaseManager.create_base("b", base_dir)
    with pytest.raises(FileExistsError):
        BaseManager.rename_base("a", "b", base_dir)


def test_cleanup_nonexistent_base_raises(base_dir):
    """Nettoyer une base inexistante doit lever FileNotFoundError."""
    with pytest.raises(FileNotFoundError):
        BaseManager.cleanup_base("nothing", base_dir)


def test_invalid_name_rejected(base_dir):
    """Les noms de base invalides doivent être rejetés."""
    with pytest.raises(ValueError):
        BaseManager.create_base("invalid name!", base_dir)
    with pytest.raises(ValueError):
        BaseManager.create_base("a" * 100, base_dir)
