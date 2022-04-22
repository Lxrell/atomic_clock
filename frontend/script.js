$(document).ready(function(){
    
    atomic_clock();

    $('#login_button').click(function(){
        if($('#username').val().length() == 0){
            alert('Enter Username');
        }else if($('#input_password').val().length() == 0){
            alert('Enter Password');

        }else{
            /*Enter code to get data from backend
            if returned is true then open main page
            else alert fail, incorrect username/ password etc
            */
        }


        location.replace("/main.html");
        
    });

    $('#atomic_clock').html(date());

    function atomic_clock(){
        const {spawn} = require('child_process');
        const childPython=spawn('python',['./backend/login.py']);
        childPython.stdout.on('data',(data)=>{
        console.log(`Current Time ${data}`)
        });
    }    

});