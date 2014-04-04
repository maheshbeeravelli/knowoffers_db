$(document).ready(function(){  
//Functions 
  $(".a[data-key]").on("click", function() {
    $(this).removeAttr("data-pause");
    $(this).attr("data-play",4);
    $("#output").text("playing 4");
  });
  


//DataManipulaters
  $( ".posted_on" ).each(function( index ) {
      // console.log( index + ": " + $( this ).text() );
      var date=$(this).text();
      var posted_split = date.split(",");
      var posted_date =new Date(posted_split[0]+","+posted_split[1])
      console.log("Posted Date " +posted_date);
      var today=new Date();
      var timeDiff = Math.abs(today.getTime() - posted_date.getTime());
      var diffDays = Math.ceil(timeDiff / (1000 * 3600 * 24)); 
      diffDays--;
      // alert("Difference Days : " + diffDays);
      if(diffDays>30)
      {
        var months = Math.ceil(diffDays/30);
        $( this ).text(months+ "months ago");
      }
      else if(diffDays>6)
      {
        weeks =diffDays/7;
        if(weeks<2){
          $( this ).text("1 week ago");
        }
        else{
          week=Math.ceil(weeks);
          $( this ).text(week + " weeks ago");
        }
      }
      else if(diffDays>1)
      {
        $( this ).text(diffDays+ " days ago");
      }
      else if (diffDays==1){
        $( this ).text("Yesterday");
      }
      else{
        $( this ).text("Today");
      }
  });
  
  $( ".expires-on" ).each(function( index ) {
      var date=$(this).text().trim();
      var expiry_split = date.split(",");
      var expiry_date =new Date(expiry_split[0]+","+expiry_split[1])
      console.log("Expiry Date :" +expiry_date);
      var today=new Date();
      var timeDiff = Math.abs(today.getTime() - expiry_date.getTime());
      var diffDays = Math.ceil(timeDiff / (1000 * 3600 * 24)); 
      diffDays;
      // diffDays = -diffDays;
      console.log("Expiry Difference :" + diffDays)
      if(date=="Nov. 1, 1991")
      {
        $( this ).text("No Expiry Date");
      }
      if(diffDays==7)
      {
        $( this ).text("1 week left");
      }
      else if (diffDays==1){
        $( this ).text("1 day left");
      }
      else if(diffDays==0){
        $(this).text("Last Day");
      }
      else if(diffDays<0)
      {
        $(this).text("Expired");
      }
      
  });
});