const user = JSON.parse(document.getElementById('user-name').textContent);
console.log(user);

// Getting the input
document.querySelector('.fuck_you').focus();
// If the user press enter...
document.querySelector('.fuck_you').onkeyup = (event) => {
    if (event.keyCode === 13) {
        document.querySelector('.submit-message').click(); // submitting the room name
    }
};

document.querySelector('.submit-message').onclick = (event) => {
    let roomName = document.querySelector('.fuck_you').value;
    // user redirection
    window.location.pathname = `/chat/${user}/${roomName}/`;
}