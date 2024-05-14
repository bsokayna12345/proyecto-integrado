
function cargar_select(link, filter,target,text1,text2,text3=""){
    console.log("desde js ajax")
    selectFilter = $('#'.concat(filter)).find(':selected')
    selectTarget = $('#'.concat(target));
    filter_value = selectFilter.val();
    var csrfmiddlewaretoken = document.getElementsByName("csrfmiddlewaretoken")[0].value;
    
    $.ajax({
        method: "POST",
        url: link,
        data:{
            "csrfmiddlewaretoken":csrfmiddlewaretoken,
            "filter_value":filter_value,
        },
        dataType: "json",
        success:function(data){
            if(data.status === 200){
                selectTarget.val(null)

                var content = JSON.parse(data.content)

                if (content.length > 0){
                    empty_option(text1);

                    for (i = 0; i < content.length; i++) {
                        var newOption = new Option(content[i].texto, content[i].id, false, false);
                        selectTarget.append(newOption);
                    }
                    selectTarget.prop("disabled", false).trigger("change");      

                }else{
                    selectTarget.prop("disabled", true).trigger("change");
                    empty_option(text2);
                }
            }else{
                selectTarget.val(null)
                empty_option(text3);
                selectTarget.prop("disabled", true).trigger("change");
            }
        },
        error: function(){
            console.log('errror recibiendo datos')
        }
    });
    return;
}

function empty_option(text){
    selectTarget.empty();
    var data = {
        id : "",
        text: text
    };
    var optionDefault = new Option(data.text, data.id, false, false);
    selectTarget.append(optionDefault);
}