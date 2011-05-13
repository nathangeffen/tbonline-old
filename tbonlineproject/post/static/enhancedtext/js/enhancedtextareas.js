/* Much of the code below taken from Grappelli */


function CustomFileBrowser(field_name, url, type, win) {
    
    var cmsURL = '/admin/filebrowser/browse/?pop=2';
    cmsURL = cmsURL + '&type=' + type;
    
    tinyMCE.activeEditor.windowManager.open({
        file: cmsURL,
        width: 980,  // Your dimensions may differ - toy around with them!
        height: 500,
        resizable: 'yes',
        scrollbars: 'yes',
        inline: 'no',  // This parameter only has an effect if you use the inlinepopups plugin!
        close_previous: 'no',
    }, {
        window: win,
        input: field_name,
        editor_id: tinyMCE.selectedInstance.editorId,
    });
    return false;
}

tinyMCE.init({
    
    // see
    // http://wiki.moxiecode.com/index.php/TinyMCE:Configuration
    
    // Init
    mode: 'none',
    theme: 'advanced',
    skin: 'grappelli',
    
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
    width: 758,
    height: 300,
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
    
    // Grappelli
    grappelli_adv_hidden: false,
    grappelli_show_documentstructure: 'on',
    
	setup: function(ed) {
		ed.onKeyUp.add(function(ed, e) {
			insertWordCount(ed.getContent(), $('#' + this.id));    				
			insertCharCount(ed.getContent(), $('#' + this.id));
		});
	}


});


function countWords(text) {
	text = $.trim(text.replace(/(<([^>]+)>)/g,"")).match(/\w+/g);
	if (text==null || text=="") {
		return 0;
	} else {
		return text.length;
	}
	
}

function insertWordCount(text, selector) {
	words = countWords(text);
	selector.closest('div.column').find('.wordcount').html(words);
}

function countChars(text) {
	text = text.replace(/(<([^>]+)>)/g,"");
    text = $.trim(text);
    if (text.length==0) {
    	return 0;
    } else {
    	return text.length;
    }
}

function insertCharCount(text, selector) {
	chars = countChars(text);
	selector.closest('div.column').find('.charcount').html(chars);
}


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

var editors = {};

function selectEditor(text_format) {

	textarea = text_format.closest('div.column').find('textarea')[0].id;
	
	changeEditor(textarea, editors[textarea], 0);
	editors[textarea] = text_format[0].value;
	changeEditor(textarea, editors[textarea], 1);

};


$(document).
ready(function($){
	//Handle switching to and from TinyMCE Editor for textareas in editor class
	$('.enhanced_text_format').each(function() {
		editors[$(this).closest('div.column').find('textarea')[0].id] = '\\P';
		selectEditor($(this));
	});
	$('.enhanced_text_format').change(function(){
		selectEditor($(this));
	});

	$('.enhanced_text').each(function() {
		insertWordCount($(this).val(), $(this));
		insertCharCount($(this).val(), $(this));
	}); 
	$('.enhanced_text').keyup(function(){
		insertWordCount($(this).val(),$(this));
		insertCharCount($(this).val(),$(this));
	});
});
