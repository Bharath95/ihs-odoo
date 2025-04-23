from odoo import fields, models


class HelloModel(models.Model):
    _name = "hello.model"
    _description = "Hello Model"

    name = fields.Char(string="Name")
    message = fields.Char(string="Message", default="Hello, World!")
