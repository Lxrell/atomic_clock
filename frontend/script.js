$(document).ready(function(){
    
    atomic_clock();

    // $('#login_button').click(function(){
    //     if('#'){
    //         location.replace("/main.html");
    //     }else{

    //     }
        
    // });

    // $('#atomic_clock').html(date());

    function atomic_clock(){
        const {spawn} = require('child_process');
        const childPython=spawn('python',['./backend/login.py']);
        childPython.stdout.on('data',(data)=>{
        console.log(`Current Time ${data}`)
        });
    }
//     function atomic_clock(){

//     $.ajax({
//         type:'GET',
//         dataType: 'JSON',
//         url: './backend/login.py/get_time_from_server',
//         success: function(data){
//             console.log(data);
//         }
//     })
// }

    

});