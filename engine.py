"""Framework-independent mystery game state and deduction rules."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass(frozen=True)
class Analysis:
    """The result of comparing one statement with one independent fact."""

    outcome: str
    message: str


@dataclass
class MysteryEngine:
    """Runs a single data-driven case without depending on the GUI toolkit."""

    case: dict[str, Any]
    selected_location: str = field(init=False)
    investigated: set[str] = field(default_factory=set)
    discovered_evidence: set[str] = field(default_factory=set)
    discovered_testimonies: set[str] = field(default_factory=set)
    found_contradictions: set[str] = field(default_factory=set)
    contradiction_found: bool = False
    solved: bool = False

    def __post_init__(self) -> None:
        locations = self.case["locations"]
        if not locations:
            raise ValueError("案件至少需要一个地点。")
        self.selected_location = locations[0]["id"]
        self._locations = {item["id"]: item for item in locations}
        self._evidence = {item["id"]: item for item in self.case["evidence"]}
        self._testimonies = {item["id"]: item for item in self.case["testimonies"]}

    @property
    def current_location(self) -> dict[str, Any]:
        return self._locations[self.selected_location]

    @property
    def progress_percent(self) -> int:
        return round(len(self.investigated) / len(self._locations) * 100)

    @property
    def can_accuse(self) -> bool:
        required = set(self.case["final_accusation"]["required_evidence"])
        return self.has_required_contradictions and required.issubset(self.discovered_evidence) and not self.solved

    @property
    def has_required_contradictions(self) -> bool:
        """Check that the contradiction needed for this specific accusation exists."""
        required = set(self.case["final_accusation"].get("required_contradictions", []))
        return self.contradiction_found and required.issubset(self.found_contradictions)

    def select_location(self, location_id: str) -> None:
        if location_id not in self._locations:
            raise KeyError(f"未知地点：{location_id}")
        self.selected_location = location_id

    def investigate_current_location(self) -> list[str]:
        location = self.current_location
        if location["id"] in self.investigated:
            return []
        self.investigated.add(location["id"])
        self.discovered_evidence.update(location["evidence"])
        self.discovered_testimonies.update(location["testimonies"])
        return [*location["evidence"], *location["testimonies"]]

    def available_evidence(self) -> list[dict[str, Any]]:
        return [item for item in self.case["evidence"] if item["id"] in self.discovered_evidence]

    def available_testimonies(self) -> list[dict[str, Any]]:
        return [item for item in self.case["testimonies"] if item["id"] in self.discovered_testimonies]

    def is_cross_scene_link_resolved(self, evidence: dict[str, Any]) -> bool:
        """Return whether the location needed to interpret a linked clue was searched.

        Cross-scene clues are deliberately collected as normal evidence first.
        Their connection becomes reliable only after the player has visited the
        related location, so no GUI-specific state is needed here.
        """
        related_location = evidence.get("related_location")
        return bool(
            evidence.get("kind") == "cross-scene"
            and evidence.get("id") in self.discovered_evidence
            and related_location in self.investigated
        )

    def analyze(self, statement_id: str, evidence_id: str) -> Analysis:
        if statement_id not in self.discovered_testimonies or evidence_id not in self.discovered_evidence:
            return Analysis("error", "请先收集并选择一条证词与一项物证。")
        for rule in self.case["reasoning_rules"]:
            if rule["statement"] == statement_id and rule["evidence"] == evidence_id:
                if rule["outcome"] == "contradiction":
                    self.contradiction_found = True
                    rule_id = rule.get("id", f"{statement_id}:{evidence_id}")
                    self.found_contradictions.add(rule_id)
                return Analysis(rule["outcome"], rule["message"])
        return Analysis("insufficient", self.case["fallback_reasoning"])

    def accuse(self, suspect_id: str) -> Analysis:
        if not self.can_accuse:
            return Analysis("error", "证据链尚未完整，现在还不能提交指控。")
        final = self.case["final_accusation"]
        if suspect_id != final["culprit"]:
            return Analysis("failure", final["failure"])
        self.solved = True
        return Analysis("success", final["success"])
