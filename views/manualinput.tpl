% rebase('layout.tpl')

<h5>NWMC Attendance</h5>
<br>
<h6>Date: <strong>{{todaydate}}</strong></h6>
<h6> Current Class: <strong>{{currentclass}}</strong></h6>
<br>

<form action="/manualinput" method="post">
           <label for="userinput">First and Last Name:</label>
           <input type="text" id="userinput" name="userinput"><input class="btn dark" type="submit" value="Submit">
		   <div class="alert success">{{status}}</div>
</form>
<script src="/static/scripts/jquery-1.10.2.js"></script>
<script src="/static/scripts/bootstrap.js"></script>
<script src="/static/scripts/respond.js"></script>