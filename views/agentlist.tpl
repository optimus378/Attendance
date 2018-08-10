% rebase('layout.tpl')
<script type="text/javascript" src="/static/js/jquery.tablesorter.js"></script>
<script type="text/javascript" src="/static/js/tablesort.js"></script> 

<h6> List of all Agents</h6>
<br>
<br>
<table class="table" table id="usertable">
<thead>
			<th><button class="btn dark sml">Agent Name</button></th>
</thead>
<tbody>
		
    %for i in agentlist:
	<tr>
	<td><a href="/admin/reports/agents/{{i}}"</a>{{i}}</td>
	%end
</tbody>
</table>
<br>
<hr/>

<p><button class="btn dark sml"><a href="/reports">Return to Admin</a></button></p>

