//////////////////////////////////// clock, date
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
    let weekday = "Day " + day + " / 7";

    document.getElementById("clock").innerText = time;
    document.getElementById("day").innerText = weekday;
    var t = setTimeout(function(){ currentTime() }, 1000);

};

currentTime();

//////////////////////////////////// night mode
var toggle_night = false;
function nightMode(){
    if (toggle_night == false){
        document.getElementById("body").style.color="#faebd7";
        document.getElementById("body").style.background="#4b544b";
        document.getElementById("textbox1").style.background="rgba(0,0,0,0.25)";
        document.getElementById("textbox2").style.background="rgba(0,0,0,0.25)";
        document.getElementById("textbox3").style.background="rgba(0,0,0,0.25)";
        document.getElementById("textbox4").style.background="rgba(0,0,0,0.25)";
        document.getElementById("night").textContent="🌞";
        toggle_night = true;
    } else {
        document.getElementById("body").style.color="black";
        document.getElementById("body").style.background="#c7c7bb";
        document.getElementById("textbox1").style.background="rgba(0,0,0,0.50)";
        document.getElementById("textbox2").style.background="rgba(0,0,0,0.50)";
        document.getElementById("textbox3").style.background="rgba(0,0,0,0.50)";
        document.getElementById("textbox4").style.background="rgba(0,0,0,0.50)";
        document.getElementById("night").textContent="🌚";
        toggle_night = false;
    }
};

//////////////////////////////////// hockeyfeber
var music = new Audio('song.mp3');
var toggle_music = 0;
function playMusic(){
    if (music.paused) {
        music.play();
        document.getElementById("hockey").style.color="red";
    } else {
        music.pause();
        document.getElementById("hockey").style.color="black";
    }
};