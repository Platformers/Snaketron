<!DOCTYPE html> 

<!--
login.php
Destin LeBarron
-->
<!-- delete or make a thing-->
<?php
	//start session
	session_id('user');
	session_name('user');
	session_start('user');
	
	//chech to see fi user is already logged in
	if(isset($_SESSION['user']))
	{
		header('Location: welcome.php');
		exit;
	}

?>


<html lang="en"> 
  	
  <head>
   <?php 
		if (substr($_SERVER['HTTP_HOST'],0,9) == 'localhost')
		{
			echo '<base href="http://localhost/CIS-425/2161%20spring/">';
			include('../connect/local-connect.php');
		}
		else
		{
			echo '<base href="http://cis425a.wpcarey.asu.edu/dlebarro/">';
			include('../connect/server-connect.php');
		}
	?>
	
    <!-- Meta tag -->
    <meta charset="utf-8" />  <!--how to code this always and on final -->
	<meta name="robots" content="noindex,nofollow" />

    <!-- Link tag for CSS -->
    <link type="text/css" rel="stylesheet" href="stylesheets/a7ss.css" /> <!-- style to be named -->
	
	<!--javascript tags -->
	<!--<script type="text/javascript" src="js/a3Focus.js"></script> -->
	<script type="text/javascript" src="js/messages.js"></script>
	
	<!-- Favicon tag -->
	<link type="image/gif" rel="icon" href="images/pitchfork.ico" />

    <!-- Web Page Title -->
    <title>Login</title>

  </head>

  <body>
  
	<div id="wrapper">
	
		<?php include('../php/header.php'); ?> <!-- how to open and close a php code block -->
		<!-- ../ go up one level to get to a folder-->
		<div id="main">
			<p>Enter your Username and Password below to Login...</p>
		</div>
		
		<form id="regform" action="process/process.php" method="post">
		<!-- three arguments ID allows us to add style ,method-transfers data-,action tell it what to do-->
			<p>Login Form</p>
			<?php
				//check the return code from process.php
				if(isset($_GET['rc']))
				{
					if($_GET['rc'] == 1)
						echo '<p class="loginerror">Invalid Username!</p>';
					if($_GET['rc'] == 2)
						echo '<p class="loginerror">Invalid Password!</p>';
					if($_GET['rc'] == 3)
						echo '<p class="loginerror">Returned from process.php...!</p>';
				}
			
			
			?>
			<p>
				
				<!--username-->	<!--set the for,id and name = "uname"-->
				<label for="uname">Username:</label> 
				<input type="text" id="uname" name="uname"
				autofocus
				required
				title="Username: 4-15 chars; U/l case letters, 0-9, and -, _, !, $ only! No spaces. "
				pattern="[a-zA-Z0-9-_!$]{4,15}"
				onfocus="message(this.id)"
				/>
				<br/>
				
				<!--password-->	<!--set the for,id and name = "pword"-->
				<label for="pword">Password:</label> 
				<input type="password" id="pword" name="pword"
				required
				title="Pasword: 5-15 chars; U/l case letters, 0-9, and -, _, !, $ only! No spaces. "
				pattern="[a-zA-Z0-9-_!$]{5,15}"
				onfocus="message(this.id)" />
				<br/>
				
				</p>
					
				<p class="submit">	
					<input type="submit" value="SUMBIT" />
					<span class="reset">
						<input type="reset" value="CLEAR" onclick="history.go(0)"/>
					</span>
				</p>
		
		
		</form>
		
		<p id="jsmsgs"><p>
		
		<div id="prefooter"></div> <!-- empty div that lock footer into place -->
		
		<?php include('../php/footer.htm'); ?>
	</div>
  </body>

</html>