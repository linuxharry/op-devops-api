"""
@author:lijx
@contact: 360595252@qq.com
@site: http://blog.51cto.com/breaklinux
@version: 1.0
"""

import json
from collections import namedtuple

from ansible.executor.task_queue_manager import TaskQueueManager
from ansible.inventory.manager import InventoryManager
from ansible.parsing.dataloader import DataLoader
from ansible.playbook.play import Play
from ansible.plugins.callback import CallbackBase
from ansible.vars.manager import VariableManager
from ansible.errors import AnsibleParserError


class ResultCallback(CallbackBase):

    def __init__(self, *args, **kwargs):
        super(ResultCallback, self).__init__(*args, **kwargs)
        self.host_ok = {}
        self.host_unreachable = {}
        self.host_failed = {}

    def v2_runner_on_ok(self, result, **kwargs):
        self.host_ok[result._host.get_name()] = result

        host = result._host
        print(json.dumps({host.name: result._result}, indent=4))

    def v2_runner_on_unreachable(self, result):
        self.host_unreachable[result._host.get_name()] = result

    def v2_runner_on_failed(self, result, *args, **kwargs):
        self.host_failed[result._host.get_name()] = result


class AnsibleApi(object):

    def __init__(self, resource, user, becomeuser, playvars={}, *args, **kwargs):
        # type: (object, object, object, object) -> object
        # type: (object, object, object, object) -> object
        self._resource = resource
        self._user = user
        self._becomeuser = becomeuser
        self.inventory = None
        self.playvars = playvars  # add
        self.variable_manager = None
        self.loader = None
        self.options = None
        self.passwords = None
        self.callback = None
        self.__initializeAnsibleData()
        self.results_raw = {}

    def __initializeAnsibleData(self):

        Options = namedtuple('Options', ['connection', 'module_path', 'forks', 'timeout', 'remote_user',
                                         'ask_pass', 'private_key_file', 'ssh_common_args', 'ssh_extra_args',
                                         'sftp_extra_args',
                                         'scp_extra_args', 'become', 'become_method', 'become_user', 'ask_value_pass',
                                         'verbosity',
                                         'check', 'listhosts', 'listtasks', 'listtags', 'syntax', 'diff'])
        self.options = Options(connection='ssh', module_path=None, forks=100, timeout=5,
                               remote_user=self._user, ask_pass=False, private_key_file=None, ssh_common_args=None,
                               ssh_extra_args=None, sftp_extra_args=None, scp_extra_args=None, become=True,
                               become_method='sudo',
                               become_user=self._becomeuser, ask_value_pass=False, verbosity=None, check=False,
                               listhosts=False,
                               listtasks=False, listtags=False, syntax=False, diff=False)
        self.loader = DataLoader()
        self.passwords = dict(sshpass=None, becomepass=None)
        self.inventory = InventoryManager(loader=self.loader, sources=self._resource)
        # self.variable_manager = VariableManager(loader=self.loader, inventory=self.inventory)

        self.variable_manager = VariableManager(loader=self.loader, inventory=self.inventory)
        self.variable_manager.extra_vars = self.playvars
        # self.variable_manager.set_inventory(self.inventory)  ##add
        # self.variable_manager.extra_vars = self.myvars  ##add

    def run(self, host_list, module_name, module_args, ):
        play_source = dict(
            name="Ansible Play",
            hosts=host_list,
            gather_facts='no',
            tasks=[
                ###统一返回####
                dict(action=dict(module=module_name, args=module_args))]

        )

        play = Play().load(play_source, variable_manager=self.variable_manager, loader=self.loader)

        tqm = None
        self.callback = ResultCallback()
        try:
            tqm = TaskQueueManager(
                inventory=self.inventory,
                variable_manager=self.variable_manager,
                loader=self.loader,
                options=self.options,
                passwords=self.passwords,
                stdout_callback="default",
                # Use our custom callback instead of the ``default`` callback plugin, which prints to stdout
            )
            tqm._stdout_callback = self.callback
            result = tqm.run(play)  # most interesting data for a play is actually sent to the callback's methods
        finally:
            if tqm is not None:
                tqm.cleanup()
            ###########ansible task Remove ansible tmpdir
            # shutil.rmtree(C.DEFAULT_LOCAL_TMP, True)    

    def playbookRun(self, playbook_path):
        from ansible.executor.playbook_executor import PlaybookExecutor

        playbook = PlaybookExecutor(playbooks=playbook_path,
                                    inventory=self.inventory,
                                    variable_manager=self.variable_manager,
                                    loader=self.loader,
                                    options=self.options,
                                    passwords=self.passwords)

        self.callback = ResultCallback()
        playbook._tqm._stdout_callback = self.callback
        try:
            result = playbook.run()
        except AnsibleParserError:
            code = 1001
            results = {'playbook': playbook_path, 'msg': playbook_path + 'playbook have syntax error', 'flag': False}
            return code, results

    def get_result(self):
        self.results_raw = {'success': {}, 'failed': {}, 'unreachable': {}}
        for host, result in self.callback.host_ok.items():
            self.results_raw['success'][host] = result._result

        for host, result in self.callback.host_failed.items():
            self.results_raw['failed'][host] = result._result

        for host, result in self.callback.host_unreachable.items():
            self.results_raw['unreachable'][host] = result._result['msg']

        return self.results_raw


    def get_result_v2(self):
        self.results_raw = {'success': list(), 'failed': list(), 'unreachable': list()}

        for host, result in self.callback.host_ok.items():
            self.results_raw['success'].append({"ip": host, "result": result._result})

        for host, result in self.callback.host_failed.items():
            self.results_raw['failed'].append({"ip": host, "result": result._result})

        for host, result in self.callback.host_unreachable.items():
            self.results_raw['unreachable'].append({"ip": host, "result": result._result['msg']})
        return self.results_raw


if __name__ == "__main__":
    print("Ansible Api Ansible Version: 2.7.5  Test Ok")
