from marshmallow import Schema, fields, validates, validate, ValidationError


class BandPaymentsSchema(Schema):
    id = fields.UUID(
        validate=validate.Length(
            min=36, max=36, error="String must be 36 chars"
        )
    )
    contract_id = fields.UUID(
        validate=validate.Length(
            min=36, max=36, error="String must be 36 chars"
        )
    )
    contributor = fields.String(
        validate=validate.Length(min=1, error="String too short")
    )
    date = fields.DateTime()
    amount = fields.Float()

    @validates("amount")
    def validate_amount(self, amount):
        if not float(amount):
            raise ValidationError(
                "Amount have wrong format. Only whole numbers."
            )
