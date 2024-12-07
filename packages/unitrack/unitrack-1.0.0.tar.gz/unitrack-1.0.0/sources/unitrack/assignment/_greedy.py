"""
Greedy assignment is a simple assignment algorithm that greedily assigns 
detections to tracklets, by selecting the best match at each step. This
algorithm is not guaranteed to find the optimal solution, but it is fast
and simple to implement.
"""

from __future__ import annotations

from typing import Tuple

import torch
import torch.fx

from ._base import Assignment

__all__ = ["Greedy", "greedy_assignment"]


class Greedy(Assignment):
    """
    See :func:`.greedy_assignment` for details.
    """

    def _assign(
        self, cost_matrix: torch.Tensor
    ) -> Tuple[torch.Tensor, torch.Tensor, torch.Tensor]:
        return greedy_assignment(cost_matrix)


@torch.no_grad()
def greedy_assignment(
    cost_matrix: torch.Tensor,
) -> Tuple[torch.Tensor, torch.Tensor, torch.Tensor]:
    """
    Performs a greedy assignment algorithm on a cost matrix, assigning pairs of elements (rows and columns) based on
    the minimum cost, with a threshold as the stopping condition.

    Parameters
    ----------
    cost_matrix : torch.Tensor
        A 2D tensor representing the cost matrix.
    threshold : float
        The maximum cost allowed for an assignment.

    Returns
    -------
    matches : torch.Tensor
        A tensor containing the indices of matched row-column pairs.
    unmatched_rows : torch.Tensor
        A tensor containing the indices of unmatched rows.
    unmatched_cols : torch.Tensor
        A tensor containing the indices of unmatched columns.

    """
    with cost_matrix.device:
        N, M = cost_matrix.shape
        matches = torch.full((min(N, M), 2), -1, dtype=torch.long)
        unmatched_rows = torch.arange(N, dtype=torch.long)
        unmatched_cols = torch.arange(M, dtype=torch.long)

        match_count = 0
        while True:
            min_val, idx = torch.min(cost_matrix.flatten(), dim=0)
            row, col = idx // M, idx % M

            if not torch.isfinite(min_val):
                break

            matches[match_count] = torch.tensor([row, col], dtype=torch.long)
            match_count += 1

            cost_matrix[row, :] = torch.inf
            cost_matrix[:, col] = torch.inf

        unmatched_rows = unmatched_rows[torch.isfinite(cost_matrix[:, 0])]
        unmatched_cols = unmatched_cols[torch.isfinite(cost_matrix[0, :])]

    return matches[:match_count], unmatched_rows, unmatched_cols


torch.fx.wrap("greedy_assignment")
