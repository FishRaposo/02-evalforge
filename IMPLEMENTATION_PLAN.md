# Implementation Plan

## Phase 1 — Core (MVP)

**Goal**: Run a basic evaluation suite end-to-end with mock backend.

### Deliverables
- [ ] Suite loader: Parse and validate YAML test suites
- [ ] Basic judges: `ExactMatchJudge`, `SemanticMatchJudge`
- [ ] Mock backend: Return pre-configured responses for testing
- [ ] RAG runner: Execute test cases against backend, collect responses
- [ ] CLI `eval` command: `evalforge eval suite.yaml`
- [ ] Markdown reporter: Generate pass/fail report
- [ ] Pydantic models: `TestCase`, `TestResult`, `Report`

### Acceptance Criteria
- Can run `evalforge eval example_suites/rag_basic.yaml` end-to-end
- Markdown report is generated with correct pass/fail counts
- All unit tests pass

---

## Phase 2 — Intelligence

**Goal**: Add advanced judges, real backend support, and CI integration.

### Deliverables
- [ ] Citation judge: Verify source citations in responses
- [ ] Refusal judge: Detect and validate refusal behavior
- [ ] Retrieval judge: Check retrieved document correctness
- [ ] OpenAI-compatible backend: Call real API endpoints
- [ ] JSON reporter: Structured output for programmatic consumption
- [ ] HTML reporter: Styled report with tables and charts
- [ ] CLI enhancements: `--backend`, `--format`, `--output` flags
- [ ] GitHub Actions workflow: Run evals on push/PR
- [ ] Error handling: Backend failures, timeouts, partial results

### Acceptance Criteria
- Can run evaluations against OpenAI API with real responses
- Citation, refusal, and retrieval judges work correctly
- CI pipeline runs evaluations and uploads reports
- JSON and HTML reports are generated

---

## Phase 3 — Polish

**Goal**: Production-ready with agent support and extensibility.

### Deliverables
- [ ] Agent runner: Test tool-use sequences and multi-step chains
- [ ] Forbidden content judge: Detect policy violations
- [ ] Drift detection: Compare results across runs, flag regression
- [ ] Custom judge API: Plugin system for user-defined judges
- [ ] Performance optimization: Concurrent execution, caching
- [ ] `evalforge list-suites` command: Discover available suites
- [ ] `evalforge init` command: Scaffold example suites
- [ ] Comprehensive documentation and examples
- [ ] Type coverage: Full mypy strict compliance

### Acceptance Criteria
- Agent runner handles multi-step tool chains
- Drift detection flags quality regression
- Custom judges can be loaded via entry points
- All tests pass, type checking is clean
