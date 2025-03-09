# -*- coding: utf-8 -*-
from marshmallow import Schema, fields


class ExternalLibrarySchema(Schema):
    library_id = fields.Str(required=True)
    name = fields.Str(required=True)
    available = fields.Bool(required=True)
    details = fields.Dict(required=False)


class BookStatusResponseSchema(Schema):
    book_id = fields.Int(required=True)
    external_libraries = fields.List(
        fields.Nested(ExternalLibrarySchema), required=True
    )


class BookStatusUpdateSchema(Schema):
    external_status = fields.List(fields.Dict(), required=True)
    last_checked = fields.Str(required=True)


class ReservationRequestSchema(Schema):
    book_id = fields.Int(required=True)
    user_data = fields.Dict(required=False)


class ReservationResponseSchema(Schema):
    reservation_id = fields.Str(required=True)
    status = fields.Str(required=True)
    library_id = fields.Str(required=True)
    details = fields.Dict(required=False)


class ErrorResponseSchema(Schema):
    error = fields.Str(required=True)
