function activateNav() {
    $('ul.nav > li').on('click', function (evt) {
      if ($(evt.currentTarget).hasClass('toggle-nav')) return;
      $(evt.currentTarget).addClass('active').siblings().removeClass('active');
    });
  }
  
  
function addToggle() {
    $('li.toggle-nav').on('click', function () {
        $(this).find('i').toggleClass('rotate-180-deg');
        $('.navbar-nav.side-nav').toggleClass('hide-link-text');
        $('#wrapper').toggleClass('expanded');
    });
}

function fixHamburgerUl() {
    $('.navbar-toggle').on('click', function () {
        $('.navbar-nav.side-nav').removeClass('hide-link-text');
        $("#wrapper").removeClass('expanded');
        $('i.fa-arrow-left').removeClass('rotate-180-deg');
    });
}
function readtd(){
  var coll = document.getElementsByClassName("collapsible");
    var i;

    for (i = 0; i < coll.length; i++) {
        coll[i].addEventListener("click", function() {
            this.classList.toggle("active");
            var content = this.nextElementSibling
            if (content.style.maxHeight) {
              content.style.maxHeight = null;
            } 
            else {
              content.style.maxHeight = content.scrollHeight + "px";
            } 
      });
    }
}
function readmore(){
  var more = document.getElementById("more");
  var btn  = document.getElementById("myBtn");
  var btn2  = document.getElementById("myBtn2");

  more.style.display = 'inline';
  btn.style.display = 'none';
  btn2.style.display = 'inline';

}
function readless(){
  var more = document.getElementById("more");
  var btn  = document.getElementById("myBtn");
  var btn2  = document.getElementById("myBtn2");

  more.style.display = 'none';
  btn.style.display = 'inline';
  btn2.style.display = 'none';

}
function category_show(){
  $('#category_num_id').change(function() {
    var value = $(this).val(); 
    $("#report_table tr:even").filter(function() { 
      $(this).toggle($(this).children('td').eq(2).text().indexOf(value) > -1)
    });
    $("#report_table tr:odd").filter(function() { 
      $(this).toggle($(this).prev().children('td').eq(2).text().indexOf(value) > -1)
    });
  });
}
// 欄位名稱是找到row td 裡面的第四格和第二格改值，是寫死的，以後要修正要回來改。
function branch_show(){
  $('#branch_id').change(function() {
    var value = $(this).val(); 
    $("#report_table tr:even").filter(function() { 
      $(this).toggle($(this).children('td').eq(4).text().indexOf(value) > -1)
    });
    $("#report_table tr:odd").filter(function() { 
      $(this).toggle($(this).prev().children('td').eq(4).text().indexOf(value) > -1)
    });
  });
}
// 欄位名稱是找到row td 裡面的第四格和第二格改值，是寫死的，以後要修正要回來改。
function case_show(){
  $("#Case_id").on("keyup", function() {
    var value = $(this).val().toLowerCase();
    $("#report_table tr:even").filter(function() {
      $(this).toggle($(this).children('td').eq(1).text().toLowerCase().indexOf(value) > -1)
    });
    $("#report_table tr:odd").filter(function() { 
      $(this).toggle($(this).prev().children('td').eq(1).text().toLowerCase().indexOf(value) > -1)
    });
  });
}
function write_log(){
  $("#report_table a").click(function(){
    $.ajax({
         url : "/content_table_log",
         type : "POST",
         contentType: "application/json; charset=UTF-8",
         data : JSON.stringify({"postid" : $(this).data("postid"),
                                      "user" : $(this).data("userid"),
                                      "clicked_time" : new Date().toLocaleString("zh-TW", {timeZone: "Asia/Taipei"})
                                      }),
         success : function(response) {
              console.log('success');
              console.log(response); 
         },
         error : function(xhr) {
              console.log('error');
              console.log(xhr);
         }
    });
});
}


function init() {
  activateNav();
  addToggle();
  fixHamburgerUl();
  category_show();
  branch_show();
  case_show();
  write_log();
}
  
init();


window.onscroll = function() {myFunction()};

// Get the header
var header = document.getElementById("myHeader");

// Get the offset position of the navbar
var sticky = header.offsetTop;

// Add the sticky class to the header when you reach its scroll position. Remove "sticky" when you leave the scroll position
function myFunction() {
  if (window.pageYOffset > sticky) {
    header.classList.add("sticky");
  } else {
    header.classList.remove("sticky");
  }
}