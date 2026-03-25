import json
import re
import subprocess
from pathlib import Path
from datetime import datetime
from typing import Any, Dict, List, Optional, Tuple

import requests
import streamlit as st


# =========================================================
# PAGE CONFIG
# =========================================================
st.set_page_config(
    page_title="RoboMed Dashboard",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# =========================================================
# CUSTOM CSS
# =========================================================
st.markdown(
    """
    <style>
    :root {
        --bg-main: #0b1620;
        --bg-panel: #102233;
        --bg-panel-2: #13304a;
        --accent-blue: #2f80ed;
        --accent-green: #1d7a6f;
        --ok: #1fa36a;
        --warn: #d7a53c;
        --danger: #d84f68;
        --text-main: #eef5fb;
        --text-soft: #a8bbcf;
        --border-soft: rgba(180, 205, 230, 0.12);
    }

    .stApp {
        background:
            radial-gradient(circle at top right, rgba(47,128,237,0.10), transparent 28%),
            linear-gradient(180deg, #0b1620 0%, #0c1b28 100%);
    }

    .block-container {
        max-width: 1540px;
        padding-top: 0.45rem;
        padding-bottom: 0.35rem;
        padding-left: 0.9rem;
        padding-right: 0.9rem;
    }

    .brand-strip {
        background: linear-gradient(180deg, rgba(19,48,74,0.95), rgba(11,22,32,0.98));
        border: 1px solid var(--border-soft);
        border-radius: 18px;
        min-height: 94vh;
        display: flex;
        align-items: center;
        justify-content: center;
        box-shadow: 0 10px 28px rgba(0,0,0,0.18);
    }

    .brand-vertical {
        writing-mode: vertical-rl;
        transform: rotate(180deg);
        color: #edf6ff;
        font-size: 2.0rem;
        font-weight: 900;
        letter-spacing: 0.08em;
    }

    .brand-vertical-sub {
        writing-mode: vertical-rl;
        transform: rotate(180deg);
        color: #8fc1ff;
        font-size: 0.92rem;
        font-weight: 800;
        letter-spacing: 0.12em;
        margin-top: 20px;
    }

    .subline {
        font-size: 1.02rem;
        color: #a7c1db;
        margin-bottom: 0.35rem;
        font-weight: 650;
    }

    .section-title {
        font-size: 1.20rem;
        font-weight: 850;
        color: #ecf4ff;
        margin-top: 0.15rem;
        margin-bottom: 0.4rem;
    }

    .metric-card {
        background: linear-gradient(180deg, rgba(16,34,51,0.98), rgba(13,27,41,0.98));
        border: 1px solid var(--border-soft);
        border-radius: 16px;
        padding: 10px 14px;
        min-height: 78px;
        box-shadow: 0 8px 22px rgba(0,0,0,0.15);
        margin-bottom: 0.22rem;
    }

    .metric-title {
        font-size: 0.77rem;
        color: #a5b9cf;
        margin-bottom: 4px;
    }

    .metric-value {
        font-size: 1.10rem;
        font-weight: 850;
        color: #f4f9ff;
        word-break: break-word;
    }

    .status-wrap {
        display: flex;
        align-items: center;
        gap: 12px;
        padding: 12px 16px;
        border-radius: 16px;
        border: 1px solid var(--border-soft);
        background: linear-gradient(180deg, rgba(16,34,51,0.98), rgba(13,27,41,0.98));
        box-shadow: 0 8px 22px rgba(0,0,0,0.15);
        min-height: 68px;
        margin-bottom: 0.22rem;
    }

    .status-dot {
        width: 15px;
        height: 15px;
        border-radius: 50%;
        flex-shrink: 0;
    }

    .status-label {
        font-size: 1rem;
        font-weight: 850;
        color: #f4f9ff;
        letter-spacing: 0.02em;
    }

    .panel-box {
        background: linear-gradient(180deg, rgba(16,34,51,0.98), rgba(13,27,41,0.98));
        border: 1px solid var(--border-soft);
        border-radius: 16px;
        padding: 14px 16px;
        color: #edf4fd;
        line-height: 1.55;
        box-shadow: 0 8px 22px rgba(0,0,0,0.14);
    }

    .timeline-card {
        background: linear-gradient(180deg, rgba(19,48,74,0.98), rgba(13,27,41,0.98));
        border: 1px solid rgba(180,205,230,0.10);
        border-radius: 14px;
        padding: 10px 12px;
        margin-bottom: 7px;
    }

    .timeline-time {
        font-size: 0.76rem;
        color: #8fb0d2;
        margin-bottom: 2px;
    }

    .timeline-state {
        font-size: 0.93rem;
        font-weight: 800;
        color: #edf5ff;
        margin-bottom: 2px;
    }

    .timeline-reason {
        font-size: 0.84rem;
        color: #c1d3e5;
        line-height: 1.32;
    }

    .alert-box {
        border-radius: 14px;
        padding: 11px 13px;
        margin-bottom: 8px;
        font-weight: 600;
        line-height: 1.45;
    }

    .alert-info {
        background: rgba(47,128,237,0.12);
        border: 1px solid rgba(47,128,237,0.24);
        color: #d9ebff;
    }

    .alert-warn {
        background: rgba(215,165,60,0.14);
        border: 1px solid rgba(215,165,60,0.26);
        color: #ffeab8;
    }

    .alert-danger {
        background: rgba(216,79,104,0.14);
        border: 1px solid rgba(216,79,104,0.26);
        color: #ffd8e1;
    }

    .footer-note {
        color: #87a6c4;
        font-size: 0.84rem;
        text-align: center;
        margin-top: 8px;
        margin-bottom: 0.2rem;
    }

    div[data-testid="stTabs"] button {
        font-weight: 750;
    }

    .tight-hr {
        margin-top: 0.35rem;
        margin-bottom: 0.6rem;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# =========================================================
# CONFIG
# =========================================================
APP_SUBTITLE = "Clinical supervision console for autonomous bedside assessment"

DEFAULT_N8N_WEBHOOK = "http://localhost:5678/webhook/mission_ingest_and_agent_summary"

DEFAULT_RUNTIME_DIR = Path(
    "/Users/hosseinkhodamoradi/Downloads/robomed/MedRob_project/controllers/unified_controller_V2/runtime"
)

DEFAULT_EXPORTS_DIR = DEFAULT_RUNTIME_DIR / "exports"
DEFAULT_LOGS_DIR = DEFAULT_RUNTIME_DIR / "logs"
DEFAULT_SNAPSHOTS_DIR = DEFAULT_RUNTIME_DIR / "snapshots"

MISSION_JSON_NAME = "mission_case.json"
AI_INSPECTION_JSON_NAME = "ai_inspection.json"


# =========================================================
# HELPERS
# =========================================================
def load_json_file(path: Path) -> Optional[Dict[str, Any]]:
    if not path.exists():
        return None
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return None


def load_latest_json(directory: Path) -> Optional[Dict[str, Any]]:
    if not directory.exists():
        return None
    files = sorted(directory.glob("*.json"), key=lambda p: p.stat().st_mtime, reverse=True)
    for f in files:
        data = load_json_file(f)
        if data is not None:
            data["_source_file"] = str(f)
            return data
    return None


def latest_matching_file(directory: Path, patterns: List[str]) -> Optional[Path]:
    if not directory.exists():
        return None
    matches: List[Path] = []
    for pattern in patterns:
        matches.extend(list(directory.glob(pattern)))
    if not matches:
        return None
    return sorted(matches, key=lambda p: p.stat().st_mtime, reverse=True)[0]


def first_non_none(*values):
    for v in values:
        if v is not None:
            return v
    return None


def safe_str(value: Any, fallback: str = "") -> str:
    if value is None:
        return fallback
    return str(value)


def coerce_bool(value: Any, default: bool = False) -> bool:
    if isinstance(value, bool):
        return value
    if isinstance(value, (int, float)):
        return bool(value)
    if isinstance(value, str):
        v = value.strip().lower()
        if v in {"true", "1", "yes", "y", "ok", "success", "completed", "done", "found", "detected", "emergency"}:
            return True
        if v in {"false", "0", "no", "n", "fail", "failed", "missing", "not_found", "normal"}:
            return False
    return default


def pretty_time(ts: Any) -> str:
    try:
        return f"{float(ts):.1f}s"
    except Exception:
        return str(ts)


def shorten_text(text: str, max_len: int = 110) -> str:
    if len(text) <= max_len:
        return text
    return text[: max_len - 3] + "..."


def get_nested(data: Any, *keys, default=None):
    cur = data
    for key in keys:
        if isinstance(cur, dict) and key in cur:
            cur = cur[key]
        else:
            return default
    return cur


def find_value_by_keys(data: Any, candidate_keys: List[str]) -> Any:
    if isinstance(data, dict):
        for k, v in data.items():
            if k in candidate_keys:
                return v
        for _, v in data.items():
            found = find_value_by_keys(v, candidate_keys)
            if found is not None:
                return found
    elif isinstance(data, list):
        for item in data:
            found = find_value_by_keys(item, candidate_keys)
            if found is not None:
                return found
    return None


# =========================================================
# LOG PARSING
# =========================================================
STATE_LINE_PATTERNS = [
    re.compile(
        r'(?P<time>\d+(?:\.\d+)?)\s*[:\-]?\s*(?P<from>[A-Z_]+)\s*[-=]>\s*(?P<to>[A-Z_]+)(?:.*?reason[:=]\s*(?P<reason>.*))?',
        re.IGNORECASE,
    ),
    re.compile(
        r'\[(?P<time>\d+(?:\.\d+)?)\]\s*\[(?P<to>[A-Z_]+)\]\s*(?P<reason>.*)',
        re.IGNORECASE,
    ),
]

EMERGENCY_PATTERNS = [
    re.compile(r'\bemergency\b', re.IGNORECASE),
    re.compile(r'\bcode red\b', re.IGNORECASE),
    re.compile(r'\bcritical\b', re.IGNORECASE),
    re.compile(r'\bescalation required\b', re.IGNORECASE),
    re.compile(r'\boperator intervention\b', re.IGNORECASE),
]


def parse_states_from_log(log_text: str) -> List[Dict[str, Any]]:
    states: List[Dict[str, Any]] = []
    last_state = ""

    for line in log_text.splitlines():
        stripped = line.strip()
        if not stripped:
            continue

        for pattern in STATE_LINE_PATTERNS:
            m = pattern.search(stripped)
            if not m:
                continue

            gd = m.groupdict()
            t = gd.get("time", "")
            from_state = gd.get("from", last_state)
            to_state = gd.get("to", "")
            reason = (gd.get("reason") or "").strip()

            if to_state:
                states.append(
                    {
                        "time": t,
                        "from": from_state or "",
                        "to": to_state,
                        "reason": reason or "Parsed from robot log",
                    }
                )
                last_state = to_state
                break

    return states


def parse_emergency_from_log(log_text: str) -> Tuple[bool, List[str]]:
    findings = []
    for line in log_text.splitlines():
        for pat in EMERGENCY_PATTERNS:
            if pat.search(line):
                findings.append(line.strip())
                break
    return len(findings) > 0, findings[:8]


def sanitize_log_line(line: str) -> str:
    raw = line.strip()

    if "monitor_case.json" in raw and "emergency" in raw.lower():
        return "Emergency monitoring case file generated."
    if "monitor_case.json" in raw:
        return "Monitoring case file generated."
    if "loaded demo case=emergency" in raw.lower():
        return "Emergency patient scenario loaded."
    if "loaded demo case=normal" in raw.lower():
        return "Normal patient scenario loaded."
    if "patient" in raw.lower() and "loaded" in raw.lower():
        return "Patient case loaded."
    if "emergency" in raw.lower():
        return "Emergency condition detected in robot diagnostics."
    if "critical" in raw.lower():
        return "Critical diagnostic condition detected."
    if "monitor" in raw.lower() and "found" in raw.lower():
        return "Clinical check data acquired."
    if "patient" in raw.lower() and "found" in raw.lower():
        return "Patient detected by robot."

    cleaned = re.sub(r"/[A-Za-z0-9_\-./]+", "[hidden path]", raw)
    return shorten_text(cleaned, 120)


# =========================================================
# MISSION JSON NORMALIZATION
# =========================================================
def extract_states_from_json(data: Dict[str, Any]) -> List[Dict[str, Any]]:
    candidates = [
        find_value_by_keys(data, ["states"]),
        find_value_by_keys(data, ["timeline"]),
        find_value_by_keys(data, ["state_history"]),
        find_value_by_keys(data, ["transitions"]),
        get_nested(data, "mission", "states"),
        get_nested(data, "mission", "timeline"),
    ]

    raw = first_non_none(*candidates, [])
    out: List[Dict[str, Any]] = []

    if not isinstance(raw, list):
        return out

    for item in raw:
        if not isinstance(item, dict):
            continue

        out.append(
            {
                "time": first_non_none(item.get("time"), item.get("t"), item.get("timestamp"), item.get("mission_time"), ""),
                "from": first_non_none(item.get("from"), item.get("from_state"), item.get("previous"), item.get("src"), ""),
                "to": first_non_none(item.get("to"), item.get("to_state"), item.get("state"), item.get("dst"), ""),
                "reason": first_non_none(item.get("reason"), item.get("message"), item.get("event"), item.get("detail"), ""),
            }
        )

    return out


def extract_emergency_info(data: Dict[str, Any]) -> Tuple[bool, str, List[str]]:
    emergency_value = first_non_none(
        find_value_by_keys(data, ["emergency"]),
        find_value_by_keys(data, ["is_emergency"]),
        find_value_by_keys(data, ["emergency_case"]),
        find_value_by_keys(data, ["critical_case"]),
        find_value_by_keys(data, ["red_flag"]),
        find_value_by_keys(data, ["case"]),
        get_nested(data, "assessment", "emergency"),
        get_nested(data, "agent_result", "emergency"),
        get_nested(data, "patient_assessment", "emergency"),
    )

    emergency_reason = safe_str(
        first_non_none(
            find_value_by_keys(data, ["emergency_reason"]),
            find_value_by_keys(data, ["critical_reason"]),
            find_value_by_keys(data, ["alert_reason"]),
            get_nested(data, "assessment", "emergency_reason"),
            get_nested(data, "patient_assessment", "emergency_reason"),
        ),
        "",
    )

    alerts = first_non_none(
        find_value_by_keys(data, ["alerts"]),
        find_value_by_keys(data, ["warnings"]),
        get_nested(data, "assessment", "alerts"),
        [],
    )
    if not isinstance(alerts, list):
        alerts = [safe_str(alerts)]

    case_value = emergency_value
    if isinstance(case_value, str) and case_value.strip().lower() == "emergency":
        emergency_value = True

    return coerce_bool(emergency_value, default=False), emergency_reason, [safe_str(a) for a in alerts if a is not None]


def normalize_mission_summary(data: Dict[str, Any], log_text: str = "") -> Dict[str, Any]:
    states = extract_states_from_json(data)
    if not states and log_text:
        states = parse_states_from_log(log_text)

    emergency_case, emergency_reason, alerts = extract_emergency_info(data)

    mission_result = safe_str(
        first_non_none(
            find_value_by_keys(data, ["result"]),
            find_value_by_keys(data, ["mission_result"]),
            find_value_by_keys(data, ["status"]),
            get_nested(data, "mission", "result"),
            get_nested(data, "mission", "status"),
            "UNKNOWN",
        ),
        "UNKNOWN",
    ).upper()

    bed_label = first_non_none(
        find_value_by_keys(data, ["bed_label"]),
        find_value_by_keys(data, ["bed_id"]),
        find_value_by_keys(data, ["bed_name"]),
        get_nested(data, "patient", "bed_label"),
        get_nested(data, "mission", "bed_label"),
    )

    patient_identifier = first_non_none(
        find_value_by_keys(data, ["patient_identifier"]),
        find_value_by_keys(data, ["patient_id"]),
        find_value_by_keys(data, ["qr_patient_id"]),
        get_nested(data, "patient", "identifier"),
        get_nested(data, "patient", "id"),
    )

    qr_payload = first_non_none(
        find_value_by_keys(data, ["qr_payload"]),
        find_value_by_keys(data, ["qr_data"]),
        find_value_by_keys(data, ["qr_text"]),
        get_nested(data, "qr", "payload"),
        get_nested(data, "patient", "qr_payload"),
    )

    patient_found = coerce_bool(
        first_non_none(
            find_value_by_keys(data, ["patient_found"]),
            find_value_by_keys(data, ["target_found"]),
            find_value_by_keys(data, ["patient_detected"]),
            get_nested(data, "mission", "patient_found"),
            False,
        )
    )

    patient_centered = coerce_bool(
        first_non_none(
            find_value_by_keys(data, ["patient_centered"]),
            find_value_by_keys(data, ["target_centered"]),
            get_nested(data, "mission", "patient_centered"),
            False,
        )
    )

    approach_done = coerce_bool(
        first_non_none(
            find_value_by_keys(data, ["approach_done"]),
            find_value_by_keys(data, ["approach_completed"]),
            find_value_by_keys(data, ["bedside_reached"]),
            get_nested(data, "mission", "approach_done"),
            False,
        )
    )

    clinical_check_done = coerce_bool(
        first_non_none(
            find_value_by_keys(data, ["clinical_check_done"]),
            find_value_by_keys(data, ["monitor_found"]),
            find_value_by_keys(data, ["vitals_monitor_found"]),
            find_value_by_keys(data, ["screen_found"]),
            get_nested(data, "mission", "monitor_found"),
            False,
        )
    )

    return {
        "run_id": safe_str(
            first_non_none(
                find_value_by_keys(data, ["run_id"]),
                find_value_by_keys(data, ["mission_id"]),
                get_nested(data, "mission", "run_id"),
                get_nested(data, "mission", "id"),
                "mission_unknown",
            )
        ),
        "start_time": safe_str(first_non_none(find_value_by_keys(data, ["start_time"]), get_nested(data, "mission", "start_time"), "")),
        "end_time": safe_str(first_non_none(find_value_by_keys(data, ["end_time"]), get_nested(data, "mission", "end_time"), "")),
        "result": mission_result,
        "patient_found": patient_found,
        "patient_centered": patient_centered,
        "approach_done": approach_done,
        "bed_label": safe_str(bed_label, "UNKNOWN"),
        "patient_identifier": safe_str(patient_identifier, "Not available"),
        "qr_payload": safe_str(qr_payload, "Not available"),
        "clinical_check_done": clinical_check_done,
        "monitor_snapshot": safe_str(
            first_non_none(
                find_value_by_keys(data, ["monitor_snapshot"]),
                find_value_by_keys(data, ["monitor_image"]),
                find_value_by_keys(data, ["screen_snapshot"]),
                "",
            )
        ),
        "full_snapshot": safe_str(
            first_non_none(
                find_value_by_keys(data, ["full_snapshot"]),
                find_value_by_keys(data, ["room_snapshot"]),
                find_value_by_keys(data, ["camera_snapshot"]),
                "",
            )
        ),
        "states": states,
        "notes": alerts,
        "emergency_case": emergency_case,
        "emergency_reason": emergency_reason,
    }


def build_mock_summary() -> Dict[str, Any]:
    now = datetime.now().isoformat()
    return {
        "run_id": "mission_demo_001",
        "start_time": now,
        "end_time": now,
        "result": "SUCCESS",
        "patient_found": True,
        "patient_centered": True,
        "approach_done": True,
        "bed_label": "BED 1",
        "patient_identifier": "P-10294",
        "qr_payload": "P-10294|BED 1|NORMAL",
        "clinical_check_done": True,
        "monitor_snapshot": None,
        "full_snapshot": None,
        "states": [
            {"time": 1.2, "from": "INIT", "to": "ENTER_ROOM", "reason": "Mission started"},
            {"time": 8.4, "from": "ENTER_ROOM", "to": "FIND_PATIENT", "reason": "Patient search active"},
            {"time": 16.1, "from": "FIND_PATIENT", "to": "APPROACH_PATIENT", "reason": "Patient located"},
            {"time": 24.7, "from": "APPROACH_PATIENT", "to": "CLINICAL_CHECK", "reason": "Bedside position reached"},
            {"time": 31.8, "from": "CLINICAL_CHECK", "to": "DONE", "reason": "Clinical check completed"},
        ],
        "notes": [],
        "emergency_case": False,
        "emergency_reason": "",
    }


# =========================================================
# AI INSPECTION JSON
# =========================================================
def load_ai_inspection(exports_dir: Path) -> Optional[Dict[str, Any]]:
    ai_file = exports_dir / AI_INSPECTION_JSON_NAME
    data = load_json_file(ai_file)
    if data is not None:
        data["_source_file"] = str(ai_file)
    return data


def build_local_ai_analysis(summary: Dict[str, Any]) -> Dict[str, Any]:
    emergency_case = coerce_bool(summary.get("emergency_case"))
    patient_found = coerce_bool(summary.get("patient_found"))
    clinical_check_done = coerce_bool(summary.get("clinical_check_done"))
    approach_done = coerce_bool(summary.get("approach_done"))
    result = safe_str(summary.get("result", "UNKNOWN"), "UNKNOWN").upper()
    emergency_reason = safe_str(summary.get("emergency_reason", ""), "")

    risk_level = "Low"
    confidence = 0.62
    assessment = "Mission completed without clinically significant alerts."
    recommendation = "No immediate clinical action required."
    explainability = [
        "Patient was detected by the robot.",
        "Clinical bedside check was completed.",
        "Mission result indicates successful completion.",
    ]
    alerts: List[str] = []

    if not patient_found:
        risk_level = "High"
        confidence = 0.88
        assessment = "The robot did not confirm the patient at bedside."
        recommendation = "Human verification required."
        explainability = [
            "Patient detection flag is negative.",
            "Mission requires manual confirmation at bedside.",
        ]
        alerts = ["Patient could not be confirmed by the robot."]

    elif patient_found and not approach_done:
        risk_level = "Moderate"
        confidence = 0.74
        assessment = "The patient was identified, but bedside positioning may be incomplete."
        recommendation = "Review robot approach and confirm patient status."
        explainability = [
            "Patient was detected.",
            "Approach completion was not confirmed.",
        ]
        alerts = ["Patient detected, but bedside approach was incomplete."]

    elif patient_found and not clinical_check_done:
        risk_level = "High"
        confidence = 0.84
        assessment = "The patient was detected, but the clinical bedside check was not confirmed."
        recommendation = "Verify patient status and clinical evidence."
        explainability = [
            "Patient was detected.",
            "Clinical check completion flag is negative.",
        ]
        alerts = ["Clinical check was not fully completed."]

    if result not in {"SUCCESS", "DONE", "COMPLETED"}:
        risk_level = "High"
        confidence = max(confidence, 0.86)
        assessment = f"Mission completed with non-success status: {result}."
        recommendation = "Clinical staff should review the mission outcome before acting on it."
        explainability.append(f"Mission status was reported as {result}.")
        alerts.append(f"Mission status is {result}.")

    if emergency_case:
        risk_level = "Critical"
        confidence = 0.93
        assessment = "Possible emergency condition detected."
        recommendation = "Immediate human assessment required."
        explainability = [
            "Emergency flag is present in mission data.",
            "The case requires escalation to clinical staff.",
        ]
        if emergency_reason:
            explainability.append(f"Emergency reason: {emergency_reason}")
        alerts = ["Possible emergency condition detected.", "Immediate human intervention required."]

    return {
        "available": True,
        "assessment": assessment,
        "risk_level": risk_level,
        "recommendation": recommendation,
        "confidence": confidence,
        "summary": assessment,
        "explainability": explainability,
        "alerts": alerts,
    }


# =========================================================
# AGENT / INTERPRETATION
# =========================================================
def normalize_states(states: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    out = []
    for s in states or []:
        out.append(
            {
                "time": s.get("time", ""),
                "from": s.get("from", ""),
                "to": s.get("to", ""),
                "reason": s.get("reason", ""),
            }
        )
    return out


def build_payload_from_summary(summary: Dict[str, Any], log_text: str) -> Dict[str, Any]:
    return {
        "run_id": summary.get("run_id"),
        "result": summary.get("result"),
        "patient_found": summary.get("patient_found"),
        "patient_centered": summary.get("patient_centered"),
        "approach_done": summary.get("approach_done"),
        "bed_label": summary.get("bed_label"),
        "patient_identifier": summary.get("patient_identifier"),
        "qr_payload": summary.get("qr_payload"),
        "clinical_check_done": summary.get("clinical_check_done"),
        "full_snapshot": summary.get("full_snapshot"),
        "monitor_snapshot": summary.get("monitor_snapshot"),
        "states": normalize_states(summary.get("states", [])),
        "notes": summary.get("notes", []),
        "emergency_case": summary.get("emergency_case", False),
        "emergency_reason": summary.get("emergency_reason", ""),
        "log_text": log_text,
    }


def default_agent_response(summary: Dict[str, Any], log_text: str = "", ai_inspection: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    result = safe_str(summary.get("result", "UNKNOWN"), "UNKNOWN").upper()
    bed_label = safe_str(summary.get("bed_label", "UNKNOWN"), "UNKNOWN")
    patient_found = coerce_bool(summary.get("patient_found"))
    clinical_check_done = coerce_bool(summary.get("clinical_check_done"))
    approach_done = coerce_bool(summary.get("approach_done"))
    emergency_case = coerce_bool(summary.get("emergency_case"))
    emergency_reason = safe_str(summary.get("emergency_reason", ""), "")

    log_emergency, log_emergency_lines = parse_emergency_from_log(log_text) if log_text else (False, [])
    actual_emergency = emergency_case or log_emergency

    human_review_required = False
    status_light = "green"
    anomalies: List[str] = []

    if actual_emergency:
        status_light = "red"
        human_review_required = True
        anomalies.append("Possible emergency condition detected.")
        if emergency_reason:
            anomalies.append(f"Clinical reason: {emergency_reason}")
        for item in log_emergency_lines[:2]:
            anomalies.append(sanitize_log_line(item))

    if not patient_found:
        anomalies.append("Patient could not be confirmed by the robot.")
        status_light = "red"
        human_review_required = True

    if patient_found and not approach_done:
        anomalies.append("Patient detected, but bedside approach was not fully confirmed.")
        if status_light != "red":
            status_light = "yellow"
        human_review_required = True

    if patient_found and not clinical_check_done:
        anomalies.append("Clinical bedside check was not fully completed.")
        if status_light != "red":
            status_light = "yellow"
        human_review_required = True

    if result not in {"SUCCESS", "DONE", "COMPLETED"}:
        anomalies.append(f"Mission completed with status {result}.")
        status_light = "red"
        human_review_required = True

    if not anomalies:
        operator_summary = (
            f"The robot completed the bedside mission successfully. "
            f"The patient was located, approached safely, bed assignment {bed_label} was recorded, "
            f"and the clinical check was completed without critical alerts."
        )
    else:
        if actual_emergency:
            operator_summary = (
                "A possible emergency condition was detected. "
                "Immediate human review and direct clinical assessment are required."
            )
        else:
            operator_summary = (
                "The mission contains one or more operational or clinical alerts. "
                "Human review is recommended before accepting the mission outcome."
            )

    progress_items = [
        "Patient detected" if patient_found else "Patient not confirmed",
        "Bedside approach completed" if approach_done else "Bedside approach incomplete",
        f"Bed assignment recorded: {bed_label}" if bed_label else "Bed assignment unavailable",
        "Clinical check completed" if clinical_check_done else "Clinical check incomplete",
        f"Mission result: {result}",
    ]
    if actual_emergency:
        progress_items.insert(0, "Emergency case flag present in mission data")

    if ai_inspection and coerce_bool(ai_inspection.get("available", True), default=True):
        ai_analysis = ai_inspection
    else:
        ai_analysis = build_local_ai_analysis(summary)

    return {
        "status_light": status_light,
        "mission_status": result.lower(),
        "operator_summary": operator_summary,
        "bed_label": bed_label,
        "patient_identifier": safe_str(summary.get("patient_identifier", "Not available yet")),
        "qr_payload": safe_str(summary.get("qr_payload", "Not available yet")),
        "progress_items": progress_items,
        "anomalies": anomalies,
        "human_review_required": human_review_required,
        "emergency_case": actual_emergency,
        "emergency_reason": emergency_reason,
        "ai_analysis": ai_analysis,
        "ai_available": ai_inspection is not None,
    }


def call_n8n(webhook_url: str, payload: Dict[str, Any]) -> Dict[str, Any]:
    response = requests.post(webhook_url, json=payload, timeout=40)
    response.raise_for_status()
    return response.json()


def build_report_json(summary: Dict[str, Any], agent_result: Dict[str, Any]) -> str:
    report = {
        "generated_at": datetime.now().isoformat(),
        "mission_summary": summary,
        "agent_result": agent_result,
    }
    return json.dumps(report, indent=2)


# =========================================================
# FILE ACTIONS
# =========================================================
def open_in_finder(file_path: Optional[str]) -> Tuple[bool, str]:
    if not file_path:
        return False, "No file available."
    p = Path(file_path)
    if not p.exists():
        return False, "File does not exist."
    try:
        subprocess.run(["open", "-R", str(p)], check=False)
        return True, f"Opened {p.name} in Finder."
    except Exception as e:
        return False, f"Could not open Finder: {e}"


# =========================================================
# DATA LOAD
# =========================================================
def load_latest_log_text(logs_dir: Path) -> Tuple[Optional[Path], str]:
    log_path = latest_matching_file(logs_dir, ["*.log", "*.txt"])
    if not log_path or not log_path.exists():
        return None, ""
    try:
        return log_path, log_path.read_text(encoding="utf-8", errors="ignore")
    except Exception:
        return log_path, ""


def load_real_summary(exports_dir: Path, logs_dir: Path) -> Dict[str, Any]:
    preferred_mission = exports_dir / MISSION_JSON_NAME
    raw = load_json_file(preferred_mission)

    if raw is not None:
        raw["_source_file"] = str(preferred_mission)
    else:
        raw = load_latest_json(exports_dir)

    log_path, log_text = load_latest_log_text(logs_dir)

    if raw is None:
        demo = build_mock_summary()
        demo["_latest_log_file"] = str(log_path) if log_path else None
        demo["_log_text"] = log_text
        return demo

    summary = normalize_mission_summary(raw, log_text=log_text)
    summary["_source_file"] = raw.get("_source_file")
    summary["_latest_log_file"] = str(log_path) if log_path else None
    summary["_log_text"] = log_text
    return summary


# =========================================================
# UI HELPERS
# =========================================================
def render_metric_card(title: str, value: str) -> None:
    st.markdown(
        f"""
        <div class="metric-card">
            <div class="metric-title">{title}</div>
            <div class="metric-value">{value}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_status_bar(color: str, text: str) -> None:
    colors = {
        "green": "#22c55e",
        "red": "#ef4444",
        "yellow": "#f59e0b",
        "gray": "#94a3b8",
        "blue": "#2f80ed",
    }
    c = colors.get(color, "#94a3b8")
    st.markdown(
        f"""
        <div class="status-wrap">
            <div class="status-dot" style="background:{c}; box-shadow:0 0 10px {c};"></div>
            <div class="status-label">{text}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_alert_box(text: str, level: str = "info") -> None:
    cls = {
        "info": "alert-info",
        "warn": "alert-warn",
        "danger": "alert-danger",
    }.get(level, "alert-info")
    st.markdown(f'<div class="alert-box {cls}">{text}</div>', unsafe_allow_html=True)


def build_mission_progress(summary: Dict[str, Any], agent_result: Dict[str, Any]) -> List[Dict[str, str]]:
    items: List[Dict[str, str]] = []
    states = summary.get("states", []) or []

    if states:
        for s in states[:7]:
            t = pretty_time(s.get("time", ""))
            to_state = safe_str(s.get("to", ""), "")
            reason = safe_str(s.get("reason", ""), "")

            nice_state = to_state.replace("_", " ").title()
            if nice_state == "Find Patient":
                nice_state = "Patient search"
            elif nice_state == "Approach Patient":
                nice_state = "Bedside approach"
            elif nice_state == "Clinical Check":
                nice_state = "Clinical check"
            elif nice_state == "Done":
                nice_state = "Mission completed"

            items.append(
                {
                    "time": t,
                    "state": nice_state,
                    "reason": reason or "Mission progress event",
                }
            )

    if not items:
        items = [
            {"time": "-", "state": "Mission started", "reason": "No structured mission progress available."},
            {"time": "-", "state": "Mission result", "reason": safe_str(summary.get("result", "UNKNOWN"))},
        ]

    if agent_result.get("emergency_case"):
        items.append(
            {
                "time": "-",
                "state": "Clinical escalation",
                "reason": "Possible emergency condition detected",
            }
        )

    return items[:8]


# =========================================================
# SIDEBAR
# =========================================================
with st.sidebar:
    st.markdown("## Control Panel")

    data_mode = st.radio(
        "Data source",
        ["Robot runtime folder", "n8n webhook", "Local demo mode"],
        index=0,
    )

    ui_mode = st.radio(
        "Dashboard mode",
        ["Clinical View", "Engineering View"],
        index=0,
    )

    show_vertical_brand = st.checkbox("Show vertical brand strip", value=True)

    webhook_url = st.text_input("n8n webhook URL", value=DEFAULT_N8N_WEBHOOK)
    runtime_dir_str = st.text_input("Robot runtime directory", value=str(DEFAULT_RUNTIME_DIR))

    st.markdown("---")
    refresh_clicked = st.button("Reload mission data", use_container_width=True)
    analyze_clicked = st.button("Run AI mission analysis", type="primary", use_container_width=True)

    st.markdown("---")
    st.caption("RoboMed clinical dashboard")


# =========================================================
# LOAD DATA
# =========================================================
runtime_dir = Path(runtime_dir_str)
exports_dir = runtime_dir / "exports"
logs_dir = runtime_dir / "logs"
snapshots_dir = runtime_dir / "snapshots"

if "mission_summary" not in st.session_state or refresh_clicked:
    if data_mode == "Robot runtime folder":
        mission_summary = load_real_summary(exports_dir, logs_dir)

        latest_full = latest_matching_file(
            snapshots_dir,
            ["full_camera_snapshot.png", "full_snapshot.png", "room_snapshot.png", "*full*.png", "*room*.png"],
        )
        latest_monitor = latest_matching_file(
            snapshots_dir,
            ["tv_crop_full_for_agent.png", "monitor_crop.png", "screen_crop.png", "*monitor*.png", "*crop*.png", "*screen*.png"],
        )

        if latest_full:
            mission_summary["full_snapshot"] = str(latest_full)
        if latest_monitor:
            mission_summary["monitor_snapshot"] = str(latest_monitor)
    else:
        mission_summary = build_mock_summary()
        mission_summary["_latest_log_file"] = None
        mission_summary["_log_text"] = ""

    st.session_state["mission_summary"] = mission_summary

mission_summary = st.session_state["mission_summary"]
log_text = mission_summary.get("_log_text", "")
ai_inspection = load_ai_inspection(exports_dir) if data_mode == "Robot runtime folder" else None
payload = build_payload_from_summary(mission_summary, log_text)

if "agent_result" not in st.session_state or refresh_clicked:
    st.session_state["agent_result"] = default_agent_response(
        mission_summary,
        log_text=log_text,
        ai_inspection=ai_inspection,
    )

if analyze_clicked:
    if data_mode == "n8n webhook":
        try:
            n8n_result = call_n8n(webhook_url, payload)
            st.session_state["agent_result"] = default_agent_response(
                mission_summary,
                log_text=log_text,
                ai_inspection=n8n_result,
            )
            st.sidebar.success("AI mission analysis completed.")
        except Exception as e:
            st.sidebar.error(f"n8n call failed: {e}")
    else:
        st.session_state["agent_result"] = default_agent_response(
            mission_summary,
            log_text=log_text,
            ai_inspection=ai_inspection,
        )
        st.sidebar.success("Mission analysis completed.")

agent_result = st.session_state["agent_result"]

full_snapshot_path = Path(mission_summary["full_snapshot"]) if mission_summary.get("full_snapshot") else None
monitor_snapshot_path = Path(mission_summary["monitor_snapshot"]) if mission_summary.get("monitor_snapshot") else None

# =========================================================
# MAIN LAYOUT
# =========================================================
if show_vertical_brand:
    left_brand, main_area = st.columns([0.42, 6.4], gap="small")
else:
    left_brand, main_area = None, None

if show_vertical_brand and left_brand is not None and main_area is not None:
    with left_brand:
        st.markdown(
            """
            <div class="brand-strip">
                <div>
                    <div class="brand-vertical">RoboMed</div>
                    <div class="brand-vertical-sub">CLINICAL OPS</div>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    container = main_area
else:
    container = st.container()

with container:
    st.markdown(f'<div class="subline">{APP_SUBTITLE}</div>', unsafe_allow_html=True)
    st.markdown("<hr class='tight-hr'>", unsafe_allow_html=True)

    # TOP STATUS
    c1, c2, c3, c4 = st.columns([2.5, 1.3, 1.2, 1.2])

    with c1:
        label_map = {
            "green": "MISSION STATUS: STABLE",
            "yellow": "MISSION STATUS: REVIEW REQUIRED",
            "red": "MISSION STATUS: ESCALATION REQUIRED",
            "gray": "MISSION STATUS: UNKNOWN",
        }
        status_key = agent_result.get("status_light", "gray")
        render_status_bar(status_key, label_map.get(status_key, "MISSION STATUS: UNKNOWN"))

    with c2:
        render_metric_card("Mission ID", safe_str(mission_summary.get("run_id", "N/A")))

    with c3:
        render_metric_card("Mission Result", safe_str(mission_summary.get("result", "N/A")))

    with c4:
        render_metric_card("Emergency", "YES" if agent_result.get("emergency_case") else "NO")

    # SUMMARY
    st.markdown('<div class="section-title">Mission Summary</div>', unsafe_allow_html=True)
    m1, m2, m3, m4, m5 = st.columns(5)
    with m1:
        render_metric_card("Patient Detected", "Yes" if mission_summary.get("patient_found") else "No")
    with m2:
        render_metric_card("Bed Assignment", safe_str(agent_result.get("bed_label", mission_summary.get("bed_label", "N/A"))))
    with m3:
        render_metric_card("Clinical Check Completed", "Yes" if mission_summary.get("clinical_check_done") else "No")
    with m4:
        render_metric_card("Patient ID", safe_str(agent_result.get("patient_identifier", "N/A")))
    with m5:
        render_metric_card("Human Verification", "Required" if agent_result.get("human_review_required") else "Not required")

    if ui_mode == "Clinical View":
        tab_overview, tab_evidence, tab_review = st.tabs(["Overview", "Visual Evidence", "Clinical Review"])
    else:
        tab_overview, tab_evidence, tab_review, tab_logs = st.tabs(["Overview", "Visual Evidence", "Clinical Review", "Engineering"])

    # OVERVIEW
    with tab_overview:
        left, right = st.columns([1.05, 1.0], gap="medium")

        with left:
            st.markdown('<div class="section-title">Clinical Alert Status</div>', unsafe_allow_html=True)

            if agent_result.get("emergency_case"):
                render_status_bar("red", "POSSIBLE EMERGENCY CONDITION DETECTED")
                render_alert_box("Immediate human assessment is required.", "danger")
            elif agent_result.get("human_review_required"):
                render_status_bar("yellow", "HUMAN REVIEW RECOMMENDED")
                render_alert_box("A clinical or operational review should be performed before accepting the mission outcome.", "warn")
            else:
                render_status_bar("green", "NO CRITICAL CLINICAL ALERTS")
                render_alert_box("The mission can be reviewed routinely without urgent escalation.", "info")

            st.markdown('<div class="section-title">AI Clinical Analysis</div>', unsafe_allow_html=True)
            ai = agent_result.get("ai_analysis", {})

            if agent_result.get("ai_available"):
                st.markdown(
                    f"""
                    <div class="panel-box">
                        <div style="font-weight:800; margin-bottom:6px;">Assessment</div>
                        {safe_str(ai.get("assessment", "No AI assessment available."))}<br><br>
                        <div style="font-weight:800; margin-bottom:6px;">Risk Level</div>
                        {safe_str(ai.get("risk_level", "Unknown"))}<br><br>
                        <div style="font-weight:800; margin-bottom:6px;">Recommendation</div>
                        {safe_str(ai.get("recommendation", "No recommendation available."))}<br><br>
                        <div style="font-weight:800; margin-bottom:6px;">Confidence</div>
                        {float(ai.get("confidence", 0.0)):.2f}
                    </div>
                    """,
                    unsafe_allow_html=True,
                )
            else:
                render_alert_box("No AI inspection available.", "info")

        with right:
            st.markdown('<div class="section-title">Mission Progress</div>', unsafe_allow_html=True)
            progress = build_mission_progress(mission_summary, agent_result)
            for item in progress:
                st.markdown(
                    f"""
                    <div class="timeline-card">
                        <div class="timeline-time">{item["time"]}</div>
                        <div class="timeline-state">{item["state"]}</div>
                        <div class="timeline-reason">{item["reason"]}</div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

            st.markdown('<div class="section-title">Robot Explanation</div>', unsafe_allow_html=True)
            explain_lines = ai.get("explainability", []) if agent_result.get("ai_available") else []
            if explain_lines:
                st.markdown('<div class="panel-box">', unsafe_allow_html=True)
                for line in explain_lines:
                    st.markdown(f"- {line}")
                st.markdown("</div>", unsafe_allow_html=True)
            else:
                render_alert_box("No AI explanation available.", "info")

    # VISUAL EVIDENCE
    with tab_evidence:
        ev1, ev2 = st.columns(2, gap="medium")

        with ev1:
            st.markdown('<div class="section-title">Room Camera Snapshot</div>', unsafe_allow_html=True)
            if full_snapshot_path and full_snapshot_path.exists():
                st.image(str(full_snapshot_path), use_container_width=True)
            else:
                render_alert_box("Room snapshot is not available for this mission.", "info")

        with ev2:
            st.markdown('<div class="section-title">Clinical Check Snapshot</div>', unsafe_allow_html=True)
            if monitor_snapshot_path and monitor_snapshot_path.exists():
                st.image(str(monitor_snapshot_path), use_container_width=True)
            else:
                render_alert_box("Clinical check snapshot is not available for this mission.", "info")

        st.markdown('<div class="section-title">Patient and Case Context</div>', unsafe_allow_html=True)
        ctx1, ctx2, ctx3 = st.columns(3)
        with ctx1:
            render_metric_card("Patient ID", safe_str(agent_result.get("patient_identifier", "N/A")))
        with ctx2:
            render_metric_card("QR Payload", safe_str(agent_result.get("qr_payload", "N/A")))
        with ctx3:
            log_name = Path(mission_summary["_latest_log_file"]).name if mission_summary.get("_latest_log_file") else "Not available"
            render_metric_card("Latest Log File", log_name)

    # CLINICAL REVIEW
    with tab_review:
        r1, r2 = st.columns([1.0, 1.15], gap="medium")

        with r1:
            st.markdown('<div class="section-title">Clinical Review Status</div>', unsafe_allow_html=True)

            if agent_result.get("emergency_case"):
                render_status_bar("red", "EMERGENCY REVIEW REQUIRED")
                render_alert_box("Immediate human intervention is required before accepting this mission.", "danger")
            elif agent_result.get("human_review_required"):
                render_status_bar("yellow", "MANUAL REVIEW REQUIRED")
                render_alert_box("A clinician or operator should verify this mission before acceptance.", "warn")
            else:
                render_status_bar("green", "ROUTINE REVIEW")
                render_alert_box("No urgent escalation is currently indicated.", "info")

            st.markdown('<div class="section-title">Clinical Alerts</div>', unsafe_allow_html=True)

            ai_alerts = ai.get("alerts", []) if agent_result.get("ai_available") else []
            if ai_alerts:
                for a in ai_alerts:
                    level = "danger" if ("emergency" in a.lower() or "immediate" in a.lower()) else "warn"
                    render_alert_box(a, level)
            else:
                anomalies = agent_result.get("anomalies", [])
                if anomalies:
                    for a in anomalies:
                        level = "danger" if ("emergency" in a.lower() or "immediate" in a.lower()) else "warn"
                        render_alert_box(a, level)
                else:
                    render_alert_box("No clinical alerts were detected.", "info")

        with r2:
            st.markdown('<div class="section-title">Action Center</div>', unsafe_allow_html=True)
            st.markdown(
                """
                <div class="panel-box">
                    Use these actions to review the mission, inspect evidence, export reports, or open supporting files in Finder.
                </div>
                """,
                unsafe_allow_html=True,
            )

            a1, a2 = st.columns(2)
            with a1:
                report_json = build_report_json(mission_summary, agent_result)
                st.download_button(
                    label="Download Mission Report JSON",
                    data=report_json,
                    file_name=f"{mission_summary.get('run_id', 'mission_report')}.json",
                    mime="application/json",
                    use_container_width=True,
                )
            with a2:
                if mission_summary.get("_latest_log_file") and Path(mission_summary["_latest_log_file"]).exists():
                    log_path = Path(mission_summary["_latest_log_file"])
                    st.download_button(
                        label="Download Latest Robot Log",
                        data=log_path.read_text(encoding="utf-8", errors="ignore"),
                        file_name=log_path.name,
                        mime="text/plain",
                        use_container_width=True,
                    )
                else:
                    st.button("Download Latest Robot Log", disabled=True, use_container_width=True)

            b1, b2, b3 = st.columns(3)
            with b1:
                if st.button("Open Case File", use_container_width=True):
                    ok, msg = open_in_finder(mission_summary.get("_source_file"))
                    (st.success if ok else st.error)(msg)
            with b2:
                if st.button("Open Robot Log", use_container_width=True):
                    ok, msg = open_in_finder(mission_summary.get("_latest_log_file"))
                    (st.success if ok else st.error)(msg)
            with b3:
                ai_source = ai_inspection.get("_source_file") if ai_inspection else None
                if st.button("Open AI Inspection", use_container_width=True):
                    ok, msg = open_in_finder(ai_source)
                    (st.success if ok else st.error)(msg)

            c1, c2 = st.columns(2)
            with c1:
                st.button("Confirm Patient Status", use_container_width=True)
            with c2:
                st.button("Escalate to Nurse Station", use_container_width=True)

    # ENGINEERING
    if ui_mode == "Engineering View":
        with tab_logs:
            st.markdown('<div class="section-title">Engineering Diagnostics</div>', unsafe_allow_html=True)

            box1, box2 = st.columns([1.0, 1.0])

            with box1:
                render_metric_card("Mission JSON", Path(mission_summary["_source_file"]).name if mission_summary.get("_source_file") else "Not available")
                render_metric_card("Robot Log", Path(mission_summary["_latest_log_file"]).name if mission_summary.get("_latest_log_file") else "Not available")
                render_metric_card("AI Inspection", Path(ai_inspection["_source_file"]).name if ai_inspection and ai_inspection.get("_source_file") else "Not available")

            with box2:
                parsed_states = parse_states_from_log(log_text) if log_text else []
                if parsed_states:
                    for s in parsed_states[:10]:
                        st.markdown(
                            f"""
                            <div class="timeline-card">
                                <div class="timeline-time">{pretty_time(s["time"])}</div>
                                <div class="timeline-state">{s["from"]} → {s["to"]}</div>
                                <div class="timeline-reason">{s["reason"]}</div>
                            </div>
                            """,
                            unsafe_allow_html=True,
                        )
                else:
                    render_alert_box("No parseable state transitions were found in the current log.", "info")

            st.markdown('<div class="section-title">Sanitized Diagnostic Log</div>', unsafe_allow_html=True)
            if log_text:
                sanitized_lines = [sanitize_log_line(x) for x in log_text.splitlines() if x.strip()]
                st.code("\n".join(sanitized_lines[-120:]), language="text")
            else:
                render_alert_box("No diagnostic log is available.", "info")

            st.markdown('<div class="section-title">Mission JSON</div>', unsafe_allow_html=True)
            st.json(mission_summary)

            st.markdown('<div class="section-title">AI Inspection JSON</div>', unsafe_allow_html=True)
            if ai_inspection:
                st.json(ai_inspection)
            else:
                render_alert_box("No AI inspection available.", "info")

    st.markdown("<hr class='tight-hr'>", unsafe_allow_html=True)
    st.markdown(
        '<div class="footer-note">RoboMed clinical dashboard • hospital-oriented UI • AI-ready supervision • emergency-aware mission review</div>',
        unsafe_allow_html=True,
    )