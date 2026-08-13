from pathlib import Path
import re


ROOT = Path(__file__).resolve().parents[1]
CAUSAL = ROOT / "docs" / "c147-review-free-portable-core-causal-reclassification.md"
DESIGN = ROOT / "docs" / "c147-review-free-portable-core-design.md"
AUDIT = ROOT / "docs" / "c147-review-free-portable-core-direction-audit.md"
REANALYSIS = ROOT / "docs" / "c147-functional-decomposition-reanalysis.md"
GROUP_AUDIT = ROOT / "docs" / "c147-control-group-overlap-optimality-audit.md"
F06_AUTHORITY_AUDIT = ROOT / "docs" / "c147-f06-authority-route-causal-audit.md"
VALIDATION_OVERLAP_AUDIT = ROOT / "docs" / "c147-validation-control-overlap-causal-audit.md"
RUNTIME_SURFACE_AUDIT = ROOT / "docs" / "c147-runtime-surface-portability-audit.md"
STANDARD14_INSUFFICIENCY_AUDIT = ROOT / "docs" / "c147-standard14-control-insufficiency-audit.md"


def _core_text() -> str:
    text = DESIGN.read_text()
    start = "<!-- PORTABLE_CORE_BEGIN -->"
    end = "<!-- PORTABLE_CORE_END -->"
    assert text.count(start) == 1
    assert text.count(end) == 1
    return text.split(start, 1)[1].split(end, 1)[0]


def test_reclassification_is_superseded_by_functional_reanalysis() -> None:
    text = CAUSAL.read_text()
    for fragment in (
        "superseded",
        "M1_completion_withdrawn",
        "functional_decomposition_reopened",
        "c147-functional-decomposition-reanalysis.md",
    ):
        assert fragment in text


def test_reanalysis_covers_all_c147_clauses_and_missing_transition_classes() -> None:
    text = REANALYSIS.read_text()
    for clause in (
        "SPEC",
        "PRODUCER",
        "TERMINAL",
        "CONTEXT",
        "EVIDENCE_GATE",
        "OWNER_ROLE",
        "ROOT",
        "INDEPENDENCE",
        "DECISION_BOUNDARY",
        "VALIDATION_CLOSURE",
        "VALIDATION_PLAN",
        "METHOD",
        "RECOVERY",
    ):
        assert f"### `{clause}`" in text
    for primitive in ("`E12`", "`O2`", "`D4`", "`D5`", "`D6`", "`D7`", "`VC3`", "`VP4`"):
        assert primitive in text
    for observation in (
        "最初の一つのtool発行にidentity観測とreadの両方を含む | 15 / 15",
        "identity resultを外側の次判断へ返した後にreadを別発行 | 0 / 15",
        "C205の成立数は強いイベント順序基準では0 / 15",
    ):
        assert observation in text


def test_reanalysis_has_eighty_one_unique_primitives_without_optimality_claim() -> None:
    text = REANALYSIS.read_text()
    inventory = text.split("## 全13条項の機能primitive", 1)[1].split(
        "## C204/C205との対応", 1
    )[0]
    primitive_ids = re.findall(r"\| `([A-Z]+\d+)` \|", inventory)
    assert len(primitive_ids) == 81
    assert len(set(primitive_ids)) == 81
    assert "意味ごと削除してよいと立証できたものは現時点で0件" in text
    assert "意味の除去は全件`not_evaluated`" in text
    assert "Standard14通過を最適性へ読み替えず" in text


def test_control_group_audit_keeps_thirteen_groups_and_classifies_overlaps() -> None:
    text = GROUP_AUDIT.read_text()
    group_table = text.split("## 13制御群がまとめて制御するもの", 1)[1].split(
        "## 境界重複の分類", 1
    )[0]
    group_rows = re.findall(r"^\| `([A-Z_]+)` \|", group_table, re.MULTILINE)
    for group in (
        "SPEC",
        "PRODUCER",
        "TERMINAL",
        "CONTEXT",
        "EVIDENCE_GATE",
        "OWNER_ROLE",
        "ROOT",
        "INDEPENDENCE",
        "DECISION_BOUNDARY",
        "VALIDATION_CLOSURE",
        "VALIDATION_PLAN",
        "METHOD",
        "RECOVERY",
    ):
        assert group_rows.count(group) == 1
    assert len(group_rows) == 13
    for classification in (
        "### 防御的強化",
        "### 相互制限",
        "### handoff",
        "### 一般制御と局所強化",
        "### 競合・冗長候補",
    ):
        assert classification in text
    assert "確定した境界競合は0件" in text


def test_control_group_audit_bounds_optimality_and_hypotheses() -> None:
    text = GROUP_AUDIT.read_text()
    for fragment in (
        "optimality_not_evaluated",
        "Standard14 N=100",
        "除去・短縮・portable置換した比較ではない",
        "### H1: F06 authority追加read残差",
        "### H2: validation二条項の重複cost",
        "### H3: start gate barrier（現行最適化から除外）",
        "### H4: producer系三条項の読解cost",
        "Candidate作成許可ではない",
    ):
        assert fragment in text


def test_f06_authority_audit_separates_required_reads_from_route_cost() -> None:
    text = F06_AUTHORITY_AUDIT.read_text()
    for fragment in (
        "required_path_instruction_reads_17",
        "path-local instructionだけを含む | 13",
        "path-local instructionとroot instructionの両方 | 4",
        "root instructionだけ | 2",
        "discoveryだけ | 2",
        "authority関連21 runを全て削減できる | `rejected`",
        "locator探索を狭められる | `optimization_hypothesis`",
        "path-local instruction readを省ける | `change_not_justified`",
        "model_visible_inputs_21_verified",
        "root `AGENTS.md`のC147本文 | 21 / 21 | 6 / 21",
        "`tests/AGENTS.md`本文 | 0 / 21 | 17 / 21",
        "result effectを持たなかった失敗probe",
        "locator commandをpromptで一意に固定する | `change_not_justified`",
        "ADR9_saved_runs_450_checked",
        "ADR9_redundant_root_reads_111",
        "合計 | 111 / 450",
        "112 / 112 task",
        "isolated_prompt_trial_not_ready",
    ):
        assert fragment in text
    run_ids = re.findall(r"^[0-9a-f]{32}$", text, re.MULTILINE)
    assert len(run_ids) == 21
    assert len(set(run_ids)) == 21


def test_validation_overlap_audit_distinguishes_handoff_from_redundancy() -> None:
    text = VALIDATION_OVERLAP_AUDIT.read_text()
    for fragment in (
        "saved_validation_runs_190_audited",
        "required_command_groups_403",
        "one_wrapper_189",
        "split_wrapper_1",
        "repeated_required_command_0",
        "nonterminal_wait_runs_52",
        "wait_invocations_79",
        "wait_interleaving_0",
        "supported / intentional_handoff_and_specialization",
        "required-validation 685件",
        "prebound_completion_evidence_22_of_22",
        "nonterminal_ticket_bypass_11",
        "terminal_visible_evidence_reacquisition_10",
        "H2a_missing_relation_rejected",
        "existing_control_deviation / candidate_not_justified",
    ):
        assert fragment in text


def test_runtime_surface_audit_separates_names_from_observation_points() -> None:
    text = RUNTIME_SURFACE_AUDIT.read_text()
    for fragment in (
        "runtime_surface_inventory_completed",
        "machine_observation_points_separated",
        "H3_rejected_as_current_overquality",
        "役割名",
        "機械field",
        "発行境界",
        "設定名",
        "強いcommand event順ではidentity完了前にreadを開始したrunが0 / 15",
        "52 runの79 `wait`",
        "start gateと少なくとも一つのreview対象readを同じ発行群へ入れたrunが19 / 100件",
        "追加barrierは過剰品質として除外する",
    ):
        assert fragment in text
    for clause in (
        "PRODUCER",
        "TERMINAL",
        "CONTEXT",
        "OWNER_ROLE",
        "ROOT",
        "DECISION_BOUNDARY",
        "VALIDATION_CLOSURE",
        "VALIDATION_PLAN",
        "RECOVERY",
    ):
        assert f"| `{clause}` |" in text


def test_standard14_insufficiency_audit_drives_optimization_from_results() -> None:
    text = STANDARD14_INSUFFICIENCY_AUDIT.read_text()
    for fragment in (
        "standard14_n100_primary_result_bound",
        "quality_1400_of_1400",
        "archived_event_runs_1385_audited",
        "root_reread_runs_130",
        "start_gate_review_read_overcoissue_19_of_100",
        "validation_false_unavailable_rerun_1_of_685",
        "hidden_full_exit_normal_59_of_60",
        "validation_followup_exec_22_of_685",
        "all-agent token中央値 | 1,394,412.5",
        "owner / producer evidenceの`inadmissible` 950 / 1,400件は不足件数ではない",
        "累積はexact 94 / 100、mismatch 6 / 100",
        "admitted_evidence_current",
        "再取得しなかったiteration 88もScore 4",
        "許可readへ列挙していても、それはread上限であって発行要件ではない",
        "operation_start_member",
        "terminal_status_admitted",
        "H1 revised",
        "H2a closed",
        "H2b analyzed",
        "同型表示省略60件中59件は正常",
        "positive_relation_hypothesis / candidate_not_ready",
        "H3 rejected",
        "rejected_as_current_overquality",
        "全22件で後から取得したdiff / status / source等をvalidation開始前に明示",
        "既存制御の同義反復をCandidateへ足さない",
        "現時点ではprompt set、profile、preflightまたは評価slotを作らない",
    ):
        assert fragment in text


def test_portable_core_has_exactly_twelve_single_owner_labels() -> None:
    core = _core_text()
    labels = (
        "OUTCOME",
        "PRODUCER",
        "INPUT",
        "INVOCATION",
        "RESULT_ADMISSION",
        "RESULT_EFFECT",
        "IMPLEMENTATION",
        "COMPLETION",
        "VALIDATION_PLAN",
        "VALIDATION_CLOSURE",
        "METHOD",
        "RECOVERY",
    )
    lines = [line for line in core.splitlines() if line.startswith("- ")]
    assert len(lines) == len(labels)
    assert [line.split(":", 1)[0][2:] for line in lines] == list(labels)


def test_portable_core_excludes_review_and_runtime_surface_terms() -> None:
    core = _core_text()
    forbidden = (
        "review",
        "Codex",
        "root",
        "worker",
        "fork_turns",
        "FINAL_ANSWER",
        "runtime_spawn_result",
        "custom exec",
        "exec_command",
        "cell ID",
        "model step",
        "modelへ戻らず",
        "environment_recovery_max",
    )
    for fragment in forbidden:
        assert fragment not in core


def test_design_is_superseded_but_keeps_historical_core_closed() -> None:
    text = DESIGN.read_text()
    for fragment in (
        "superseded",
        "M2_completion_withdrawn",
        "functional_coverage_incomplete",
        "c147-functional-decomposition-reanalysis.md",
        "初稿にmethod resultとpredicate resultのterminal競合が1件",
        "修正した後のblocking counterexampleは0件",
        "M3が閉じる前はcandidate bundle、profile、preflight、評価slotを作成しない",
    ):
        assert fragment in text


def test_direction_audit_permission_is_withdrawn() -> None:
    text = AUDIT.read_text()
    for fragment in (
        "superseded",
        "prior_M3_permission_withdrawn",
        "input_M1_M2_incomplete",
        "c147-functional-decomposition-reanalysis.md",
        "一般18状態",
        "prompt_control_not_demonstrated / candidate_not_created_or_stopped",
        "preflightが`ready`でなければ評価slotを一件も発行しない",
    ):
        assert fragment in text
