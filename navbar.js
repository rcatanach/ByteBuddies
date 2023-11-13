// Import the necessary functions
import { auth, signOutUser } from './firebase.js';

export function includeDone() {
    const userInfoElement = document.getElementById('userInfo');
    const userEmail = localStorage.getItem('userEmail');

    if (userEmail) {
        userInfoElement.textContent = `Logged in as: ${userEmail}`;
    } else {
        userInfoElement.textContent = 'Log in';
    }

    function logout() {
        console.log("inside logout");
        const confirmed = confirm("Are you sure you want to log out?");
        if (confirmed) {
        signOutUser(auth).then(() => {
            const userInfoElement = document.getElementById('userInfo');
            userInfoElement.textContent = "";
            window.location.href = 'LoginSignup.html'; 
        }).catch((error) => {
            console.error('Logout error:', error);
        });
        }
    }

    // Add the event listener for the logout button
    document.getElementById('logoutButton').addEventListener('click', logout);
};