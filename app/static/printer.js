function printpage() {
    var content
    myWindow = window.open('', '', 'width=800,height=600');
    myWindow.innerWidth = screen.width;
    myWindow.innerHeight = screen.height;
    myWindow.screenX = 0;
    myWindow.screenY = 0;
    myWindow.document.body.innerHTML = content;
    myWindow.focus();
}