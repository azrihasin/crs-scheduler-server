
 


//document.getElementById("add").addEventListener("click", function() {  
  



var i=100;
function myFunction(){



var subject = document.getElementById('timetable').value;

var day=document.getElementById('day');

var daychoose = day.options[day.selectedIndex].value;

var time_start = document.getElementById('time_start').value;

var time_end = document.getElementById('time_end').value;



  document.getElementById( "timetable").innerHTML = subject;

  var period= time_start-time_end;
  var width=period*60;


  //starttime
  var fields = time_start.split(':');
  var hour = parseInt(fields[0]);
  var minute = parseInt(fields[1]);
  var masa=(hour*60)+minute;





  //endtime
  var fields1 = time_end.split(':');
  var hour1 = parseInt(fields1[0]);
  var minute1 = parseInt(fields1[1]);
  var masa1=(hour1*60)+minute1;


  //period of subject
  var period =((masa1-masa)/60)*60;

  var periodtext=period.toString();

  //width of subject
  var height=periodtext+"px";


//starttime aka top width
var topcal = ((masa-420)/60)*60;
var toptext=topcal.toString();
var top = toptext+"px";



if(masa>=420&&masa<=1350&&masa1>=420&&masa1<=1350){


if(daychoose=="MON"){



var div = document.createElement("div");
div.style.position="absolute";
div.style.top=top;
div.style.width = "100%";
div.style.height = height;
div.style.background = "blue";
div.style.color = "white";
div.innerHTML = subject;
div.setAttribute("id", i);



var div1 = document.createElement("LI");
var button = document.createElement("BUTTON");
div1.style.top="5px";
div1.style.width = "90%";
div1.style.height = "20px";
div1.style.background = "grey";
div1.style.color = "black";
div1.innerHTML = subject;
div1.setAttribute("id", i);

button.style.position="absolute";
button.style.left="80%";
button.style.width="20%";
button.style.height="20px";
button.setAttribute("id", i);
alert(button.id);
button.addEventListener('click', function () {
     deleteRow(button.id);
});
button.innerHTML="Remove";


div1.appendChild(button);

document.getElementById('MON').appendChild(div);
document.getElementById('SUBJECTELEMENT').appendChild(div1);


i++;


}
else if (daychoose=="TUE") {

  var div = document.createElement("div");
  div.style.position="absolute";
  div.style.top=top;
  div.style.width = "100%";
  div.style.height = height;
  div.style.background = "blue";
  div.style.color = "white";
  div.innerHTML = subject;
  div.setAttribute("id", i);



  var div1 = document.createElement("LI");
  var button = document.createElement("BUTTON");
  div1.style.top="5px";
  div1.style.width = "90%";
  div1.style.height = "20px";
  div1.style.background = "grey";
  div1.style.color = "black";
  div1.innerHTML = subject;
  div1.setAttribute("id", i);

  button.style.position="absolute";
  button.style.left="80%";
  button.style.width="20%";
  button.style.height="20px";
  button.setAttribute("id", i);
  alert(button.id);
  button.addEventListener('click', function () {
       deleteRow(button.id);
  });
  button.innerHTML="Remove";


  div1.appendChild(button);

  document.getElementById('TUE').appendChild(div);
  document.getElementById('SUBJECTELEMENT').appendChild(div1);


  i++;
}
else if (daychoose=="WED") {

  var div = document.createElement("div");
  div.style.position="absolute";
  div.style.top=top;
  div.style.width = "100%";
  div.style.height = height;
  div.style.background = "blue";
  div.style.color = "white";
  div.innerHTML = subject;
  div.setAttribute("id", i);



  var div1 = document.createElement("LI");
  var button = document.createElement("BUTTON");
  div1.style.top="5px";
  div1.style.width = "90%";
  div1.style.height = "20px";
  div1.style.background = "grey";
  div1.style.color = "black";
  div1.innerHTML = subject;
  div1.setAttribute("id", i);

  button.style.position="absolute";
  button.style.left="80%";
  button.style.width="20%";
  button.style.height="20px";
  button.setAttribute("id", i);
  alert(button.id);
  button.addEventListener('click', function () {
       deleteRow(button.id);
  });
  button.innerHTML="Remove";


  div1.appendChild(button);

  document.getElementById('WED').appendChild(div);
  document.getElementById('SUBJECTELEMENT').appendChild(div1);


  i++;

}
else if(daychoose=="THUR"){

  var div = document.createElement("div");
  div.style.position="absolute";
  div.style.top=top;
  div.style.width = "100%";
  div.style.height = height;
  div.style.background = "blue";
  div.style.color = "white";
  div.innerHTML = subject;
  div.setAttribute("id", i);



  var div1 = document.createElement("LI");
  var button = document.createElement("BUTTON");
  div1.style.top="5px";
  div1.style.width = "90%";
  div1.style.height = "20px";
  div1.style.background = "grey";
  div1.style.color = "black";
  div1.innerHTML = subject;
  div1.setAttribute("id", i);

  button.style.position="absolute";
  button.style.left="80%";
  button.style.width="20%";
  button.style.height="20px";
  button.setAttribute("id", i);
  alert(button.id);
  button.addEventListener('click', function () {
       deleteRow(button.id);
  });
  button.innerHTML="Remove";


  div1.appendChild(button);

  document.getElementById('THUR').appendChild(div);
  document.getElementById('SUBJECTELEMENT').appendChild(div1);


  i++;

}
else if (daychoose=="FRI") {

  var div = document.createElement("div");
  div.style.position="absolute";
  div.style.top=top;
  div.style.width = "100%";
  div.style.height = height;
  div.style.background = "blue";
  div.style.color = "white";
  div.innerHTML = subject;
  div.setAttribute("id", i);



  var div1 = document.createElement("LI");
  var button = document.createElement("BUTTON");
  div1.style.top="5px";
  div1.style.width = "90%";
  div1.style.height = "20px";
  div1.style.background = "grey";
  div1.style.color = "black";
  div1.innerHTML = subject;
  div1.setAttribute("id", i);

  button.style.position="absolute";
  button.style.left="80%";
  button.style.width="20%";
  button.style.height="20px";
  button.setAttribute("id", i);
  alert(button.id);
  button.addEventListener('click', function () {
       deleteRow(button.id);
  });
  button.innerHTML="Remove";


  div1.appendChild(button);

  document.getElementById('FRI').appendChild(div);
  document.getElementById('SUBJECTELEMENT').appendChild(div1);


  i++;

}
else if (daychoose=="SAT") {

  var div = document.createElement("div");
  div.style.position="absolute";
  div.style.top=top;
  div.style.width = "100%";
  div.style.height = height;
  div.style.background = "blue";
  div.style.color = "white";
  div.innerHTML = subject;
  div.setAttribute("id", i);



  var div1 = document.createElement("LI");
  var button = document.createElement("BUTTON");
  div1.style.top="5px";
  div1.style.width = "90%";
  div1.style.height = "20px";
  div1.style.background = "grey";
  div1.style.color = "black";
  div1.innerHTML = subject;
  div1.setAttribute("id", i);

  button.style.position="absolute";
  button.style.left="80%";
  button.style.width="20%";
  button.style.height="20px";
  button.setAttribute("id", i);
  alert(button.id);
  button.addEventListener('click', function () {
       deleteRow(button.id);
  });
  button.innerHTML="Remove";


  div1.appendChild(button);

  document.getElementById('SAT').appendChild(div);
  document.getElementById('SUBJECTELEMENT').appendChild(div1);


  i++;

}
else if(daychoose=="SUN"){

  var div = document.createElement("div");
  div.style.position="absolute";
  div.style.top=top;
  div.style.width = "100%";
  div.style.height = height;
  div.style.background = "blue";
  div.style.color = "white";
  div.innerHTML = subject;
  div.setAttribute("id", i);



  var div1 = document.createElement("LI");
  var button = document.createElement("BUTTON");
  div1.style.top="5px";
  div1.style.width = "90%";
  div1.style.height = "20px";
  div1.style.background = "grey";
  div1.style.color = "black";
  div1.innerHTML = subject;
  div1.setAttribute("id", i);

  button.style.position="absolute";
  button.style.left="80%";
  button.style.width="20%";
  button.style.height="20px";
  button.setAttribute("id", i);
  alert(button.id);
  button.addEventListener('click', function () {
       deleteRow(button.id);
  });
  button.innerHTML="Remove";


  div1.appendChild(button);

  document.getElementById('SUN').appendChild(div);
  document.getElementById('SUBJECTELEMENT').appendChild(div1);


  i++;

}


}

function deleteRow(x)
{
  var elem = document.getElementById(x);
  elem.parentNode.removeChild(elem);

  var elem = document.getElementById(x);
  elem.parentNode.removeChild(elem);
}
}
//});
