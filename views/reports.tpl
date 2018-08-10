% rebase('layout.tpl')
<h3>Reports </h3>

<h6><u>Active Class</u></h6>
<h7><strong>{{currentclass}}</strong></h7>
<br>
<h7>Attendance Count: {{currentagentcount}}</h7>
<br>
<table class="table" id="currentclass">
	<thead>
		<tr>
			<th><button class="btn default sml">Agent Name</button></th>
			<th><button class="btn default sml">Checkin Time</button></th>
			<th><button class="btn default sml">Input Method</button></th>
		</tr>
	</thead>
<tbody>
		<br>
			%for i in currentreport:
			<tr>
			<td><a href="/admin/reports/agents/{{i[0]}}"</a>{{i[0]}}</td>
			<td>{{i[1]}}</td>
			<td>{{i[2]}}</td>
			</tr>
			%end
		</tbody>
	</table>
<br>

<p><button class="btn dark sml"><a href="/admin/setclass">Class Settings</a></button></p>

<br>
<hr/>
<h5> Individual Agent Reports</h5>

<form action= "/admin/reports/agentreport" method="post">
	<label for="agentname">Agent Name:</label>
		<input type="text" id="agentname" name="agentname"><input class="btn dark sml" type="submit" value="Search">
	%if notfound is None:
	<br>
	%else:
	<div class="alert error" align="center">{{notfound}}</div>
	%end
<a href ="/admin/agentlist">List of All Agents</a>
</form>
<hr/>
<h5>Previous Classes</h5>
<br>
<br>
<table class = "table" id="previousclass">
	<thead>
		 <tr>
			<th><button class="btn default sml">Class Name</button></th>
			<th><button class="btn default sml">Class Time</button></th>
		</tr>
	<thead>
	<tbody>
		
			%for i in classlist:
			<tr>
		    <td><a href="/admin/reports/classes/{{i[0]}}"</a>{{i[0]}}</td>
			<td>{{i[1]}}</td>
			<td><form action= "/admin" method="post">
				<input type="hidden" name="classname" value = "{{i[0]}}">
				<input class="btn error sml" type="Submit" value="delete">
			</td>
		</form>
			</tr>
			%end
			
	</tbody>
</table>
<script type="text/javascript" src="/static/js/tablesort.js"></script> 