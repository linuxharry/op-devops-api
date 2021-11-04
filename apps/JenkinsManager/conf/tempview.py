viewConf="""
<hudson.model.ListView>
<filterExecutors>false</filterExecutors>
<filterQueue>false</filterQueue>
<properties class="hudson.model.View$PropertyList"/>
<jobNames>
<comparator class="hudson.util.CaseInsensitiveComparator"/>
</jobNames>
<jobFilters/>
<columns>
<hudson.views.StatusColumn/>
<hudson.views.WeatherColumn/>
<hudson.views.JobColumn/>
<hudson.views.LastSuccessColumn/>
<hudson.views.LastFailureColumn/>
<hudson.views.LastDurationColumn/>
<hudson.views.BuildButtonColumn/>
<hudson.plugins.favorite.column.FavoriteColumn plugin="favorite@2.3.2"/>
</columns>
<includeRegex>^.+-ci$</includeRegex>
<recurse>false</recurse>
</hudson.model.ListView>
"""