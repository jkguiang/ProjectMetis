var jsonPath = "static/summaryinfo.json";
var refreshSecs = 10*60;

$(function() {
    load_json(jsonPath);
    setInterval(load_json, refreshSecs*1000);
});

$.ajaxSetup({
   type: 'POST',
   timeout: 15000,
});

function load_json(jsonPath){
    $.getJSON(jsonPath, function(data){
        set_sections(data);
        fill_sections(data);
    });
}

function set_sections(data){
    var container = $("#section_1");
    var i = 0;
    for (var key in data){
        var toappend = "";
        if (data.hasOwnProperty(key)){
            toappend += "<br>";
            //Link to toggle hidden of details_i
            toappend += ("<a href='#/' class='thick' onClick=\"$('#details_"+i+"').slideToggle(100)\">"+key+"</a>");
            toappend += "<div class='pbar' id='pbar_"+i+"'>";
            toappend +=      "<span id='pbartextleft_"+i+"' class='pbartextleft'></span>";
            toappend +=      "<span id='pbartextright_"+i+"' class='pbartextright'></span>";
            toappend += "</div>";
            //details_i to contain .stringify(data[dsname])
            toappend += "<div id='details_"+i+"' style='display:none;'></div>";

            container.append(toappend);
            i++;
        }
    }
}

function get_plots(data){
    var i = 0;
    for (var key in data){
        $("#details_"+i).append("<p id='plots_"+i+"'></p>");
        toappend = "";
        if (data.hasOwnProperty(key)){
            pltLst = data[key].Plots;
            for (var j = 0; j < pltLst.length; j++){
                toappend+="<img src="+pltLst[j]+" width=400 height=300>";
            }
            $("#plots_"+i).html(toappend);
            i++;
        }
    }
}

function get_summaries(data){
    var i = 0;
    for (var key in data){
        $("#details_"+i).append("<ul id='summary_"+i+"'></ul>");
        if (data.hasOwnProperty(key)){
            jsonStr = syntaxHighlight(JSON.stringify(data[key], undefined, 4));
            $("#summary_"+i).html("<pre>"+jsonStr+"</pre>");
            i++;
        }
    }
}

function fill_sections(data){
    get_plots(data);
    get_summaries(data);
}

function syntaxHighlight(json) {
    // stolen from http://stackoverflow.com/questions/4810841/how-can-i-pretty-print-json-using-javascript
    json = json.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');
    return json.replace(/("(\\u[a-zA-Z0-9]{4}|\\[^u]|[^\\"])*"(\s*:)?|\b(true|false|null)\b|-?\d+(?:\.\d*)?(?:[eE][+\-]?\d+)?)/g, function (match) {
        var cls = 'number';
        if (/^"/.test(match)) {
            if (/:$/.test(match)) {
                cls = 'key';
            } else {
                cls = 'string';
            }
        } else if (/true|false/.test(match)) {
            cls = 'boolean';
        } else if (/null/.test(match)) {
            cls = 'null';
        }
        return '<span class="' + cls + '">' + match + '</span>';
    });
}

function expandAll() {
    // do it this way because one guy may be reversed
    if(detailsVisible) {
        $("#toggle_all").text("show details");
        $("[id^=details_]").slideUp(100);
    } else {
        $("#toggle_all").text("hide details");
        $("[id^=details_]").slideDown(100);
    }
    detailsVisible = !detailsVisible;
}
