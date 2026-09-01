function addChar(selector, obj) {
	let char = obj.getAttribute("value");
	selector.value = selector.value.slice(0, selector.selectionStart) + char +
		selector.value.slice(selector.selectionEnd);
}
let hasBeenClicked;
let link;
if (document.getElementById("showCode")) {
    link = document.getElementById("showCode");
    link.addEventListener("click", showCode);
}
function showCode() {
	if (hasBeenClicked != true) {
		document.getElementById("solution").style.visibility = "visible";
		link.innerHTML = "Click here to hide example solution";
		hasBeenClicked = true;
	}
	else{
		document.getElementById("solution").style.visibility = "hidden";
		link.innerHTML = "Click here to show example solution";
		hasBeenClicked = false;
	}
}