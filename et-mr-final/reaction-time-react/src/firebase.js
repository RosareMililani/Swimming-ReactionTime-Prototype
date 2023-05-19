import { getDatabase } from 'firebase/database'
import { initializeApp } from "firebase/app"
import { firebase } from './firebase.js'

const firebaseConfig = {
    apiKey: "AIzaSyBLptMKgZcl_fHDDciGF_v77xJyZKBxYSw",
    authDomain: "reaction-time-ba131.firebaseapp.com",
    databaseURL: "https://reaction-time-ba131-default-rtdb.firebaseio.com",
    projectId: "reaction-time-ba131",
    storageBucket: "reaction-time-ba131.appspot.com",
    messagingSenderId: "754168301232",
    appId: "1:754168301232:web:3026d6e352d4576ff5dd75",
    measurementId: "G-TR8X70TPZL"
};

const app = initializeApp(firebaseConfig);
export const db = getDatabase(app)