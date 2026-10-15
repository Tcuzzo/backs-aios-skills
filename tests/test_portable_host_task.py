"""Sanitized real Claude host envelope; route the human task, retain full payload."""
import copy
import importlib.util
from pathlib import Path

POLICY = Path(__file__).resolve().parents[1] / "provider/runtime/typed_routing_policy.py"


def task_text(body):
    spec = importlib.util.spec_from_file_location("portable_shared_policy", POLICY)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.task_text(body)


def test_host_reminder_blocks_do_not_replace_the_current_human_task():
    prompt = "This is a read-only installed host transport proof. Do not edit files or run tools. Reply with exactly PORTABLE_NEEDLE_KEV_OK."
    body = {"messages": [
        {"role": "user", "content": [
            {"type": "text", "text": "<system-reminder>\nHost date and session context.\n</system-reminder>"},
            {"type": "text", "text": "<system-reminder>\nHost skill catalog and execution context.\n</system-reminder>"},
            {"type": "text", "text": prompt},
        ]},
        {"role": "system", "content": [{"type": "text", "text": "Host dynamic system context."}]},
    ]}
    untouched = copy.deepcopy(body)
    assert task_text(body) == prompt
    assert body == untouched


def test_literal_tag_inside_human_text_and_tool_results_preserve_task():
    prompt = "Fix the parser that handles <system-reminder>literal text</system-reminder> in source files."
    body = {"messages": [{"role": "user", "content": prompt},
                         {"role": "assistant", "content": [{"type": "tool_use", "id": "one", "name": "read", "input": {}}]},
                         {"role": "user", "content": [{"type": "tool_result", "tool_use_id": "one", "content": "file output is not a new task"}]}]}
    assert task_text(body) == prompt
