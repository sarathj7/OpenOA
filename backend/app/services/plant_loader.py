from __future__ import annotations

import shutil
from dataclasses import dataclass
from pathlib import Path
from threading import Lock
from zipfile import ZipFile

from openoa.plant import PlantData


@dataclass(frozen=True)
class PlantLoaderConfig:
    repo_root: Path
    openoa_example_zip_path: Path
    data_dir: Path


class PlantLoader:
    """
    Loads and caches a PlantData instance.

    Notes:
    - Uses OpenOA's `examples/project_ENGIE.py` loader to build PlantData.
    - Extracts the example dataset zip if needed.
    """

    def __init__(self, config: PlantLoaderConfig):
        self._config = config
        self._lock = Lock()
        self._plant: PlantData | None = None

    def get_plant(self) -> PlantData:
        if self._plant is not None:
            return self._plant

        with self._lock:
            if self._plant is not None:
                return self._plant

            self._ensure_example_data_extracted()
            self._plant = self._load_plant_with_openoa_loader()
            return self._plant

    def _ensure_example_data_extracted(self) -> None:
        repo = self._config.repo_root.resolve()
        data_dir = (repo / self._config.data_dir).resolve()
        target_dir = (data_dir / "la_haute_borne").resolve()
        zip_path = (repo / self._config.openoa_example_zip_path).resolve()

        data_dir.mkdir(parents=True, exist_ok=True)

        # Copy plant_meta.yml from examples/data so PlantData can find it (prepare() uses path.parent / "plant_meta.yml")
        meta_src = repo / "examples" / "data" / "plant_meta.yml"
        meta_dst = data_dir / "plant_meta.yml"
        if meta_src.exists() and (not meta_dst.exists() or meta_src.stat().st_mtime > meta_dst.stat().st_mtime):
            shutil.copy2(meta_src, meta_dst)

        # If already extracted, skip
        if (target_dir / "la-haute-borne-data-2014-2015.csv").exists():
            return

        if not zip_path.exists():
            raise FileNotFoundError(f"OpenOA example zip not found at: {zip_path}")

        target_dir.mkdir(parents=True, exist_ok=True)
        with ZipFile(zip_path) as zf:
            zf.extractall(target_dir)

    def _load_plant_with_openoa_loader(self) -> PlantData:
        """
        Import OpenOA's example loader and construct PlantData.

        We intentionally import at runtime so the backend can run even if the
        examples module isn't imported elsewhere.
        """

        # Local import: this repository includes the examples package.
        from examples.project_ENGIE import prepare  # type: ignore

        extracted_dir = (self._config.repo_root / self._config.data_dir / "la_haute_borne").resolve()
        return prepare(path=extracted_dir, return_value="plantdata", use_cleansed=False)


_singleton_lock = Lock()
_singleton: PlantLoader | None = None


def get_plant_loader(
    repo_root: Path,
    openoa_example_zip_path: str,
    data_dir: str,
) -> PlantLoader:
    global _singleton
    if _singleton is not None:
        return _singleton

    with _singleton_lock:
        if _singleton is not None:
            return _singleton
        _singleton = PlantLoader(
            PlantLoaderConfig(
                repo_root=repo_root,
                openoa_example_zip_path=Path(openoa_example_zip_path),
                data_dir=Path(data_dir),
            )
        )
        return _singleton

