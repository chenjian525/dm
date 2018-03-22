$(function() {
    $('#exec_once').change(function() {
        if (document.getElementById('exec_once').checked) {
            $('#exec_per_minute').prop('disabled', true);
        } else {
            $('#exec_per_minute').prop('disabled', false);
        }
    });

    $('#exec_per_minute').change(function() {
        if ($('#exec_per_minute').val() > 0) {
            $('#exec_once').prop('disabled', true);
        } else {
            $('#exec_once').prop('disabled', false);
        }
    });

    $('#add-task').click(function () {
        if (!document.getElementById('exec_once').checked && $('#exec_per_minute').val() < 0) {
            showFormError('执行任务的时间周期请填写正数');
            return false
        }

        $.ajax({
            url: postUrl,
            type: 'post',
            data: $('#add-form').serialize()
        }).done(function (data) {
            if (data.ok) {
                showFormSuccess(data.body);
            } else {
                showFormMsg(data.body);
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