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

-- 主机管理 -> 主机列表
INSERT INTO account_permissions (id, name, `desc`) VALUES (301, 'assets_host_view', '获取主机列表');
INSERT INTO account_permissions (id, name, `desc`) VALUES (302, 'assets_host_add', '添加主机');
INSERT INTO account_permissions (id, name, `desc`) VALUES (303, 'assets_host_edit', '编辑主机');
INSERT INTO account_permissions (id, name, `desc`) VALUES (304, 'assets_host_del', '删除主机');
INSERT INTO account_permissions (id, name, `desc`) VALUES (305, 'assets_host_valid', '验证主机');


-- 应用发布 -> 应用列表 -> 发布页面
INSERT INTO account_permissions (id, name, `desc`) VALUES (401, 'publish_app_publish_host_select', '选择发布主机');
INSERT INTO account_permissions (id, name, `desc`) VALUES (402, 'publish_app_publish_menu_exec', '执行自定义菜单');


-- 配置管理 -> 环境管理
INSERT INTO account_permissions (id, name, `desc`) VALUES (501, 'config_environment_view', '获取环境列表');
INSERT INTO account_permissions (id, name, `desc`) VALUES (502, 'config_environment_add', '添加环境');
INSERT INTO account_permissions (id, name, `desc`) VALUES (503, 'config_environment_edit', '编辑环境');
INSERT INTO account_permissions (id, name, `desc`) VALUES (504, 'config_environment_del', '删除环境');



-- 系统管理 -> LDAP管理
INSERT INTO account_permissions (id, name, `desc`) VALUES (801, 'system_ldap_view', '系统LDAP列表');
INSERT INTO account_permissions (id, name, `desc`) VALUES (802, 'system_ldap_add', '添加LDAP设置');
INSERT INTO account_permissions (id, name, `desc`) VALUES (803, 'system_ldap_edit', '编辑LDAP设置');
INSERT INTO account_permissions (id, name, `desc`) VALUES (804, 'system_ldap_del', '删除LDAP设置');
INSERT INTO account_permissions (id, name, `desc`) VALUES (805, 'system_ldap_scrapes', '同步LDAP数据');

-- 系统管理 -> ansbile 管理-->执行管理
INSERT INTO account_permissions (id, name, `desc`) VALUES (901, 'system_ansible_view', 'ansible操作历史列表');
INSERT INTO account_permissions (id, name, `desc`) VALUES (902, 'system_ansible_run', 'ansible操作权限');


-- 系统管理 -> ansbile 管理-->静态主机管理
INSERT INTO account_permissions (id, name, `desc`) VALUES (1001, 'system_ansible_host_view', '主机列表-查看');
INSERT INTO account_permissions (id, name, `desc`) VALUES (1002, 'system_ansible_host_add', '主机列表-新增');
INSERT INTO account_permissions (id, name, `desc`) VALUES (1003, 'system_ansible_host_edit', '主机列表-修改');
INSERT INTO account_permissions (id, name, `desc`) VALUES (1004, 'system_ansible_host_del', '机列表-删除');


-- 系统管理 -> 渠道管理-->uuid 唯一标识
INSERT INTO account_permissions (id, name, `desc`) VALUES (1101, 'system_channel_uuid_view', '渠道UUID列表-查看');
INSERT INTO account_permissions (id, name, `desc`) VALUES (1102, 'system_channel_uuid_add', '渠道UUID列表-新增');
INSERT INTO account_permissions (id, name, `desc`) VALUES (1103, 'system_channel_uuid_edit', '渠道UUID列表-修改');
INSERT INTO account_permissions (id, name, `desc`) VALUES (1104, 'system_channel_uuid_del', '渠道UUID列表-删除');

-- 系统管理 -> 渠道管理-->IP白名单
INSERT INTO account_permissions (id, name, `desc`) VALUES (1201, 'system_channel_ipwhilt_view', '渠道IP白名单-查看');
INSERT INTO account_permissions (id, name, `desc`) VALUES (1202, 'system_channel_ipwhilt_add', '渠道IP白名单-新增');
INSERT INTO account_permissions (id, name, `desc`) VALUES (1203, 'system_channel_ipwhilt_edit', '渠道IP白名单-修改');
INSERT INTO account_permissions (id, name, `desc`) VALUES (1204, 'system_channel_ipwhilt_del', '渠道IP白名单-删除');


-- 应用发布 -> 应用管理
INSERT INTO account_permissions (id, name, `desc`) VALUES (1301, 'apps_appname_view', '应用列表-查看');
INSERT INTO account_permissions (id, name, `desc`) VALUES (1302, 'apps_appname_add', '应用列表-添加');
INSERT INTO account_permissions (id, name, `desc`) VALUES (1303, 'apps_appname_edit', '应用列表-修改');
INSERT INTO account_permissions (id, name, `desc`) VALUES (1304, 'apps_appname_del', '应用列表-删除');

-- 应用发布 -> jenkins管理
INSERT INTO account_permissions (id, name, `desc`) VALUES (1401, 'apps_jenkins_view', '应用发布结果-查看');
INSERT INTO account_permissions (id, name, `desc`) VALUES (1402, 'apps_jenkins_add', '应用发布-执行发布');
INSERT INTO account_permissions (id, name, `desc`) VALUES (1403, 'apps_jenkins_del', '发布历史列表-删除');

-- 应用发布 -> 服务管理
INSERT INTO account_permissions (id, name, `desc`) VALUES (1501, 'apps_service_view', '服务管理-查看');
INSERT INTO account_permissions (id, name, `desc`) VALUES (1502, 'assets_service_add', '服务管理-添加');
INSERT INTO account_permissions (id, name, `desc`) VALUES (1503, 'assets_service_edit', '服务管理-修改');
INSERT INTO account_permissions (id, name, `desc`) VALUES (1504, 'assets_service_del', '服务管理-删除');

-- 主机管理 -> 实例管理
INSERT INTO account_permissions (id, name, `desc`) VALUES (1601, 'assets_instance_view', '实例管理-查看');
INSERT INTO account_permissions (id, name, `desc`) VALUES (1602, 'assets_instance_add', '实例管理-添加');
INSERT INTO account_permissions (id, name, `desc`) VALUES (1603, 'assets_instance_edit', '实例管理-修改');
INSERT INTO account_permissions (id, name, `desc`) VALUES (1604, 'assets_instance_del', '实例管理-删除');


