
function currentTime() {
    let date = new Date();
    let day = date.getDay();
    let hh = date.getHours();
    let mm = date.getMinutes();
    let ss = date.getSeconds();
    hh = (hh < 10) ? "0" + hh : hh;
    mm = (mm < 10) ? "0" + mm : mm;
    ss = (ss < 10) ? "0" + ss : ss;

    let time = hh + ":" + mm + ":" + ss + " ";

    document.getElementById("clock").innerText = time;
    document.getElementById("day").innerText = day;
    var t = setTimeout(function(){ currentTime() }, 1000);

}

currentTime();




function buttonColor() {
    document.getElementById("header").style.color="#2E4155";
}

