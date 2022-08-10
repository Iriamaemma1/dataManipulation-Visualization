/*!
* Start Bootstrap - Small Business v5.0.5 (https://startbootstrap.com/template/small-business)
* Copyright 2013-2022 Start Bootstrap
* Licensed under MIT (https://github.com/StartBootstrap/startbootstrap-small-business/blob/master/LICENSE)
*/
// This file is intentionally blank
// Use this file to add JavaScript to your project

var div = document.createElement('div');
return ('draggable' in div) || ('ondragstart' in div && 'ondrop' in div);
return 'FormData' in window;
'FileReader' in window
var isAdvancedUpload = function() {
    var div = document.createElement('div');
    return (('draggable' in div) || ('ondragstart' in div && 'ondrop' in div)) && 'FormData' in window && 'FileReader' in window;
  }();
  var $form = $('.box');

if (isAdvancedUpload) {
  $form.addClass('has-advanced-upload');
}

if (isAdvancedUpload) {

    var droppedFiles = false;
  
    $form.on('drag dragstart dragend dragover dragenter dragleave drop', function(e) {
      e.preventDefault();
      e.stopPropagation();
    })
    .on('dragover dragenter', function() {
      $form.addClass('is-dragover');
    })
    .on('dragleave dragend drop', function() {
      $form.removeClass('is-dragover');
    })
    .on('drop', function(e) {
      droppedFiles = e.originalEvent.dataTransfer.files;
    });
  
  }

  $form.find('input[type="file"]').prop('files', droppedFiles);

  $form.on('submit', function(e) {
    if ($form.hasClass('is-uploading')) return false;
  
    $form.addClass('is-uploading').removeClass('is-error');
  
    if (isAdvancedUpload) {
      // ajax for modern browsers
      e.preventDefault();

      var ajaxData = new FormData($form.get(0));
    
      if (droppedFiles) {
        $.each( droppedFiles, function(i, file) {
          ajaxData.append( $input.attr('name'), file );
        });
      }
    
      $.ajax({
        url: $form.attr('action'),
        type: $form.attr('method'),
        data: ajaxData,
        dataType: 'json',
        cache: false,
        contentType: false,
        processData: false,
        complete: function() {
          $form.removeClass('is-uploading');
        },
        success: function(data) {
          $form.addClass( data.success == true ? 'is-success' : 'is-error' );
          if (!data.success) $errorMsg.text(data.error);
        },
        error: function() {
          // Log the error, show an alert, whatever works for you
          alert("error occured");
        }
      });
    
    } else {
      // ajax for legacy browsers
      var iframeName  = 'uploadiframe' + new Date().getTime();
    $iframe   = $('<iframe name="' + iframeName + '" style="display: none;"></iframe>');

  $('body').append($iframe);
  $form.attr('target', iframeName);

  $iframe.one('load', function() {
    var data = JSON.parse($iframe.contents().find('body' ).text());
    $form
      .removeClass('is-uploading')
      .addClass(data.success == true ? 'is-success' : 'is-error')
      .removeAttr('target');
    if (!data.success) $errorMsg.text(data.error);
    $form.removeAttr('target');
    $iframe.remove();
  });
    }
  });

  $input.on('drop', function(e) { // when drag & drop is supported
    droppedFiles = e.originalEvent.dataTransfer.files;
    $form.trigger('submit');
  });
  
  // ...
  
  $input.on('change', function(e) { // when drag & drop is NOT supported
    $form.trigger('submit');
  });

  var $input    = $form.find('input[type="file"]'),
    $label    = $form.find('label'),
    showFiles = function(files) {
      $label.text(files.length > 1 ? ($input.attr('data-multiple-caption') || '').replace( '{count}', files.length ) : files[ 0 ].name);
    };

// ...

$input.on('drop', function(e) {
  droppedFiles = e.originalEvent.dataTransfer.files; // the files that were dropped
  showFiles( droppedFiles );
});

//...

$input.on('change', function(e) {
  showFiles(e.target.files);
});