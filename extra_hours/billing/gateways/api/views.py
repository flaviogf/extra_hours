from datetime import datetime

from flask import Blueprint, jsonify, request

from extra_hours.billing.commands import CreateBillingCommand


def create_billing_bp(get_create_billing):
    billing_bp = Blueprint('billing', __name__)

    @billing_bp.route('/api/v1/billing', methods=['post'])
    def create_billing_view():
        json = request.get_json()

        work_date = json.get('work_date', None)

        work_date = datetime.strptime(work_date, '%Y-%m-%d') if work_date else datetime.today()

        command = CreateBillingCommand(user_id=json.get('user_id', ''),
                                       title=json.get('title', ''),
                                       description=json.get('description', ''),
                                       value=json.get('value', 0.0),
                                       work_date=work_date)

        create_billing = get_create_billing()

        create_billing.execute(command)

        if not create_billing.is_valid:
            return jsonify([n.message for n in create_billing.notifications]), 400

        return jsonify('billing created'), 201

    return billing_bp
