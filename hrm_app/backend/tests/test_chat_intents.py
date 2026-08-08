"""Pure tests for the chat intent parser + tutor. No DB, no framework."""
from app.domain.services import tutor
from app.domain.services.chat_intents import parse


def test_add_employee():
    i = parse("add employee Rakib rate 22 start 09:00")
    assert i.kind == "add_employee"
    assert i.params["name"] == "Rakib"
    assert i.params["base_rate"] == 22.0
    assert i.params["shift_start"] == "09:00"


def test_edit_employee_rule():
    i = parse("set E101 base rate to 30")
    assert i.kind == "edit_employee"
    assert i.params == {"employee_id": "E101", "field": "base_rate", "value": "30"}


def test_edit_employee_weekend():
    i = parse("set E101 weekend to fri,sat")
    assert i.kind == "edit_employee"
    assert i.params["field"] == "weekend_days"
    assert i.params["value"] == "fri,sat"


def test_insert_attendance():
    i = parse("add attendance E101 2024-06-15 present 09:00 18:00 pay 160")
    assert i.kind == "insert_attendance"
    assert i.params["employee_id"] == "E101"
    assert i.params["day"] == "2024-06-15"
    assert i.params["day_type"] == "present"
    assert i.params["check_in"] == "09:00"
    assert i.params["check_out"] == "18:00"
    assert i.params["reported_pay"] == 160.0


def test_set_pay_is_attendance_edit():
    i = parse("set E101 2024-06-12 pay to 190")
    assert i.kind == "edit_attendance"
    assert i.params["field"] == "reported_pay"
    assert i.params["value"] in ("190", 190.0)


def test_insert_payroll_phrasing():
    i = parse("insert payroll E101 2024-06-12 190")
    assert i.kind == "edit_attendance"
    assert i.params["field"] == "reported_pay"
    assert float(i.params["value"]) == 190.0


def test_edit_attendance_checkout():
    i = parse("set E101 2024-06-12 checkout to 18:00")
    assert i.kind == "edit_attendance"
    assert i.params["field"] == "check_out"
    assert i.params["value"] == "18:00"


def test_delete_needs_confirm():
    i = parse("delete attendance E101 2024-06-12")
    assert i.kind == "delete_attendance" and i.confirm is False
    j = parse("delete attendance E101 2024-06-12 confirm")
    assert j.kind == "delete_attendance" and j.confirm is True


def test_delete_employee():
    i = parse("delete employee E101")
    assert i.kind == "delete_employee" and i.params["employee_id"] == "E101"


def test_label():
    i = parse("E100 2024-06-11 is wrong")
    assert i.kind == "label" and i.params["is_wrong"] is True
    j = parse("mark E100 2024-06-05 correct")
    assert j.kind == "label" and j.params["is_wrong"] is False


def test_train_and_retrain():
    assert parse("train").kind == "train"
    assert parse("train the model").kind == "train"
    assert parse("retrain from my labels").kind == "retrain"


def test_check_month():
    i = parse("check E101 june")
    assert i.kind == "check_month"
    assert i.params == {"employee_id": "E101", "year": 2024, "month": 6}


def test_check_range_last_n_months():
    i = parse("check E100 last two months")
    assert i.kind == "check_range"
    assert i.params == {"employee_id": "E100", "months": 2}
    j = parse("check E100 last 3 months")
    assert j.kind == "check_range" and j.params["months"] == 3


def test_import_data():
    i = parse("import the real biometric data")
    assert i.kind == "import_data"
    assert i.params.get("replace") is not False        # default = replace demo

    j = parse("import real data merge 90 but keep the demo")
    assert j.kind == "import_data"
    assert j.params["merge_seconds"] == 90
    assert j.params["replace"] is False


def test_tutor_and_help():
    assert parse("how does training work?").kind == "tutor"
    assert parse("").kind == "help"
    assert parse("blah blah nonsense").kind == "help"


def test_tutor_answers_have_text():
    assert "TRAINING" in tutor.answer("how does training work?")
    assert "SUPERVISED" in tutor.answer("what is supervised learning?")
    assert "FEATURE" in tutor.answer("what is a feature?")
