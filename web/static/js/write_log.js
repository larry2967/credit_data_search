



let histories=[];
let addHistory = function(ev){
    ev.preventDefault();
    let history ={
        time:Date.now(),
        user:document.getElementById('user_name').textContent(),
        search_input:document.getElementById('MyInput').value
    };
    console.log(history);
histories.push(history);
document.forms[0].reset();
localStorage.setItem('userhistory',JSON.stringify(histories));
}
$("#report_table a").on("click", function() {
    $.ajax({
            url :  "/content_table_log",
            type : "POST",
            contentType: 'application/json; charset=UTF-8',
            dataType: "json",
            data : JSON.stringify({'postid' : $(this).data('postid'),
                                        'user' : $(this).data('userid'),
                                        'clicked_time' : new Date().toLocaleString('zh-TW', {timeZone: 'Asia/Taipei'})
                                        }),
            success : function(response) {
                console.log(response); 
            },
            error : function(xhr) {
                console.log(xhr);
            }
    });
});
//document.getElementById('btn').addEventListener('click',addHistory);
    