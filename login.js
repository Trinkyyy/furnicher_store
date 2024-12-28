let container = document.getElementById('container');

toggle = () => {
    container.classList.toggle('sign-in');
    container.classList.toggle('sign-up');
}

signup = () => {
    // Implement sign-up logic here
    alert('Sign up functionality not implemented yet');
}

signin = () => {
    // Implement sign-in logic here
    alert('Sign in functionality not implemented yet');
}

setTimeout(() => {
    container.classList.add('sign-in');
}, 200);
