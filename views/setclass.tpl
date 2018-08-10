% rebase('layout.tpl')
<h5>NWMC Attendance</h5>
<h6>Date: <strong>{{todaydate}}</strong></h6>
<br>
<h6> Current Class: <strong>{{currentclass}}</strong></h6>

<br>

		   <form action="/admin/setclass"method="post">
          <label for="setclass">Set the Class Name:  </label>
           <input type="text" id="classname" name="classname"><input class="btn dark" type="submit" value="Submit">
</form>
<br>
%if class_status is '':
	{{class_status}}
%elif class_status.startswith('C'):
    <h7><strong><div class="alert success" align="center">{{class_status}}</div></strong></h7>
%else:
	<h7><strong><div class="alert error" align="center">{{class_status}}</div></strong></h7>
%end

<form action="/admin/setclass" method="post">
    <input class="btn dark" type="submit" value="End Current Class">
</form>
<hr/>
<p><button class="btn dark sml"><a href="/admin">Return to Admin</a></button></p>