// ----------------- ERROR MESSAGES -----------------------//
var NO_MSG="";
var NO_TITLE = "Please Select Your Title ";
var NO_STATE = "Please Select your State ";
var NO_INST = "Please Select Your Institute ";
var NO_FN = 'Please Enter your First Name !';
var WR_FN = 'Please Enter a Valid First Name !';
var WR_LN = 'Please Enter a Valid Last Name !';
var NO_EML = " Please Enter Your email ";
var WR_EML = "Please Enter a Valid Email ";
var NO_PW1 = 'Please Enter Password ';
var WR_PW1 = 'Please Enter Valid Password';
var NO_PW2 = 'Please Confirm Password !';
var WR_PW2 = 'Enter proper match in confirm password field';	
var NO_COURSE = " Selected Institute has not enrolled for any Course ";
var NOT_SELECT_COURSE = "Please select a Course ";
var NO_MOB = 'Please enter your mobile number';
var INV_MOB = "Enter valid phone number. It should be 10 digit no. beginning with 7/8/9";
var WR_MOB = "Enter a 10 digit no.";
var WR_OFF = "Enter valid Office number . It should be 11 digit no. starting with 0";
var NO_EXP = 'Please enter your experience';
var NO_GEN = ' Please enter your gender ';
var NO_QUAL = 'Please enter your Qualification';
var NO_STREAM = 'Please enter your Discipline';
var NO_DESG = "Please Select your designation";
var NO_TOS = "To Register you must agree to the TOS ";
var INV_OFF = "Enter 11 digit office number starting with 0";
//--------------------------------------------------------//


// --------------- Defining all regex values --------------//
var ck_fname = /^[A-Za-z](\. )?[A-Za-z]{1,30}$/;
var ck_lname = /^[A-Za-z]{1,30}$/;
var ck_email = /^([\w-]+(?:\.[\w-]+)*)@((?:[\w-]+\.)*\w[\w-]{0,66})\.([a-z]{2,6}(?:\.[a-z]{2})?)$/i ;
var ck_password =  /^[A-Za-z0-9!@#$%^&*()_]{6,20}$/;
var ck_mob = /^[7-9][0-9]{0,9}$/;
var ck_off = /^[0][0-9]{0,10}$/;
//---------------------------------------------------------//


function register_field_validation(pageid)
{

	
    var msg ="";
    var error=0; //Initialize error variable to 0 i.e no error
    
    if (pageid == '4')  // Request_registration
    { 
            var state =  document.getElementById('state').value;
            var Institute =  document.getElementById('Institute').value;
    
            msg = State_validate(state);
            if (msg!="") //Check if State is not selected
                  error=1;
            else 
            {	
                msg = Institute_validate(Institute);
                if (msg!="") //Check if Institute is not selected
                    error=1;
            }
    }               
    else if (error==0)
    {   // For Rest of the pages
         var title =  document.getElementById('title').value;
         msg = Title_validate(title)
         if (msg != "") //Check if Title is not selected
             error =1; 
    }
    
    
    // -------------- Common fields -------------------- // 
    var fname = document.getElementById('fname').value;
    var lname = document.getElementById('lname').value;
    var email = document.getElementById('email').value;
    
    if (error == 0)
    {
        msg = fname_validate(fname);
        if (msg!="")    // if error occured
            error=1;    // First name invalid
        else
        {
            msg = lname_validate(lname);
            if (msg!="") // if error occured
                error=1;
            
        }
        
        if (error==0)   // then check for other field validations
        {
            msg = email_validate(email);
            if (msg != "") // Check if email is blank
                error=1;
        }
    
    }
    // --------------------------------------------------//
    
    if ((error == 0) && (pageid == '4'))
    {
        var course = document.getElementById('Course').value;
        msg = course_validate(course);
        if (msg != "") // error occured
		 error = 1;
        // Role need not to be checked , coz it has been given a default , so user cannot unselect both  
    }
    
    // ----------------  Password Fields ---------------------//
    if (( pageid == '1' || pageid == '2' ) && (error == 0))
    {
        var password1 = document.getElementById('password1').value;
        var password2 = document.getElementById('password2').value;
        password1=String(password1);
        password2=String(password2);
        
        msg = password_validate(password1,password2)
        if (msg != "")
            error = 1;
    }
    // ----------------------------------------------------//
    
    
    
    // ----- Personal Information ------------//
    
    if ( (pageid != '4') && (error == 0) )
    {
    
        var expe = document.getElementById('experience').value;
        var gender = document.getElementById('gender').value;
        var Qual = document.getElementById('Qual').value;
        var stream = document.getElementById('stream').value; // Discipline
        var mob = document.getElementById('phone1').value;
        var off = document.getElementById('phone2').value;
    
        msg = Gender_validate(gender);
        if (msg!="")
            error=1;
        
        if (error==0)
        {
            msg = Qualification_validate(Qual);
            if (msg!="")
                error=1;
        }
        
        if (error==0)
        {
            msg = Stream_validate(stream);
            if (msg!="")
                error=1;
        }
        
        if (error==0)
        {
            msg = Experience_validate(expe);
            if (msg!="")
                error=1;
        }
        
        if (error==0)
        {
            msg = mob_validate(mob);
            if(msg!="")
                error=1;    
        }
        
         
        if (error==0)
        {
            msg = office_validate(off);
            if(msg!="")
                error=1;    
        }
    
    }
    // -----------------------------------------//
  
    // --------------- Common Fileds -------------//
    if (error==0)
    {
        var desg = document.getElementById('Desg').value;
        msg = Designation_validate(desg);
        
        if ( (error==0) && (msg!="") )
            error=1;
    } 
    //--------------------------------------------//
 
    if ( (error == 0)  && (pageid != '3') ) // tos not for edit profile page
    {
        var tos = document.getElementById('tos-yes').checked;
        
        msg = tos_validate(tos);
        if (msg!="") 
            error = 1;
        
    }
    
   
    //-------------------- SUBMISSION OF FORM -------------//
    if (error==1)
    {
    // If error has occured show error
    document.getElementById('error-msg-js').className = "status message submission-error is-shown"; 
    obj = document.getElementById('showerrormsg');
    obj.innerHTML = msg;
    location.href="#show-error";
    }
    else	
    {
    document.forms["register-form"].submit();
    }
    
    // ---------------------------------------------------//


}


//#Validate Firstname of the person #
//# It is a mandatory field         #
//# First Letter is Alphabet        #
//# Dot and space is allowed        #
//# Consecutive dots are not allowed #


function fname_validate(fname)
{
    //alert('fname called');

    if (fname == "") //Check if First name is Blank
        	return NO_FN;
    else if (!ck_fname.test(fname)) // Else Check for its validation
        	return WR_FN;
    else    // Else return null msg
        return NO_MSG;

}



function lname_validate(lname)
{
    //alert('lname called');

    if ((lname != "") && (!ck_lname.test(lname))) // If Last name is filled
        return WR_LN; 
    else
        return NO_MSG;

}



function email_validate(email)
{
    //alert('email called');

    if (email == "") // Check if email is blank
       return NO_EML;  
    else if(!ck_email.test(email)) // Else Check for its Validation
        return WR_EML; 
    else
        return NO_MSG;
}



function password_validate(password1,password2)
{   
     //alert('Password called');
    
     if (password1=="")	//Check if Field is Blank
        	return NO_PW1;
     else if (!ck_password.test(password1))
        	return WR_PW1; 
     else if (password2 == "") //Check if Field is Blank
        	return NO_PW2; 
     else if(password1 != password2) // Both Passwords Dont Match
        	return WR_PS2;
     else // No error occured in this part
          return NO_MSG; 
  
}


function mob_validate(mob)
{
    if (mob=="")
        	return NO_MOB;
    else if(!ck_mob.test(mob))  // Validate mobile number
        	return INV_MOB;
    else if ( mob.length != 10)
          return WR_MOB;
    else // No error occured in this part
         return NO_MSG;
}


function office_validate(off)
{
    if ((off != "") && (!ck_off.test(off)) )   // If office number filled
        return WR_OFF;
    else if  (off != "")
{
	if (off.length != 11)  
		return INV_OFF;
	else 
		return NO_MSG;
}
    else 
        return NO_MSG;
}


function course_validate(course)
{
    //alert('Password called');
    
    if (course=="nocourse")
        return NO_COURSE;
    else if (course == "")
	return NOT_SELECT_COURSE;
    else
        return NO_MSG;
}


function Gender_validate(gender)
{
    if (gender=="")
        return NO_GEN;
    else
        return NO_MSG;
}
function Qualification_validate(Qual)
{
    if (Qual=="")
        return NO_QUAL;
    else
        return NO_MSG;
}
function Stream_validate(stream)
{
    if (stream=="")
        return NO_STREAM;
    else
        return NO_MSG;
}

function Experience_validate(expe)
{
    if (expe=="")
        return NO_EXP;
    else
        return NO_MSG;
}

function Designation_validate(desg)
{
    if (desg=="")
        return NO_DESG;
    else
        return NO_MSG;

}

function State_validate(state)
{
    if (state=="")
        return NO_STATE;
    else
        return NO_MSG;
}

function Institute_validate(institute)
{
//alert(institute);
    if (institute=="")
        return NO_INST;
    else
        return NO_MSG;
}

function tos_validate(tos)
{
    if (tos==false)
        return NO_TOS;
    else
        return NO_MSG;
}


function Title_validate(title)
{
    if (title=="")
        return NO_TITLE;
    else
        return NO_MSG;
}


function timepass(pageid)
{
alert('timepass was called');
//document.forms["register-form"].submit();
}
