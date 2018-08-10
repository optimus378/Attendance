% rebase('layout.tpl')
<script type="text/javascript" src="/static/js/jquery.tablesorter.js"></script>
<script type="text/javascript" src="/static/js/tablesort.js"></script> 

<h6> Attendance Report for : {{name}}</h6>
<br>
<br>
<table class="table" table id="usertable">
<thead>
			<th><button class="btn dark sml">Class Date</button></th>
			<th><button class="btn dark sml">Class Name</button></th>
			<th><button class="btn dark sml">Input Method</button></th>
</thead>
<tbody>
	%for i in agentreport:
	<tr>
	<td>{{i[1]}}</td>
	<td><a href="/admin/reports/classes/{{i[0]}}"</a>{{i[0]}}</td>
	<td>{{i[2]}}</td>
	<tr>
	%end
</tbody>
</table>
<br>
<hr/>
<p><button class="btn dark sml"><a href="/download/agents/{{name}}">Export as CSV</a></button></p>
<p><button class="btn dark sml"><a href="/admin">Return to Admin</a></button></p>



