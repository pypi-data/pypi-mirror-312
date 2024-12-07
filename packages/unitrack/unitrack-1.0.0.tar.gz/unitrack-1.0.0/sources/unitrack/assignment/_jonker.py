from __future__ import annotations

from typing import Tuple

import numpy as np
import torch
import torch.fx
import typing_extensions as TX
from ._base import Assignment

__all__ = ["Jonker", "jonker_volgenant_assignment"]

class Jonker(Assignment):
    """
    Uses the Jonker-Volgenant algorithm to solve the linear assignment problem.
    """

    @TX.override
    def _assign(
        self, cost_matrix: torch.Tensor
    ) -> Tuple[torch.Tensor, torch.Tensor, torch.Tensor]:
        return jonker_volgenant_assignment(cost_matrix, self.threshold)


def jonker_volgenant_assignment(
    cost_matrix: torch.Tensor, threshold: float
) -> Tuple[torch.Tensor, torch.Tensor, torch.Tensor]:
    """
    Perform linear assignment. If possible, an assignment on the diagonal of the
    matrix is preferred if this assignment has equal cost to the algorithm
    result.

    TODO: PyTorch implementation
    """

    from lap import lapjv

    device = cost_matrix.device
    cost_matrix = cost_matrix.detach().cpu().contiguous()
    cost_matrix = np.ascontiguousarray(cost_matrix).astype(np.float64)
    cost_matrix = np.where(np.isfinite(cost_matrix), cost_matrix, np.inf)
    matches, unmatched_a, unmatched_b = [], [], []

    # Jonker algorithm, i.e. linear sum assignment (rows) -> (cols)
    cost, x, y = lapjv(cost_matrix, extend_cost=True, cost_limit=threshold)

    # Create match and unassigned lists
    for ix in range(x.shape[0]):
        mx = x[ix]
        if mx < 0:
            continue
        c = cost_matrix[ix, mx]
        if not np.isfinite(c):
            continue
        matches.append([ix, mx])

    unmatched_a = torch.from_numpy(np.where(x < 0)[0]).clone().long()
    unmatched_b = torch.from_numpy(np.where(y < 0)[0]).clone().long()
    matches = torch.from_numpy(np.asarray(matches)).clone().long()

    # NOTE: Too verbose. Needs revision
    # if check_debug_enabled():
    #     print(f"Jonker-Volgenant Assignment completed with total cost: {cost}")
    #     for i, j in matches:
    #         print(f"- match: C {i} -> D {j} (cost: {cost_matrix[i,j]})")

    #     unmatch_min_cost = [
    #         f"{i} (min. cost: {cost_matrix[i, :].min()})" for i in unmatched_a
    #     ]
    #     print(f"Unmatched C: {unmatch_min_cost}")

    #     unmatch_min_cost = [
    #         f"{i} (min. cost: {cost_matrix[:, i].min()})" for i in unmatched_b
    #     ]
    #     print(f"Unmatched D: {unmatch_min_cost}")

    return matches.to(device), unmatched_a.to(device), unmatched_b.to(device)


torch.fx.wrap("jonker_volgenant_assignment")
