$(function() {
    console.log('hello world');
    $('#add-submit').click(function() {
        console.log($('#action-form').serialize());
        $.post('/dbs', $('#action-form').serialize(), function(data) {
            if (data.ok) {
                showFormMsg('添加成功');
            } else {
                showFormError(data)
            }
        }).fail(function(jqXHR) {
            showFormError('网络错误，请稍后重试')
        })
    });
});