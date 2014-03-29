$(document).ready(function(){  
  var upload_form=$("#form_blob");
  var url=upload_form.attr("action");
  var files;
 
// Add events
  $('input[type=file]').on('change', prepareUpload);
// Grab the files and set them to our variable
  function prepareUpload(event)
  {
    files = event.target.files;
  }
  
  $("#upload_photo").click(function(){
    var data = new FormData();
    $.each(files, function(key, value)
    {
      data.append(key, value);
    });
    $(this).toggleClass("btn-info");
    $("#upload_photo").html("Uploading. . . ")
    $.ajax({
          url:url,
          type: 'POST',
          dataType : 'json',
          data:data,
          cache: false,
          processData: false, // Don't process the files
          contentType: false,
          success: function(data,status){
            // alert(data);
            alert(data.blob_key);
            $(".blob_key").val(data.blob_key);
            $("#upload_photo").html("Uploaded ");
            $("#upload_photo").toggleClass("btn-info");
          }
      });
  });//End Of File upload handler
  
});