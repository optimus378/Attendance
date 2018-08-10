% rebase('layout.tpl')
<script type="text/javascript" src="/static/js/jquery.tablesorter.js"></script>
<script type="text/javascript" src="/static/js/tablesort.js"></script> 

<h6> Classreport for: {{name}}</h6>
<br>
<br>
%if classreport is None:
	<h7><strong><div class="alert error" align="center">No Info.</div></strong></h7>
%else:
<table class="table" table id="usertable">
<thead>
			<th><button class="btn dark sml">Agent Name</button></th>
			<th><button class="btn dark sml">Checkin Time</button></th>
			<th><button class="btn dark sml">Input Method</button></th>
</thead>
<tbody>
	
		
    %for i in classreport:
	<tr>
	<td><a href="/admin/reports/agents/{{i[0]}}"</a>{{i[0]}}</td>
	<td>{{i[1]}}</td>
	<td>{{i[2]}}</td>
	<td><form action= "/admin/reports/classes/{{name}}" method="post">
		%agentname = i[0]
		<input type="hidden" name="agentname" value="{{i[0]}}">
		<input type="hidden" name="classname">
		<input class="btn error sml" type="Submit" value="delete">
		</form>
	<tr>
	%end
	<tr><td>Total Attended: {{agentcount}}</td></tr>
</tbody>
</table>
<br>
<hr/>
<form action= "/admin/reports/class/manualagentadd" method="post">
	<label for="agentname">Add Agent to Class: </label>
		<input type="text" id="agentname" name="agentname"><input class="btn dark sml" type="submit" value="Add">
		%classname = name
		%end
		<input type="hidden" name="classname" value="{{name}}"/>
</form


<p><button class="btn dark sml"><a href="/download/classes/{{name}}">Export as CSV</a></button></p>
<p><button class="btn dark sml"><a href="/admin">Return to Admin</a></button></p>

