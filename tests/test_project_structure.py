"""Testes de organização do repositório.

Estes testes garantem as regras do projeto:

1. Todo arquivo Python em bot/ tem uma explicação em education/code-explanation/.
2. Os arquivos importantes do repositório existem e não estão vazios.
3. Nenhum token do Discord foi escrito por engano nos arquivos.
4. Os links relativos entre arquivos Markdown apontam para arquivos que existem.
5. Os exemplos de Python básico executam sem erro.
"""

import os
import re
import subprocess
import sys
from pathlib import Path

import pytest

PROJECT_ROOT = Path(__file__).resolve().parent.parent
BOT_DIR = PROJECT_ROOT / "bot"
CODE_DOCS_DIR = PROJECT_ROOT / "education" / "code-explanation"
IGNORED_DIRS = {".venv", "venv", ".git", "__pycache__", ".pytest_cache", "node_modules"}

REQUIRED_FILES = [
    "README.md",
    "LICENSE",
    "CONTRIBUTING.md",
    "CODE_OF_CONDUCT.md",
    "SECURITY.md",
    "CHANGELOG.md",
    "ROADMAP.md",
    ".env.example",
    ".gitignore",
    "requirements.txt",
    "requirements-dev.txt",
    "resources/youtube-playlists.md",
    "resources/official-documentation.md",
    "resources/useful-websites.md",
    "resources/glossary.md",
]

# Formato aproximado de um token de bot do Discord: três partes separadas por pontos.
TOKEN_PATTERN = re.compile(r"[MNO][A-Za-z\d_-]{23,27}\.[A-Za-z\d_-]{6}\.[A-Za-z\d_-]{27,40}")
MARKDOWN_LINK_PATTERN = re.compile(r"\]\(([^)\s]+)\)")


def project_files(pattern: str) -> list[Path]:
    """Arquivos do projeto, ignorando ambiente virtual, cache e .git."""
    return [
        path
        for path in PROJECT_ROOT.rglob(pattern)
        if path.is_file() and not IGNORED_DIRS.intersection(path.relative_to(PROJECT_ROOT).parts)
    ]


def bot_python_files() -> list[Path]:
    return sorted(path for path in BOT_DIR.rglob("*.py") if path.name != "__init__.py" and "__pycache__" not in path.parts)


@pytest.mark.parametrize("python_file", bot_python_files(), ids=lambda path: str(path.relative_to(BOT_DIR)))
def test_every_python_file_has_documentation(python_file: Path):
    relative = python_file.relative_to(BOT_DIR).with_suffix(".md")
    doc = CODE_DOCS_DIR / relative
    assert doc.is_file(), f"Crie a explicação {doc.relative_to(PROJECT_ROOT)} para {python_file.relative_to(PROJECT_ROOT)}"
    assert len(doc.read_text(encoding="utf-8")) > 1500, f"A explicação {doc.name} parece incompleta"


def test_documentation_has_no_orphan_files():
    """Todo .md de code-explanation (exceto os gerais) corresponde a um arquivo Python real."""
    general_pages = {"README.md", "pacotes-e-init.md"}
    for doc in CODE_DOCS_DIR.rglob("*.md"):
        if doc.name in general_pages:
            continue
        source = BOT_DIR / doc.relative_to(CODE_DOCS_DIR).with_suffix(".py")
        assert source.is_file(), f"{doc.relative_to(PROJECT_ROOT)} explica um arquivo que não existe"


def test_every_package_has_init():
    for folder in BOT_DIR.rglob("*"):
        if folder.is_dir() and folder.name not in IGNORED_DIRS and folder.name != "data" and any(folder.glob("*.py")):
            assert (folder / "__init__.py").is_file(), f"Falta __init__.py em {folder.relative_to(PROJECT_ROOT)}"


@pytest.mark.parametrize("relative_path", REQUIRED_FILES)
def test_required_files_exist_and_are_not_empty(relative_path: str):
    path = PROJECT_ROOT / relative_path
    assert path.is_file(), f"Arquivo obrigatório ausente: {relative_path}"
    assert path.stat().st_size > 100, f"Arquivo muito curto: {relative_path}"


def test_no_discord_tokens_in_repository():
    for path in project_files("*"):
        if path.name == ".env" or path.suffix in {".db", ".pyc", ".png", ".jpg", ".ico"}:
            continue
        text = path.read_text(encoding="utf-8", errors="ignore")
        assert not TOKEN_PATTERN.search(text), f"Possível token do Discord em {path.relative_to(PROJECT_ROOT)}"


def test_env_example_has_placeholder_only():
    text = (PROJECT_ROOT / ".env.example").read_text(encoding="utf-8")
    assert "DISCORD_TOKEN=cole_seu_token_aqui" in text


def test_gitignore_protects_secrets():
    text = (PROJECT_ROOT / ".gitignore").read_text(encoding="utf-8")
    for entry in (".env", ".venv/", "data/*.db", "logs/"):
        assert entry in text


def test_requirements_are_pinned():
    for line in (PROJECT_ROOT / "requirements.txt").read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if line and not line.startswith("#"):
            assert "==" in line, f"Fixe a versão da dependência: {line}"


def test_relative_markdown_links_point_to_existing_files():
    broken = []
    for markdown in project_files("*.md"):
        for target in MARKDOWN_LINK_PATTERN.findall(markdown.read_text(encoding="utf-8")):
            if target.startswith(("http://", "https://", "mailto:", "#")):
                continue
            path_part = target.split("#", 1)[0]
            if not (markdown.parent / path_part).resolve().exists():
                broken.append(f"{markdown.relative_to(PROJECT_ROOT)} -> {target}")
    assert not broken, "Links quebrados:\n" + "\n".join(broken)


@pytest.mark.parametrize(
    "script",
    sorted((PROJECT_ROOT / "examples" / "python-basics").glob("*.py")),
    ids=lambda path: path.name,
)
def test_python_basics_examples_run(script: Path):
    # PYTHONUTF8=1 garante que emojis e acentos funcionem mesmo no terminal do Windows.
    env = {**os.environ, "PYTHONUTF8": "1"}
    result = subprocess.run(
        [sys.executable, str(script)],
        capture_output=True,
        text=True,
        encoding="utf-8",
        timeout=30,
        cwd=PROJECT_ROOT,
        env=env,
    )
    assert result.returncode == 0, result.stderr
