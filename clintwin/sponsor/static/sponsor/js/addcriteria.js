// Need to grab th criteria entered and populate the "add criteria detail" page
var popup1 = document.getElementById("popup-1")
var openPopup1 = document.getElementById("add_btn")
var closePopup1 = document.getElementById('back_cri')

openPopup1.addEventListener('click', () => {
	popup1.style.display = "block";
})

closePopup1.addEventListener('click', () => {
	popup1.style.display = "none";
})
