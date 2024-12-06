from __future__ import annotations

import importlib.metadata
import os
import subprocess
import sys
from typing import TYPE_CHECKING, Any
from unittest import mock

import pytest

from depkit.depmanager import DependencyError, DependencyManager


if TYPE_CHECKING:
    from collections.abc import Generator
    from pathlib import Path


@pytest.fixture
def temp_venv(tmp_path: Path) -> Generator[Path, None, None]:
    """Create a temporary virtual environment structure."""
    venv_path = tmp_path / "venv"
    venv_path.mkdir()
    (venv_path / "bin").mkdir()
    (venv_path / "lib").mkdir()
    os.environ["VIRTUAL_ENV"] = str(venv_path)
    try:
        yield venv_path
    finally:
        os.environ.pop("VIRTUAL_ENV", None)


class TestDependencyManager:
    def test_init(self, settings: dict[str, Any]) -> None:
        """Test initialization."""
        manager = DependencyManager(**settings)
        assert manager.extra_paths == ["."]
        assert not manager._installed

    def test_detect_uv_environment(self, settings: dict[str, Any]) -> None:
        """Test UV environment detection."""
        with mock.patch.dict(os.environ, {"UV_VIRTUAL_ENV": "/path/to/venv"}):
            manager = DependencyManager(**settings)
            assert manager._is_uv

    def test_get_pip_command_uv(self) -> None:
        """Test pip command with UV."""
        manager = DependencyManager(prefer_uv=True)

        with mock.patch("shutil.which", return_value="/usr/local/bin/uv"):
            assert manager._get_pip_command() == ["/usr/local/bin/uv", "pip"]

    def test_check_requirements(
        self, settings: dict[str, Any], mock_importlib: mock.MagicMock
    ) -> None:
        """Test requirement checking."""
        mock_importlib.side_effect = importlib.metadata.PackageNotFoundError()

        manager = DependencyManager(**settings)
        missing = manager.check_requirements()

        assert missing == settings["requirements"]
        assert mock_importlib.call_count == len(settings["requirements"])

    def test_install_requirements(
        self,
        settings: dict[str, Any],
        mock_subprocess: mock.MagicMock,
        mock_importlib: mock.MagicMock,
    ) -> None:
        """Test requirement installation."""
        mock_importlib.side_effect = importlib.metadata.PackageNotFoundError()

        manager = DependencyManager(**settings)
        manager.install_requirements()

        mock_subprocess.assert_called_once()
        cmd = mock_subprocess.call_args[0][0]
        assert "install" in cmd
        assert all(req in cmd for req in settings["requirements"])

    def test_install_requirements_failure(
        self,
        settings: dict[str, Any],
        mock_subprocess: mock.MagicMock,
        mock_importlib: mock.MagicMock,
    ) -> None:
        """Test requirement installation failure."""
        mock_importlib.side_effect = importlib.metadata.PackageNotFoundError()
        mock_subprocess.side_effect = subprocess.CalledProcessError(1, [], stderr="Error")

        manager = DependencyManager(**settings)
        with pytest.raises(DependencyError, match="Failed to install requirements"):
            manager.install_requirements()

    def test_update_python_path(self, tmp_path: Path) -> None:
        """Test Python path updating."""
        path = str(tmp_path)
        original_path = sys.path.copy()

        try:
            manager = DependencyManager(extra_paths=[path])
            manager.update_python_path()

            assert path in sys.path
        finally:
            # Cleanup
            sys.path[:] = original_path

    def test_ensure_importable(self, settings: dict[str, Any]) -> None:
        """Test import checking."""
        manager = DependencyManager(**settings)

        # Should work for stdlib modules
        manager.ensure_importable("os.path")

        with pytest.raises(DependencyError, match="not found"):
            manager.ensure_importable("nonexistent.module")

    @pytest.mark.asyncio
    async def test_setup(
        self,
        settings: dict[str, Any],
        mock_subprocess: mock.MagicMock,
        mock_importlib: mock.MagicMock,
    ) -> None:
        """Test complete setup."""
        mock_importlib.side_effect = importlib.metadata.PackageNotFoundError()

        async with DependencyManager(**settings) as manager:
            assert manager._installed
            mock_subprocess.assert_called_once()

    def test_integration(self, tmp_path: Path) -> None:
        """Integration test with real filesystem."""
        test_dir = tmp_path / "test_dir"
        test_dir.mkdir()
        manager = DependencyManager(
            requirements=["pip"],  # pip should always be available
            extra_paths=[str(test_dir)],
        )
        manager.install_requirements()  # Should not raise
        manager.update_python_path()
        assert str(test_dir) in sys.path

    # platform
    @pytest.mark.parametrize(
        ("platform", "uv_cmd"),
        [
            ("win32", "uv.exe"),
            ("linux", "uv"),
            ("darwin", "uv"),
        ],
    )
    def test_get_pip_command_uv_platform(
        self,
        platform: str,
        uv_cmd: str,
    ) -> None:
        """Test UV command on different platforms."""
        manager = DependencyManager()

        with (
            mock.patch("sys.platform", platform),
            mock.patch("shutil.which", return_value=f"/usr/local/bin/{uv_cmd}"),
        ):
            cmd = manager._get_pip_command()
            assert cmd[0].endswith(uv_cmd)
            assert cmd[1] == "pip"

    @pytest.mark.parametrize(
        ("platform", "python_cmd"),
        [
            ("win32", "python.exe"),
            ("linux", "python3"),
            ("darwin", "python3"),
        ],
    )
    def test_get_pip_command_fallback_platform(
        self,
        platform: str,
        python_cmd: str,
    ) -> None:
        """Test fallback pip command on different platforms."""
        manager = DependencyManager(prefer_uv=False)

        with (
            mock.patch("sys.platform", platform),
            # Mock UV detection to ensure we get pip fallback
            mock.patch.object(manager, "_detect_uv_environment", return_value=False),
            mock.patch("shutil.which", return_value=None),  # No UV in PATH
        ):
            cmd = manager._get_pip_command()
            assert cmd == [sys.executable, "-m", "pip"]

    def test_update_python_path_windows(self, tmp_path: Path) -> None:
        """Test Python path updating on Windows."""
        # Create a real test directory
        test_dir = tmp_path / "test_dir"
        test_dir.mkdir()
        original_path = sys.path.copy()
        try:
            manager = DependencyManager(extra_paths=[str(test_dir)])
            manager.update_python_path()

            # The path should be added and normalized
            assert str(test_dir) in sys.path
            # Check it was added exactly once
            assert sys.path.count(str(test_dir)) == 1
        finally:
            # Restore original sys.path
            sys.path[:] = original_path


# def test_uv_detection(self) -> None:
#     """Test UV environment detection."""
#     settings = GlobalSettings()
#     manager = DependencyManager(settings)

#     # Test UV_VIRTUAL_ENV detection
#     with mock.patch.dict(os.environ, {"UV_VIRTUAL_ENV": "/some/path"}):
#         assert manager._detect_uv_environment()

#     # Test UV in PATH detection
#     with (
#         mock.patch.dict(os.environ, {}, clear=True),
#         mock.patch("shutil.which", return_value="/path/to/uv"),
#     ):
#         assert manager._detect_uv_environment()

#     # Test no UV
#     with (
#         mock.patch.dict(os.environ, {}, clear=True),
#         mock.patch("shutil.which", return_value=None),
#     ):
#         assert not manager._detect_uv_environment()
