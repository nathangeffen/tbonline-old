tinyMCE.init({
    
    // see
    // http://wiki.moxiecode.com/index.php/TinyMCE:Configuration
    
    // Init
    mode: 'textareas',
    theme: 'advanced',
    
    // General
    //accessibility_warnings: false,
    browsers: 'gecko,msie,safari,opera',
    dialog_type: 'window',
    editor_deselector: 'mceNoEditor',
    keep_styles : false,
    language: 'en',
    object_resizing: false,
    media_strict: true,
    
    // Callbackss
    file_browser_callback: 'CustomFileBrowser',
    
    // Layout
    width: 600,
    height: 320,
    indentation: '10px',
    
    // Cleanup
    cleanup : true,
    cleanup_on_startup: true,
    element_format : 'xhtml',
    fix_list_elements: true,
    fix_table_elements: true,
    fix_nesting: true,
    forced_root_block : 'p',
    
    // URL
    relative_urls: false,
    remove_script_host: true,
    
    // Content CSS
    // content_css : "css/example.css",
    
    // Plugins
    plugins: 'advimage,advlink,fullscreen,paste,media,searchreplace,grappelli,grappelli_contextmenu,template',
    
    // Theme Advanced
    theme_advanced_toolbar_location: 'top',
    theme_advanced_toolbar_align: 'left',
    theme_advanced_statusbar_location: 'bottom',
    theme_advanced_buttons1: 'formatselect,styleselect,|,bold,italic,underline,|,bullist,numlist,blockquote,|,undo,redo,|,link,unlink,|,image,|,fullscreen,|,grappelli_adv',
    theme_advanced_buttons2: 'search,|,pasteword,template,media,charmap,|,code,|,table,cleanup,grappelli_documentstructure',
    theme_advanced_buttons3: '',
    theme_advanced_path: false,
    theme_advanced_blockformats: 'p,h2,h3,h4,pre',
    theme_advanced_resizing : true,
    theme_advanced_resize_horizontal : false,
    theme_advanced_resizing_use_cookie : true,
    theme_advanced_styles: '',
    
    // Style formats
    // see http://wiki.moxiecode.com/index.php/TinyMCE:Configuration/style_formats
    style_formats : [
        {title : 'Paragraph Small', block : 'p', classes: 'p_small'},
        {title : 'Paragraph ImageCaption', block : 'p', classes: 'p_caption'},
        {title : 'Clearfix', block : 'p', classes: 'clearfix'},
        {title : 'Code', block : 'p', classes: 'code'}
    ],
    
    // Templates
    // see http://wiki.moxiecode.com/index.php/TinyMCE:Plugins/template
    // please note that you need to add the URLs (src) to your url-patterns
    // with django.views.generic.simple.direct_to_template
    template_templates : [
        {
            title : '2 Columns',
            src : '/path/to/your/template/',
            description : '2 Columns.'
        },
        {
            title : '4 Columns',
            src : '/path/to/your/template/',
            description : '4 Columns.'
        },
    ],
    
    // Adv
    advlink_styles: 'Internal Link=internal;External Link=external',
    advimage_update_dimensions_onchange: true,


});

function changeEditor(textarea, type, on) {
	switch(type) {
	case '\\W':
		if (on) {
			tinyMCE.execCommand('mceAddControl', false, textarea);
		} else {
			tinyMCE.execCommand('mceRemoveControl', false, textarea);
		};
		break;
	case '\\M':
		if (on) {
			$('#'+textarea).markItUp(mySettings);
		} else {
			$('#'+textarea).markItUpRemove();
		}
	};
};

function selectEditor(editorType) {

	textarea = 'id_body';
	
	changeEditor(textarea, editors[textarea], 0);
	editors[textarea] = editorType;
	changeEditor(textarea, editors[textarea], 1);

};

var editors = {};
var editorType = '\\W';
var fileCount = 0;
   
$(document).ready(function($){
    editors['id_body'] = editorType;
	$('#id_editor').change(function(){
	    editorType = $('#id_editor').val();
		selectEditor(editorType);
	});
    $('#add-image').live('click', function(){
        fileInputField = '<p><input type="file" class="image" id="image-file-'+fileCount+'" name="name-file-'+fileCount+'"/><input type="button" class="del-file" value="delete" /></p>';
        var hasValue = true;
        $('.image').each(function(){
            if(!$(this).val())
                hasValue = false;
        });
        if(hasValue || fileCount == 0){
            fileCount++;
            $('#id_form-TOTAL_FORMS').val(fileCount);
            $('#add-image').parent().before(fileInputField);
        }else{
            $('#add-image').parent().before('<p>Error: Can\'t add a file field. Use the empty file field instead.</p>');
            $('#add-image').parent().prev().hide().fadeIn('slow');
            setTimeout(function(){
                $('#add-image').parent().prev().fadeOut('slow', function(){
                    $('#add-image').parent().prev().remove();
                });
            }, 3000);
        }
    });
    $('.del-file').live('click', function(){
        $(this).parent().remove();
        fileCount--;
        $('#id_form-TOTAL_FORMS').val(fileCount);
    });
    $('.image').live('change', function(){
        var str = $(this).val();
        if(!str.toLowerCase().match("(.jpg|.gif|.png|.jpeg)$")){
            var field = $(this);
            field.val('');
            field.parent().before('<p>Error: File field only accepts jpg, gif, png and jpeg.</p>');
            field.parent().prev().hide().fadeIn('slow');
            setTimeout(function(){
                field.parent().prev().fadeOut('slow', function(){
                    field.parent().prev().remove();
                });
            }, 3000);
        }
    })
});
