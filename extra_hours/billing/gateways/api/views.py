from datetime import datetime

from flask import Blueprint, jsonify, request

from extra_hours.billing.commands import (CreateBillingCommand,
                                          ConfirmReceiveBillingCommand,
                                          CancelReceiveBillingCommand, UpdateBillingCommand)


def create_billing_bp(get_create_billing,
                      get_confirm_receive_billing,
                      get_cancel_receive_billing,
                      get_update_billing):
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

    @billing_bp.route('/api/v1/billing/<uuid:billing_id>/confirm-receive', methods=['post'])
    def confirm_receive_billing_view(billing_id):
        json = request.get_json()

        command = ConfirmReceiveBillingCommand(user_id=json.get('user_id', ''),
                                               billing_id=json.get('billing_id', ''))

        confirm_receive_billing = get_confirm_receive_billing()

        confirm_receive_billing.execute(command)

        if not confirm_receive_billing.is_valid:
            return jsonify([n.message for n in confirm_receive_billing.notifications]), 400

        return jsonify('ok'), 204

    @billing_bp.route('/api/v1/billing/<uuid:billing_id>/cancel-receive', methods=['post'])
    def cancel_receive_billing_view(billing_id):
        json = request.get_json()

        command = CancelReceiveBillingCommand(user_id=json['user_id'],
                                              billing_id=json['billing_id'])

        cancel_receive_billing = get_cancel_receive_billing()

        cancel_receive_billing.execute(command)

        if not cancel_receive_billing.is_valid:
            return jsonify([n.message for n in cancel_receive_billing.notifications]), 400

        return jsonify('ok'), 204

    @billing_bp.route('/api/v1/billing/<uuid:billing_id>', methods=['put'])
    def update_billing_view(billing_id):
        json = request.get_json()

        work_date = json.get('work_date', None)

        work_date = datetime.strptime(work_date, '%Y-%m-%d') if work_date else datetime.today()

        command = UpdateBillingCommand(user_id=json.get('user_id', ''),
                                       billing_id=json.get('billing_id', ''),
                                       title=json.get('title', ''),
                                       description=json.get('description', ''),
                                       value=json.get('value', 0.0),
                                       work_date=work_date)

        update_billing = get_update_billing()

        update_billing.execute(command)

        if not update_billing.is_valid:
            return jsonify([n.message for n in update_billing.notifications]), 400

        return jsonify('ok'), 204

    return billing_bp
