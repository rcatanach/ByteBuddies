// Import the functions you need from the SDKs you need
import { initializeApp } from "https://www.gstatic.com/firebasejs/10.4.0/firebase-app.js";

// Add SDKs for Firebase products that you want to use
// https://firebase.google.com/docs/web/setup#available-libraries
//Auth is used for login
import {signInWithEmailAndPassword, createUserWithEmailAndPassword} from 'https://www.gstatic.com/firebasejs/10.4.0/firebase-auth.js';
import { getAuth } from 'https://www.gstatic.com/firebasejs/10.4.0/firebase-auth.js';
import { signOut } from 'https://www.gstatic.com/firebasejs/10.4.0/firebase-auth.js';
//Firestore is used to store user inventory data (wardrobe)
//May need to use realtime database for web instead
import { getFirestore, doc, setDoc, getDoc, getDocs, collection } from 'https://www.gstatic.com/firebasejs/10.4.0/firebase-firestore.js';

import { getStorage, ref, uploadBytes, getDownloadURL} from 'https://www.gstatic.com/firebasejs/10.4.0/firebase-storage.js'

// Your web app's Firebase configuration
const firebaseConfig = {
  apiKey: "AIzaSyAu0txbxPTURDhHH4AMQ_4ElOjPIXrwXvs",
  authDomain: "mix-match-magic-f648a.firebaseapp.com",
  projectId: "mix-match-magic-f648a",
  storageBucket: "mix-match-magic-f648a.appspot.com",
  messagingSenderId: "635447219934",
  appId: "1:635447219934:web:9b873aedd01a140431944f",
  storageBucket: "gs://mix-match-magic-f648a.appspot.com"
};



// Initialize Firebase
const app = initializeApp(firebaseConfig);
console.log("Firebase initialized:", app);

// Export the initialized Firebase app and services for use in other files
export const firebaseApp = app;

// Export the authentication functions
export const auth = getAuth(firebaseApp);
export const signIn = signInWithEmailAndPassword;
export const createUser = createUserWithEmailAndPassword;
export const signOutUser = signOut;

//storage functions
export const storage = getStorage(app);
export const storageRef = ref(storage); // This is the root storage reference
export {uploadBytes, ref, getDownloadURL}; // Export the uploadBytes function and ref

//firestore functions
export const db = getFirestore(app);
export {doc, setDoc, getDoc, getDocs, collection}
