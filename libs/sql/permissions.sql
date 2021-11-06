-- system role
INSERT INTO account_roles (id, name, `desc`) VALUES (1, '系统默认角色', '系统默认角色');

-- Dashboard
INSERT INTO account_permissions (id, name, `desc`) VALUES (100, 'home_view', 'Dashboard');

-- 用户管理 -> 用户列表
INSERT INTO account_permissions (id, name, `desc`) VALUES (101, 'account_user_view', '获取用户列表');
INSERT INTO account_permissions (id, name, `desc`) VALUES (102, 'account_user_add', '添加用户');
INSERT INTO account_permissions (id, name, `desc`) VALUES (103, 'account_user_edit', '编辑用户');
INSERT INTO account_permissions (id, name, `desc`) VALUES (104, 'account_user_del', '删除用户');
INSERT INTO account_permissions (id, name, `desc`) VALUES (105, 'account_user_disable', '禁用用户');

-- 用户管理 -> 角色权限
INSERT INTO account_permissions (id, name, `desc`) VALUES (201, 'account_role_view', '获取角色列表');
INSERT INTO account_permissions (id, name, `desc`) VALUES (202, 'account_role_add', '添加角色');
INSERT INTO account_permissions (id, name, `desc`) VALUES (203, 'account_role_edit', '编辑角色');
INSERT INTO account_permissions (id, name, `desc`) VALUES (204, 'account_role_del', '删除角色');
INSERT INTO account_permissions (id, name, `desc`) VALUES (205, 'account_role_permission_view', '查看角色权限');
INSERT INTO account_permissions (id, name, `desc`) VALUES (206, 'account_role_permission_edit', '修改角色权限');


-- 应用发布 -> 应用列表 -> 发布页面
INSERT INTO account_permissions (id, name, `desc`) VALUES (301, 'publish_app_publish_host_select', '选择发布主机');
INSERT INTO account_permissions (id, name, `desc`) VALUES (302, 'publish_app_publish_menu_exec', '执行自定义菜单');


-- 配置管理 -> 环境管理
INSERT INTO account_permissions (id, name, `desc`) VALUES (401, 'config_environment_view', '获取环境列表');
INSERT INTO account_permissions (id, name, `desc`) VALUES (402, 'config_environment_add', '添加环境');
INSERT INTO account_permissions (id, name, `desc`) VALUES (403, 'config_environment_edit', '编辑环境');
INSERT INTO account_permissions (id, name, `desc`) VALUES (404, 'config_environment_del', '删除环境');



-- 系统管理 -> LDAP管理
INSERT INTO account_permissions (id, name, `desc`) VALUES (501, 'system_ldap_view', '系统LDAP列表');
INSERT INTO account_permissions (id, name, `desc`) VALUES (502, 'system_ldap_add', '添加LDAP设置');
INSERT INTO account_permissions (id, name, `desc`) VALUES (503, 'system_ldap_edit', '编辑LDAP设置');
INSERT INTO account_permissions (id, name, `desc`) VALUES (504, 'system_ldap_del', '删除LDAP设置');
INSERT INTO account_permissions (id, name, `desc`) VALUES (505, 'system_ldap_scrapes', '同步LDAP数据');

-- 系统管理 -> ansbile 管理-->执行管理
INSERT INTO account_permissions (id, name, `desc`) VALUES (601, 'system_ansible_view', 'ansible操作历史列表');
INSERT INTO account_permissions (id, name, `desc`) VALUES (602, 'system_ansible_run', 'ansible操作权限');


-- 系统管理 -> ansbile 管理-->静态主机管理
INSERT INTO account_permissions (id, name, `desc`) VALUES (701, 'system_ansible_host_view', '主机列表-查看');
INSERT INTO account_permissions (id, name, `desc`) VALUES (702, 'system_ansible_host_add', '主机列表-新增');
INSERT INTO account_permissions (id, name, `desc`) VALUES (703, 'system_ansible_host_edit', '主机列表-修改');
INSERT INTO account_permissions (id, name, `desc`) VALUES (704, 'system_ansible_host_del', '机列表-删除');


-- 系统管理 -> 渠道管理-->uuid 唯一标识
INSERT INTO account_permissions (id, name, `desc`) VALUES (801, 'system_channel_uuid_view', '渠道UUID列表-查看');
INSERT INTO account_permissions (id, name, `desc`) VALUES (802, 'system_channel_uuid_add', '渠道UUID列表-新增');
INSERT INTO account_permissions (id, name, `desc`) VALUES (803, 'system_channel_uuid_edit', '渠道UUID列表-修改');
INSERT INTO account_permissions (id, name, `desc`) VALUES (804, 'system_channel_uuid_del', '渠道UUID列表-删除');

-- 系统管理 -> 渠道管理-->IP白名单
INSERT INTO account_permissions (id, name, `desc`) VALUES (901, 'system_channel_ipwhilt_view', '渠道IP白名单-查看');
INSERT INTO account_permissions (id, name, `desc`) VALUES (902, 'system_channel_ipwhilt_add', '渠道IP白名单-新增');
INSERT INTO account_permissions (id, name, `desc`) VALUES (903, 'system_channel_ipwhilt_edit', '渠道IP白名单-修改');
INSERT INTO account_permissions (id, name, `desc`) VALUES (904, 'system_channel_ipwhilt_del', '渠道IP白名单-删除');


-- 应用发布 -> 应用管理
INSERT INTO account_permissions (id, name, `desc`) VALUES (1001, 'apps_appname_view', '应用列表-查看');
INSERT INTO account_permissions (id, name, `desc`) VALUES (1002, 'apps_appname_add', '应用列表-添加');
INSERT INTO account_permissions (id, name, `desc`) VALUES (1003, 'apps_appname_edit', '应用列表-修改');
INSERT INTO account_permissions (id, name, `desc`) VALUES (1004, 'apps_appname_del', '应用列表-删除');

-- 应用发布 -> jenkins管理
INSERT INTO account_permissions (id, name, `desc`) VALUES (1101, 'apps_jenkins_view', '应用发布结果-查看');
INSERT INTO account_permissions (id, name, `desc`) VALUES (1102, 'apps_jenkins_add', '应用发布-执行发布');
INSERT INTO account_permissions (id, name, `desc`) VALUES (1103, 'apps_jenkins_del', '发布历史列表-删除');

-- 应用发布 -> 服务管理
INSERT INTO account_permissions (id, name, `desc`) VALUES (1201, 'apps_service_view', '服务管理-查看');
INSERT INTO account_permissions (id, name, `desc`) VALUES (1202, 'assets_service_add', '服务管理-添加');
INSERT INTO account_permissions (id, name, `desc`) VALUES (1203, 'assets_service_edit', '服务管理-修改');
INSERT INTO account_permissions (id, name, `desc`) VALUES (1204, 'assets_service_del', '服务管理-删除');

-- 主机管理 -> 实例管理
INSERT INTO account_permissions (id, name, `desc`) VALUES (1301, 'assets_instance_view', '实例管理-查看');
INSERT INTO account_permissions (id, name, `desc`) VALUES (1302, 'assets_instance_add', '实例管理-添加');
INSERT INTO account_permissions (id, name, `desc`) VALUES (1303, 'assets_instance_edit', '实例管理-修改');
INSERT INTO account_permissions (id, name, `desc`) VALUES (1304, 'assets_instance_del', '实例管理-删除');

-- DNS管理 -> 私有dns解析管理
INSERT INTO account_permissions (id, name, `desc`) VALUES (1401, 'assets_privatedns_view', '私有DNS-查看');
INSERT INTO account_permissions (id, name, `desc`) VALUES (1402, 'assets_privatedns_add', '私有DNS-添加');
INSERT INTO account_permissions (id, name, `desc`) VALUES (1403, 'assets_privatedns_edit', '私有DNS-修改');
INSERT INTO account_permissions (id, name, `desc`) VALUES (1404, 'assets_privatedns_del', '私有DNS-删除');
-- DNS管理 -> 私有dns服务管理
INSERT INTO account_permissions (id, name, `desc`) VALUES (1501, 'assets_privatedns_service_view', '私有DNS服务-查看');
INSERT INTO account_permissions (id, name, `desc`) VALUES (1502, 'assets_privatedns_service_start', '私有DNS服务-启动');
INSERT INTO account_permissions (id, name, `desc`) VALUES (1503, 'assets_privatedns_service_stop', '私有DNS服务-停止');
INSERT INTO account_permissions (id, name, `desc`) VALUES (1504, 'assets_privatedns_service_restart', '私有DNS服务-重启');


