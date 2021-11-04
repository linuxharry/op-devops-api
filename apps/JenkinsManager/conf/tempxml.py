tempconf = """
<flow-definition plugin="workflow-job@2.35">
<actions>
<org.jenkinsci.plugins.pipeline.modeldefinition.actions.DeclarativeJobAction plugin="pipeline-model-definition@1.3.9"/>
<org.jenkinsci.plugins.pipeline.modeldefinition.actions.DeclarativeJobPropertyTrackerAction plugin="pipeline-model-definition@1.3.9">
<jobProperties/>
<triggers/>
<parameters/>
<options/>
</org.jenkinsci.plugins.pipeline.modeldefinition.actions.DeclarativeJobPropertyTrackerAction>
</actions>
<description/>
<keepDependencies>false</keepDependencies>
<properties>
<hudson.plugins.jira.JiraProjectProperty plugin="jira@3.0.10"/>
<com.dabsquared.gitlabjenkins.connection.GitLabConnectionProperty plugin="gitlab-plugin@1.5.13">
<gitLabConnection/>
</com.dabsquared.gitlabjenkins.connection.GitLabConnectionProperty>
<hudson.model.ParametersDefinitionProperty>
<parameterDefinitions>
<hudson.model.StringParameterDefinition>
<name>appname</name>
<description>当前应用名称</description>
<defaultValue/>
<trim>true</trim>
</hudson.model.StringParameterDefinition>
<hudson.model.StringParameterDefinition>
<name>version</name>
<description>当前应用版本信息</description>
<defaultValue/>
<trim>true</trim>
</hudson.model.StringParameterDefinition>
<hudson.model.StringParameterDefinition>
<name>giturl</name>
<description>项目URL地址</description>
<defaultValue/>
<trim>true</trim>
</hudson.model.StringParameterDefinition>
<hudson.model.StringParameterDefinition>
<name>branch</name>
<description>项目分支例如:master/depoly</description>
<defaultValue/>
<trim>false</trim>
</hudson.model.StringParameterDefinition>
<hudson.model.StringParameterDefinition>
<name>type</name>
<description>项目语言类型:1代表Java 2.python 3.Go 4.node.js</description>
<defaultValue/>
<trim>false</trim>
</hudson.model.StringParameterDefinition>
<hudson.model.StringParameterDefinition>
<name>ipadd</name>
<description>发布实例ip地址机器</description>
<defaultValue/>
<trim>false</trim>
</hudson.model.StringParameterDefinition>
</parameterDefinitions>
</hudson.model.ParametersDefinitionProperty>
</properties>
<definition class="org.jenkinsci.plugins.workflow.cps.CpsFlowDefinition" plugin="workflow-cps@2.75">
<script>{JenkinsPipelineTemp}</script>
<sandbox>true</sandbox>
</definition>
<triggers/>
<disabled>false</disabled>
</flow-definition>
"""

