<?php
	//a7
	//process.php
	//Spring 2016
	//Destin LeBarron
	
	//connect to db - LOCAL or SERVER
	include('../connect/server-connect.php');
	
	//variable for cslashes
	$chars = '_%';
	
	//get username from html
	$uname = mysqli_real_escape_string($dbc, $_POST['uname']);
	
	//escape the entry agains
	$uname = addcslashes($uname, $chars);
	
		//get password from html
	$pword = mysqli_real_escape_string($dbc, $_POST['pword']);
	
	//escape the entry agains
	$pword = addcslashes($pword, $chars);
	
	//build our query
	$query = "select * from hw7 where uname = '$uname'";
	
	//run the querey
	$result = mysqli_query($dbc, $query) or die('username read error: '.mysqli_error($dbc));
	
	//check to see if we got
	if (mysqli_num_rows($result) == 0)
	{
	//username invalid pas rc =1 to login.php
	header('Location: login.php?rc=1');
	exit;
	}
	//if we got to here we can verify username
	
	//store result of query for pass veri
	$row= mysqli_fetch_array($result);
	
	//salt and hash the pword for comparison
	//if (password_verify($pword, $row['pword']) == $row['pword'])
	if (crypt($pword, $row['pword']) == $row['pword'])
	{
		//passwords match - populate session variable and sendd to welcom page
		session_id('user');
		session_name('user');
		session_start('user');
		$_SESSION['user'] = $row['name'];
		
		//close the db connection
		mysqli_close($dbc);
		
		//transfer to welcom page
		header('Location: welcome.php');
		exit;
	}
	else
	{
		//password invalid
		header('Location: login.php?rc=2');
		exit;
	}
	
	
	
	
	
	
	
	
	
	//pass 3 back to login.php fo testing 
	//MAKE SURE THIS CODE STAYS AT THE BOTTOM
	header('Location: login.php?rc=3');
	exit;
	
	
	?>