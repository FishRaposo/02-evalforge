"""Abstract base class for test runners."""

from __future__ import annotations

import time
from abc import ABC, abstractmethod
from typing import Any

from evalforge.backends.base import BaseBackend
from evalforge.models.test_case import TestCase, TestSuite
from evalforge.models.test_result import TestResult


class BaseRunner(ABC):
    """Abstract base class for all test runners.

    Provides the common interface and shared utilities for running
    test cases against backends and collecting results.

    Args:
        backend: The AI backend to use for executing test cases.
    """

    def __init__(self, backend: BaseBackend) -> None:
        """Initialize the runner with a backend.

        Args:
            backend: The backend instance for making AI queries.
        """
        self._backend = backend

    @abstractmethod
    async def run(self, test_case: TestCase) -> TestResult:
        """Execute a single test case and return the result.

        Args:
            test_case: The test case to execute.

        Returns:
            The evaluation result for the test case.
        """
        ...

    async def run_suite(self, suite: TestSuite) -> list[TestResult]:
        """Execute all test cases in a suite sequentially.

        Args:
            suite: The test suite containing test cases to run.

        Returns:
            A list of test results, one per test case.
        """
        results: list[TestResult] = []
        for test_case in suite.test_cases:
            result = await self.run(test_case)
            results.append(result)
        return results

    def _create_result(
        self,
        test_case: TestCase,
        passed: bool,
        score: float,
        response: str,
        judge_details: dict[str, Any] | None = None,
        error: str | None = None,
        elapsed_ms: float = 0.0,
    ) -> TestResult:
        """Create a TestResult with standard fields.

        Args:
            test_case: The source test case.
            passed: Whether the test passed.
            score: Numerical score from the judge.
            response: The raw response from the backend.
            judge_details: Detailed judge output.
            error: Optional error message.
            elapsed_ms: Execution time in milliseconds.

        Returns:
            A populated TestResult instance.
        """
        return TestResult(
            test_case_id=test_case.id,
            test_case_name=test_case.name,
            passed=passed,
            score=score,
            actual_response=response,
            judge_details=judge_details or {},
            execution_time_ms=elapsed_ms,
            error=error,
        )
