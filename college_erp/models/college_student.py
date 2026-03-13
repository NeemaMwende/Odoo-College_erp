from odoo import fields,models

class CollegeStudent(models.Model):
    _name = 'college.student'
    _description = 'College Student'

    admission_no = fields.Char(string="Admission Number", required=True)
    admission_date = fields.Date(string="Admission Date", required=True)
    first_name = fields.Char(string="First Name", required=True)
    last_name = fields.Char(string="Last Name", required=True)
    father_name = fields.Char(string="Father's Name", required=True)
    mother_name = fields.Char(string="Mother's Name", required=True)
    contact_address = fields.Text(string="Contact Address", required=True)
    street = fields.Char(string="Street")
    street2 = fields.Char(string="Street 2")
    zip = fields.Char(string="ZIP")
    city = fields.Char(string="City")
    state_id = fields.Many2one(comodel_name='res.country.state', string="State", domain="[('country_id', '=?', country)]")
    country_id = fields.Many2one('res.country', string="Country")
    country_code = fields.Char(string="Country Code", related='country_id.code', store=True)
    email = fields.Char(string="Email")
    phone = fields.Char(string="Phone")
