from dataclasses import dataclass, field
from typing import Dict, Any, List,Optional


@dataclass
class FraudCase:
    case_id: str
    alert_id: str

    transaction: Dict[str, Any]
    user_profile: Dict[str, Any]
    triggered_rules: List[str]

    agent_outputs: Dict[str, Any] = field(default_factory=dict)
    final_verdict: Optional[Dict[str, Any]] = None