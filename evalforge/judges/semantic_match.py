"""Semantic similarity judge using embedding-based comparison."""

from __future__ import annotations

import hashlib
import math

from evalforge.config import get_settings
from evalforge.judges.base import BaseJudge, JudgeResult
from evalforge.models.test_case import TestCase


class SemanticMatchJudge(BaseJudge):
    """Judge that evaluates semantic similarity between response and expected answer.

    Uses a simplified similarity computation based on token overlap and
    common n-grams. In production, this would use embedding models.

    Args:
        threshold: Minimum similarity score to consider a match (0.0-1.0).
    """

    def __init__(self, threshold: float | None = None) -> None:
        """Initialize with an optional threshold override.

        Args:
            threshold: Override for the default similarity threshold.
        """
        settings = get_settings()
        self._threshold = threshold if threshold is not None else settings.SIMILARITY_THRESHOLD

    def judge(self, test_case: TestCase, response: str) -> JudgeResult:
        """Evaluate semantic similarity between response and expected answer.

        Args:
            test_case: The test case with the expected answer.
            response: The actual AI response.

        Returns:
            JudgeResult with similarity score and pass/fail status.
        """
        expected = str(test_case.expected) if test_case.expected is not None else ""
        threshold = test_case.metadata.get("threshold", self._threshold)

        similarity = self._compute_similarity(response, expected)
        passed = similarity >= threshold

        return JudgeResult(
            passed=passed,
            score=similarity,
            details={
                "expected": expected,
                "actual": response,
                "similarity": similarity,
                "threshold": threshold,
                "match_type": "semantic",
            },
        )

    def _compute_similarity(self, text_a: str, text_b: str) -> float:
        """Compute semantic similarity between two texts.

        Uses token-level Jaccard similarity with shingling for
        n-gram overlap detection.

        Args:
            text_a: First text to compare.
            text_b: Second text to compare.

        Returns:
            Similarity score between 0.0 and 1.0.
        """
        tokens_a = set(text_a.lower().split())
        tokens_b = set(text_b.lower().split())

        if not tokens_a and not tokens_b:
            return 1.0
        if not tokens_a or not tokens_b:
            return 0.0

        intersection = tokens_a & tokens_b
        union = tokens_a | tokens_b
        jaccard = len(intersection) / len(union)

        shingles_a = self._shingles(text_a.lower(), 3)
        shingles_b = self._shingles(text_b.lower(), 3)

        if shingles_a and shingles_b:
            shingle_intersection = shingles_a & shingles_b
            shingle_union = shingles_a | shingles_b
            shingle_sim = len(shingle_intersection) / len(shingle_union)
        else:
            shingle_sim = 0.0

        combined = 0.5 * jaccard + 0.5 * shingle_sim
        return round(combined, 4)

    def _shingles(self, text: str, n: int) -> set[str]:
        """Generate n-gram shingles from text.

        Args:
            text: The text to shingle.
            n: The shingle size (number of words).

        Returns:
            A set of shingle strings.
        """
        words = text.split()
        if len(words) < n:
            return {text}
        return {" ".join(words[i : i + n]) for i in range(len(words) - n + 1)}
