from pathlib import Path

from scripts.check_public_safety import candidate_files, scan_repository


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def categories_for(root: Path) -> set[str]:
    return {finding.category for finding in scan_repository(root).findings}


def test_detects_macos_home_path(tmp_path: Path) -> None:
    write_text(tmp_path / "sample.txt", "/" + "Users" + "/example-user/project")

    assert "macos_home_path" in categories_for(tmp_path)


def test_detects_linux_home_path(tmp_path: Path) -> None:
    write_text(tmp_path / "sample.txt", "/" + "home" + "/sample-user/project")

    assert "linux_home_path" in categories_for(tmp_path)


def test_detects_windows_home_path(tmp_path: Path) -> None:
    write_text(tmp_path / "sample.txt", "C:" + "\\Users\\sample-user\\project")

    assert "windows_home_path" in categories_for(tmp_path)


def test_detects_private_key_header(tmp_path: Path) -> None:
    header = "-----BEGIN " + "OPENSSH PRIVATE KEY-----"
    write_text(tmp_path / "sample.txt", header)

    assert "private_key" in categories_for(tmp_path)


def test_detects_github_pat_like_value(tmp_path: Path) -> None:
    token = "gh" + "p_" + ("A" * 36)
    write_text(tmp_path / "sample.txt", token)

    assert "github_token" in categories_for(tmp_path)


def test_relative_paths_are_not_findings(tmp_path: Path) -> None:
    write_text(tmp_path / "sample.txt", "docs/product_spec.md\nsrc/light_cylinder/app.py")

    assert not scan_repository(tmp_path).findings


def test_path_file_resolve_is_not_a_finding(tmp_path: Path) -> None:
    write_text(tmp_path / "sample.py", "Path(__file__).resolve().parents[1]")

    assert not scan_repository(tmp_path).findings


def test_findings_mask_values(tmp_path: Path) -> None:
    raw = "/" + "Users" + "/example-user/project"
    write_text(tmp_path / "sample.txt", raw)

    findings = scan_repository(tmp_path).findings

    assert findings
    assert raw not in {finding.preview for finding in findings}


def test_excluded_directories_are_not_scanned(tmp_path: Path) -> None:
    write_text(tmp_path / ".venv" / "sample.txt", "/" + "Users" + "/example-user/project")
    write_text(tmp_path / "__pycache__" / "sample.txt", "gh" + "p_" + ("A" * 36))

    assert not scan_repository(tmp_path).findings
    assert not candidate_files(tmp_path)
