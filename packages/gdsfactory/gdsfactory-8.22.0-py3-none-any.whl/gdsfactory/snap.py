"""snaps values and coordinates to the GDS grid in nm."""

from __future__ import annotations

import warnings
from functools import partial

import kfactory as kf
import numpy as np
import numpy.typing as npt

Value = float | tuple[float, ...] | npt.NDArray[np.float64]


def is_on_grid(
    x: Value,
    nm: int | None = None,
    grid_factor: int = 1,
) -> bool:
    return np.array_equal(
        snap_to_grid(x, grid_factor=grid_factor, nm=nm), np.round(x, 6)
    )


def warn_if_not_on_grid(x: Value) -> None:
    if not is_on_grid(x):
        warnings.warn(f"{x} is not on grid", stacklevel=2)


def assert_on_grid(
    x: Value,
    nm: int | None = None,
    grid_factor: int = 1,
) -> None:
    x_grid = snap_to_grid(x, nm=nm, grid_factor=grid_factor)
    if not np.isclose(x_grid, x, rtol=0).all():
        raise ValueError(f"{x} needs to be on 1nm grid and should be {x_grid}")


assert_on_1nm_grid = partial(assert_on_grid, nm=1)
assert_on_2nm_grid = partial(assert_on_grid, nm=2)


def assert_on_2x_grid(x: float) -> None:
    x_grid = snap_to_grid(x, grid_factor=2)
    if not np.isclose(x_grid, x, rtol=0).all():
        raise ValueError(f"{x} needs to be on 2x grid and should be {x_grid}")


def snap_to_grid(
    x: Value,
    nm: int | None = None,
    grid_factor: int = 1,
) -> npt.NDArray[np.float64]:
    """Snap x to grid.

    Args:
        x: value to snap.
        nm: Optional grid size in nm. If None, it will use the default grid size from PDK multiplied by grid_factor.
        grid_factor: snap to grid_factor * grid_size.
    """
    grid_size = kf.kcl.dbu
    nm = nm or round(grid_size * 1000 * grid_factor)
    return nm * np.round(np.asarray(x, dtype=float) * 1e3 / nm) / 1e3


snap_to_grid2x = partial(snap_to_grid, grid_factor=2)


if __name__ == "__main__":
    print(assert_on_grid(1.1e-3))
    # print(snap_to_grid(1.1e-3))
    # print(snap_to_2nm_grid(1.1e-3))
    # print(snap_to_2nm_grid(3.1e-3))

    # print(on_1nm_grid(1.1e-3))
    # print(on_1nm_grid(1e-3))

    # print(on_2nm_grid(1.1e-3))
    # print(on_2nm_grid(1e-3))
    # print(on_2nm_grid(2e-3))
