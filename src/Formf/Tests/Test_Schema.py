import json

from Formf.Core.Form import Form
from Formf.fields.String import String
from Formf.fields.Integer import Integer
from Formf.fields.Float import Float
from Formf.fields.Bool import Bool
from Formf.fields.Date import Date
from Formf.fields.List import List
from Formf.crossfieldvalidators import Equals


def test_form_to_schema_exports_fields_validators_and_crossfieldvalidators():
    class RegisterForm(Form):
        status = String(required=False)
        email = String(requiredif=("status", "approved"), minlength=5)
        age = Integer(requiredif=lambda form: form.data.get("email") is not None, minvalue=18)
        password = String(minlength=8)
        password_repeat = String(minlength=8)
        crossfield_validators = [Equals("password", "password_repeat")]

    schema = RegisterForm({}).to_schema()

    assert schema["form"] == "RegisterForm"
    assert schema["version"] == "1.0"
    assert "fields" in schema
    assert "crossfield_validators" in schema
    assert schema["errors_schema"]["form_error_key"] == "__all__"

    email_schema = schema["fields"]["email"]
    assert email_schema["type"] == "string"
    assert email_schema["requiredif"]["type"] == "tuple"
    assert email_schema["requiredif"]["field"] == "status"
    assert email_schema["requiredif"]["expected"] == "approved"
    assert any(v["name"] == "MinLength" for v in email_schema["validators"])

    age_schema = schema["fields"]["age"]
    assert age_schema["requiredif"]["type"] == "callable"
    assert age_schema["requiredif"]["exportable"] is False

    assert schema["crossfield_validators"][0]["name"] == "Equals"
    assert schema["crossfield_validators"][0]["params"]["field1"] == "password"
    assert schema["crossfield_validators"][0]["params"]["field2"] == "password_repeat"


def test_form_schema_is_json_serializable():
    class DemoForm(Form):
        name = String(requiredif={"field": "status", "not_empty": True})
        status = String(required=False)

    schema = DemoForm({}).to_schema()
    encoded = json.dumps(schema)
    assert isinstance(encoded, str)


def test_list_item_field_is_exported_in_schema():
    class ItemFieldForm(Form):
        tags = List(inlist=False, item_field="string")
        options = List(inlist=False, item_field={"component": "tag-input", "max_items": 5})

    schema = ItemFieldForm({}).to_schema()
    assert schema["fields"]["tags"]["item_field"] == "string"
    assert schema["fields"]["options"]["item_field"]["component"] == "tag-input"


def test_list_item_field_can_embed_field_schema():
    class NestedItemForm(Form):
        tags = List(listvalues=None, item_field=String(minlength=2))

    schema = NestedItemForm({}).to_schema()
    nested = schema["fields"]["tags"]["item_field"]
    assert nested["type"] == "string"
    assert any(v["name"] == "MinLength" for v in nested["validators"])


def test_list_membership_schema_uses_single_list_config():
    class MembershipForm(Form):
        allowed = List(listvalues=["a", "b"], must_be_in=True)
        blocked = List(listvalues=["x", "y"], must_be_in=False)

    schema = MembershipForm({}).to_schema()
    assert schema["fields"]["allowed"]["listvalues"] == ["a", "b"]
    assert schema["fields"]["allowed"]["must_be_in"] is True
    assert schema["fields"]["blocked"]["listvalues"] == ["x", "y"]
    assert schema["fields"]["blocked"]["must_be_in"] is False


def test_field_specific_schema_keys_are_exported():
    class FieldConfigForm(Form):
        title = String(strict=True, minlength=2, maxlength=10)
        age = Integer(strict=True, minvalue=18, maxvalue=120)
        score = Float(strict=True, minvalue=0.0, maxvalue=5.0)
        accepted = Bool(strict=True, value=True)
        published = Date(strict=True, dateformat="YYYY-MM-DD", before="2030-01-01", after="2020-01-01")

    schema = FieldConfigForm({}).to_schema()

    assert schema["fields"]["title"]["strict"] is True
    assert schema["fields"]["title"]["minlength"] == 2
    assert schema["fields"]["title"]["maxlength"] == 10

    assert schema["fields"]["age"]["strict"] is True
    assert schema["fields"]["age"]["minvalue"] == 18
    assert schema["fields"]["age"]["maxvalue"] == 120

    assert schema["fields"]["score"]["strict"] is True
    assert schema["fields"]["score"]["minvalue"] == 0.0
    assert schema["fields"]["score"]["maxvalue"] == 5.0

    assert schema["fields"]["accepted"]["strict"] is True
    assert schema["fields"]["accepted"]["value"] is True

    assert schema["fields"]["published"]["strict"] is True
    assert schema["fields"]["published"]["dateformat"] == "YYYY-MM-DD"
    assert schema["fields"]["published"]["before"] == "2030-01-01"
    assert schema["fields"]["published"]["after"] == "2020-01-01"
