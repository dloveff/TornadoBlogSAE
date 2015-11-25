 $(document).scroll(function() {
     //固定SideBar
     if ($(document).scrollTop() > '80') {
         $('.stickup').offset({
             top: $(document).scrollTop() + 5
         });
     } else if ($(document).scrollTop() <= '80') {
         $('.stickup').offset({
             top: $(document).scrollTop() + 68
         });
     };
 });

function insertAtCursor(myValue) {
	myField = document.getElementById("textarea");
	//IE support
	if (document.selection) {
	    myField.focus();
	    sel = document.selection.createRange();
	    sel.text = myValue;
	}
	//MOZILLA and others
	else if (myField.selectionStart || myField.selectionStart == '0') {
	    var startPos = myField.selectionStart;
	    var endPos = myField.selectionEnd;
	    myField.value = myField.value.substring(0, startPos)
	        + myValue
	        + myField.value.substring(endPos, myField.value.length);
	        myField.selectionStart = startPos + myValue.length;
	        myField.selectionEnd = startPos + myValue.length;
	} else {
	    myField.value += myValue;
	}
}

document.getElementById('textarea').onkeydown = function(e){
 if (e.keyCode == 9) {
 insertAtCursor('    ');
 return false;
 }
}
