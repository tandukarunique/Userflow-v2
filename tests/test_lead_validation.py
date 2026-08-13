import pytest


import pytest


def test_empty_lead_is_not_submitted(lead_form):
    """Required-field validation should prevent an empty lead submission."""
    lead_form.submit_lead()

    fields = lead_form.text_fields()
    assert any(
        field.evaluate("element => !element.checkValidity()")
        for field in fields.values()
    ), "The empty form was accepted without browser validation."


@pytest.mark.parametrize("field_name", ["name", "location", "referred_by", "interest_area", "notes"])
def test_massive_text_is_handled(lead_form, field_name):
    """Text fields should handle a large value without a Playwright error."""
    value = "A" * 10_000
    field = lead_form.text_fields()[field_name]
    field.fill(value)
    assert field.input_value() == value


@pytest.mark.parametrize(
    "field_name,value",
    [
        ("name", "O'Reilly <QA> & Co."),
        ("location", "東京 / São Paulo / München"),
        ("notes", "emoji ✅ newline\nsecond line"),
    ],
)
def test_special_characters_are_preserved(lead_form, field_name, value):
    field = lead_form.text_fields()[field_name]
    field.fill(value)
    assert field.input_value() == value