
var svg_repo_url = "http://gauthiier.github.io/www-micro-temporalities/img/scores/";
var csv_repo_url = "https://raw.githubusercontent.com/gauthiier/www-micro-temporalities/master/webpagetest/filtered/";

var data_ref = get_param('ref');

if(data_ref === "") {
	console.log('no ref aborting...');
} else {
	console.log('ref: ' + data_ref);
	draw(svg_repo_url + data_ref);
	synthesise(csv_repo_url + data_ref);
}

function get_param(name) {
    name = name.replace(/[\[]/, "\\[").replace(/[\]]/, "\\]");
    var regex = new RegExp("[\\?&]" + name + "=([^&#]*)"),
        results = regex.exec(location.search);
    return results === null ? "" : decodeURIComponent(results[1].replace(/\+/g, " "));
}