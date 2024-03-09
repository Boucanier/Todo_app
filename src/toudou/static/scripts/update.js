window.onload = init;


function init() {
    // Add event listeners to the table rows
    lines = document.getElementsByTagName("tr");
    for (var i = 0; i < lines.length; i++) {
        lines[i].onclick = line_on_click;
    }
}


/**
 * Handles the click event on a table row.
 * Updates the form fields with the selected row's data.
 */
function line_on_click() {
    // Remove the selected class from all rows
    allLines = document.getElementsByTagName("tr");
    for (var i = 0; i < allLines.length; i++) {
        allLines[i].setAttribute("class", "");
    }

    // Get the form fields
    var id = this.getAttribute("id");
    var id_field = document.getElementsByClassName("update_id");
    var id_title = document.getElementById("id_title");
    var task = document.getElementById("update_task");
    var due = document.getElementById("update_due");
    var completed = document.getElementById("update_comp");

    var s_date = this.children[1].innerHTML;

    // Set the date field
    if (s_date != "None") {
        var g_date = this.children[1].innerHTML;
        s_date = new Date(g_date.split(" ")[0]).toISOString().split("T")[0];
        due.value = s_date;
    }
    else {
        due.value = "";
    }

    // Set the form title
    id_title.innerHTML = id;
    
    // Set the id fields
    for (var i = 0; i < id_field.length; i++) {
        id_field[i].value = id;
    }

    // Set the task field
    task.value = this.children[2].innerHTML;

    // Set the completed field
    if (this.children[3].innerHTML.toLowerCase() == "yes") {
        completed.checked = true;
    }
    else {
        completed.checked = false;
    }

    // Set the selected class to the clicked row
    this.setAttribute("class", "todo_selected");
}