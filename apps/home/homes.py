from apps.account.models import User
from apps.ansibleManage.models import bmc_ansible_hosts
#from apps.schedule.models import Job
from apps.appManager.models import Appmg
from flask import Blueprint
from libs.decorators import require_permission
from libs.tools import json_response


blueprint = Blueprint(__name__, __name__)


@blueprint.route('/', methods=['GET'])
@require_permission('home_view')
def get():
    user_total = User.query.count()
    host_total = bmc_ansible_hosts.query.count()
    app_total = Appmg.query.count()
    print(host_total)

    data = {'user_total': user_total,
            'host_total': host_total,
            'app_total': app_total,
            }
    return json_response(data)
