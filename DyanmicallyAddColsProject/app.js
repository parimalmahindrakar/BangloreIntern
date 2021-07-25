var incre = 1

function makeDiv(class_, id_) {
    var mainDiv = $(".row")
    mainDiv.append(
        '<div class= "width-col ' + class_ + '" id = "' + id_ + '">\
        </div>\
        '
    )
}
function onoption(value_) {
    var id_ = "#col-" + incre
    if (value_ == "selection") {
        makeDiv("col-6", "col-" + incre)
        var parent_value = $("#main_title_input").val()
        // console.log(parent_value)
        $(id_).append(
            '<div> \
                    <ul id="col-'+ incre + '-ul" class="' + parent_value + '"> \
                        <li>\
                             <input type = "text" placeholder = "option">\
                                <select id="main_title" onchange="onoption(this.value)" >\
                                    <option value = "message"> Message</option>\
                                    <option value="document">Document</option>\
                                    <option value="input">Input</option>\
                                    <option value="selection">Option</option>\
                                </select >\
                        </li > \
                    </ul> \
                    <button class="btn btn-info" onclick="addNewOption()"> + Add </button> \
                    <button class="btn btn-warning" onclick="removeOption()"> - Remove</button>\
                </div >'
        );
        incre = incre + 1
        console.log(incre)
    } else {
        // console.log(incre)
        id_ = "#col-" + (incre - 1)
        $(id_).empty()
    }
}




function addNewOption() {
    console.log("add incre : " + incre)
    $('#col-' + (incre - 1) + '-ul').append('\
                         <li>\
                             <input type = "text" placeholder = "option">\
                                <select id="main_title" onchange="onoption(this.value)">\
                                    <option value="message"> Message</option>\
                                    <option value="document">Document</option>\
                                    <option value="input">Input</option>\
                                    <option value="selection">Option</option>\
                                </select>\
                        </li> \
    ')

}
function removeOption() {
    let options_list = document.getElementById('col-' + (incre - 1) + '-ul');
    var listLi = document.querySelectorAll("#col-" + (incre - 1) + "-ul li");
    if (listLi.length > 1) {
        options_list.removeChild(options_list.lastElementChild);
    }
}