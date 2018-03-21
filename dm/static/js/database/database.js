$(function() {

    $('#add-submit').click(function() {
        $.ajax({
            url: '/dbs',
            data: $('#action-form').serialize(),
            type: 'post'
        }).done(function(data) {
            if (data.ok) {
                showFormSuccess(data.body);
                setTimeout(function() {
                    $('#addModal').modal('hide');
                }, 2000)
            } else {
                showFormMsg(data.body);
                setTimeout(function() {
                    $('#addModal').modal('hide');
                }, 2000)
            }
        }).fail(function(jqXHR) {
            if (jqXHR.responseJSON && !jqXHR.responseJSON.ok) {
                showFormError(jqXHR.responseJSON.error.message);
            } else {
                showFormError('网络错误，请稍后重试')
            }
        })
    });
});
