% rebase('layout.tpl')

<h5>NWMC Attendance</h5>
<h6>Date: <strong>{{todaydate}}</strong></h6>
<br>
<h6> Current Class: <strong>{{currentclass}}</strong></h6>
<br>
<form action= "/" method="post">
	<label for="userinput">Last 5 of Social: </label>
		<input type="text" id="userinput" name="userinput"><input class="btn dark" type="submit" value="Submit">
		<hr/> 
			  %if status.startswith('R'):
			 <div class="alert info" align="center">{{status}}</div>
			  %elif status.startswith('S'):
			 <div class="alert success"align="center">{{status}}</div>
              %elif status.startswith('E'):
			 <div class="alert error"align="center">{{status}}</div>
			  %elif status.startswith('N'):
			 <div class="alert error"align="center">{{status}}</div>
			 %end
	<br>
</form>
<br>
<p> Social Not Working?  <button class="btn dark sml"><a href="/manualinput">Press Here</a></button></p>
</div>
<script>
document.getElementById("userinput").focus();
</script>
