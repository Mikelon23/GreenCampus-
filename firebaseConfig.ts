import { initializeApp } from "firebase/app";
import { getAuth } from "firebase/auth";

// IMPORTANT: Replace the placeholder values below with your actual
// Firebase project configuration. You can find this in the Firebase console
// under Project settings > General > Your apps > Firebase SDK snippet > Config.
const firebaseConfig = {
  apiKey: "AIzaSyA9hrBGDvfxoLa9oIa8Fk23c6ZmQesqGgc",
  authDomain: "greencampusplus.firebaseapp.com",
  databaseURL: "https://greencampusplus-default-rtdb.firebaseio.com",
  projectId: "greencampusplus",
  storageBucket: "greencampusplus.appspot.com",
  messagingSenderId: "313213045401",
  appId: "1:313213045401:web:efb0f467e0de5650ff8608",
  measurementId: "G-8G89S7HKYB"
};

// This is your Web Push certificate key, used to authorize notification requests.
export const VAPID_KEY = "YOUR_VAPID_KEY_HERE";


// Check if the API key is still a placeholder.
export const isFirebaseConfigured = firebaseConfig.apiKey !== "AIzaSyXXXXXXXXXXXXXXXXXXXXXXXXXXX";

// Initialize Firebase
export const app = initializeApp(firebaseConfig);

// Initialize Firebase Authentication and get a reference to the service
export const auth = getAuth(app);