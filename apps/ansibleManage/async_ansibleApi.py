"""
@author:lijx
@contact: 360595252@qq.com
@site: http://blog.51cto.com/breaklinux
@version: 1.0
"""
import json
import shutil
from ansible.module_utils.common.collections import ImmutableDict
from ansible.parsing.dataloader import DataLoader
from ansible.vars.manager import VariableManager
from ansible.inventory.manager import InventoryManager
from ansible.playbook.play import Play
from ansible.executor.task_queue_manager import TaskQueueManager
from ansible.plugins.callback import CallbackBase
from ansible import context
import ansible.constants as C

class ResultCallback(CallbackBase):
    """
    1.重写callbackBase类的部分方法
    """
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
    #  # type: (object, object, object, object) -> object
    #   # type: (object, object, object, object) -> object
    def __init__(self,connection='smart', remote_user=None, remote_password=None, private_key_file=None,
        sudo=None,sudo_user=None,ask_sudo_pass=None,module_path=None,become=None,become_method=None,
        become_user=None,check=False,diff=False,listhosts=None,listtasks=None,listtags=None,verbosity=3,syntax=None,start_at_task=None,inventory=None):
        context.CLIARGS = ImmutableDict(
            connection=connection,
            remote_user=remote_user,
            private_key_file=private_key_file,
            sudo=sudo,
            sudo_user=sudo_user,
            ask_sudo_pass=ask_sudo_pass,
            module_path=module_path,
            become=become,
            become_method=become_method,
            become_user=become_user,
            verbosity=verbosity,
            listhosts=listhosts,
            listtasks=listtasks,
            listtags=listtags,
            syntax=syntax,
            start_at_task=start_at_task,
        )
        self.passwords = None
        self.inventory = inventory if inventory else "192.168.47.108,"
        # 实例化数据解析器
        self.loader = DataLoader()
        # 实例化 资产配置对象
        self.inv_obj = InventoryManager(loader=self.loader, sources=self.inventory)
        # 设置密码
        # 实例化回调插件对象
        self.results_callback = ResultCallback()
        # 变量管理器
        self.variable_manager = VariableManager(self.loader, self.inv_obj)

    def run(self, host_list, module_name, module_args,task_time=0 ):
        play_source = dict(
            name="Ad-hoc",
            hosts=host_list,
            gather_facts='no',
            tasks=[
       ###统一返回####
       # dict(action=dict(module=module_name, args=module_args),"async": task_time, "poll": 0})]
       #   dict(action=dict(module=module_name,args=module_args,async=task_time,poll=0))]
        {"action": {"module": module_name, "args": module_args}, "async": task_time, "poll": 0}])

        #dict(action=dict(module=module_name, args=module_args))]

        play = Play().load(play_source,variable_manager=self.variable_manager, loader=self.loader)
        print("执行play",play)
        tqm = None
        self.callback = ResultCallback()
        try:
            tqm = TaskQueueManager(
                inventory=self.inv_obj,
                variable_manager=self.variable_manager,
                loader=self.loader,
                passwords=self.passwords,
                stdout_callback=self.results_callback,
            )
            #tqm._stdout_callback = self.callback
            # 使用回调函数
            result = tqm.run(play)
            return result

        finally:
            if tqm is not None:
                tqm.cleanup()
            ###########ansible task Remove ansible tmpdir
            shutil.rmtree(C.DEFAULT_LOCAL_TMP, True)

    def playbookRun(self, playbook_path):
        from ansible.executor.playbook_executor import PlaybookExecutor

        playbook = PlaybookExecutor(playbooks=playbook_path,
                                    inventory=self.inv_obj,
                                    variable_manager=self.variable_manager,
                                    loader=self.loader,
                                    passwords=self.passwords)

        playbook._tqm._stdout_callback = self.results_callback
        result = playbook.run()
        return result

    def get_result(self):
      result_raw = {'success':{},'failed':{},'unreachable':{}}
      # print(self.results_callback.host_ok)
      for host,result in self.results_callback.host_ok.items():
          result_raw['success'][host] = result._result
      for host,result in self.results_callback.host_failed.items():
          result_raw['failed'][host] = result._result
      for host,result in self.results_callback.host_unreachable.items():
          result_raw['unreachable'][host] = result._result
      return result_raw

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
    print("Ansible Api Ansible Version: 2.8.0  Test Ok")
