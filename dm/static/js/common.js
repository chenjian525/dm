/**** for sending all ajax post and delete requests with parameters _xsrf  ****/
$.ajaxSetup({
     beforeSend: function(xhr, settings) {
        if(settings.type == 'POST' || settings.type == 'DELETE') {
             xhr.setRequestHeader("X-XSRFToken", $('input[name="_xsrf"]').val());
         }
     }
});
/**** end for sending all ajax post and delete requests with parameters _xsrf  ****/

function showFormMsg(msg, delay) {
    $('#form-alert').show_now(msg, delay);
}

function showFormError(msg, delay) {
    $('#form-alert').removeClass('alert-success').addClass('alert-danger').show_now(msg, delay || 3000);
}

function showFormSuccess(msg, delay) {
    $('#form-alert').removeClass('alert-danger').addClass('alert-success').show_now(msg, delay || 5000);
}

function clearFormMsg() {
    $('#form-alert').hide();
}

function showBFFormMsg(msg, delay) {
    $('#bf_form-alert').show_now(msg, delay);
}

function showBFFormError(msg, delay) {
    $('#bf_form-alert').removeClass('alert-success').addClass('alert-danger').show_now(msg, delay || 3000);
}

function showBFFormSuccess(msg, delay) {
    $('#bf_form-alert').removeClass('alert-danger').addClass('alert-success').show_now(msg, delay || 5000);
}

function clearBFFormMsg() {
    $('#bf_form-alert').hide();
}

$.extend($.fn, {
	checkRegValid: function(reg, msg, formError) {
		formError = typeof formError !== 'undefined' ?  formError : false;

		if (formError) {
            if(reg.test(this.trimVal())) {
                return true;
            }
            showFormError(msg)
		}else {
            if(reg.test(this.trimVal())) {
                this.showSuccess();
                return true;
            }
            this.showError(msg);
		}
	},
	showSuccess: function() {
		this.parents('.form-group').removeClass('has-error').addClass('has-success');
		this.siblings('.form-control-feedback').removeClass('hide glyphicon-remove').addClass('glyphicon-ok');
		$('#'+this.attr('id')+'-error').addClass('hide');
	},
	showError: function(msg) {
		this.parents('.form-group').removeClass('has-success').addClass('has-error');
		this.siblings('.form-control-feedback').removeClass('hide glyphicon-ok').addClass('glyphicon-remove');
		$('#'+this.attr('id')+'-error').removeClass('hide').html(msg);
	},
	clearFeedback: function() {
		this.parents('.form-group').removeClass('has-success has-error')
		this.siblings('.form-control-feedback').addClass('hide');
		$('#'+this.attr('id')+'-error').addClass('hide');
	},
	trimVal: function(){
		return $.trim(this.val());
	},
	show_now: function(msg, delay){
	    this.html(msg).show();
	    if (delay){
            this.delay(3000).fadeOut();
	    }
	},
});

