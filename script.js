$(document).ready(function(){
    
    atomic_clock();
    $('#login_button').click(function(){
        if('#'){
            location.replace("/main.html");
        }else{

        }
        
    })

    function atomic_clock(){
        ntpClient.getNetworkTime("pool.ntp.org", 123, function(err, date) {
            if(err) {
                console.error(err);
                return;
            }
         
            console.log("Current time : ");
            console.log(date); // Mon Jul 08 2013 21:31:31 GMT+0200 (Paris, Madrid (heure d’été))
        });
    }
})