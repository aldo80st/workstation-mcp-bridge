"""Deliberate red-test drill; never merge this synthetic failure to production.

Acceptance: CI smoke unit-test step MUST fail when this test is present.
This single test is added only on a disposable PR branch and subsequently
closed; it is not a regression to fix or a reason to touch the pilot.
"""


def test_ci_negative_drill_must_make_workflow_red():
    assert False, "WMB_CI_NEGATIVE_DRILL_EXPECTED_FAILURE"
