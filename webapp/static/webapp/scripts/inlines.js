$(function(){
    $('.inline-group .inline-related .delete input').each(function(i,e){
        $(e).bind('change', function(e){
            if(this.checked) {
                // marked for deletion
                $(this).parents('.inline-related').children('fieldset.module').addClass('collapsed collapse')
            }else{
                $(this).parents('.inline-related').children('fieldset.module').removeClass('collapsed')
            }
        })
    })
})

function increment_form_ids(el, to, name) {
    var from = to-1
    $(':input', $(el)).each(function(i,e){
        var old_name = $(e).attr('name')
        var old_id = $(e).attr('id')
        $(e).attr('name', old_name.replace(from, to))
        $(e).attr('id', old_id.replace(from, to))
        $(e).val('')
    })
}


function add_inline_form(name) {
    var first = $('#id_'+name+'-0-id').parents('.inline-related')
    var last = $(first).parent().children('.last-related')
    var copy = $(last).clone(true)
    var count = $(first).parent().children('.inline-related').length
    $(last).removeClass('last-related');
    $(last).after(copy);
    $('input#id_'+name+'-TOTAL_FORMS').val(count+1)
    increment_form_ids($(first).parents('.inline-group').children('.last-related'), count, name);
    return false;
}

$(document).ready(function(){
    // Note the name passed in is the model's name, all lower case
    $('div.last-related').after('<div><a class="add" href="#" onclick="return add_inline_form(\'photos\')">');
});