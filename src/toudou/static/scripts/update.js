window.onload = init;

function init() {
    lines = document.getElementsByTagName("tr");
    for (var i = 0; i < lines.length; i++) {
        lines[i].onclick = line_on_click;
    }
}

function line_on_click() {
    var id = this.getAttribute("id");
    var id_field = document.getElementsByClassName("update_id");
    var id_title = document.getElementById("id_title");
    var task = document.getElementById("update_task");
    var due = document.getElementById("update_due");
    var completed = document.getElementById("update_comp");

    var s_date = this.children[1].innerHTML;

    if (s_date != "None") {
        var g_date = this.children[1].innerHTML;
        s_date = new Date(g_date.split(" ")[0]).toISOString().split("T")[0];
        due.value = s_date;
    }
    else {
        due.value = "";
    }

    id_title.innerHTML = id;
    
    for (var i = 0; i < id_field.length; i++) {
        id_field[i].value = id;
    }

    task.value = this.children[2].innerHTML;
    completed.checked = Boolean(this.children[3].innerHTML.toLowerCase() == "true");

    this.setAttribute("class", "todo_selected");

    allLines = document.getElementsByTagName("tr");

    for (var i = 0; i < allLines.length; i++) {
        if (allLines[i] != this) {
            allLines[i].setAttribute("class", "");
        }
    }
}