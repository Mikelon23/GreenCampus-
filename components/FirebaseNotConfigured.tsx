import React from 'react';
import { LeafIcon } from './Icons';

const FirebaseNotConfigured: React.FC = () => {
    const configSnippet = `
const firebaseConfig = {
  apiKey: "YOUR_API_KEY",
  authDomain: "YOUR_AUTH_DOMAIN",
  projectId: "YOUR_PROJECT_ID",
  storageBucket: "YOUR_STORAGE_BUCKET",
  messagingSenderId: "YOUR_SENDER_ID",
  appId: "YOUR_APP_ID"
};`;

  return (
    <div className="min-h-screen flex items-center justify-center bg-base-300 p-4 text-gray-200">
      <div className="w-full max-w-2xl p-8 space-y-6 bg-base-200 rounded-xl shadow-lg text-center">
        <div className="flex items-center justify-center space-x-3 mb-4">
          <div className="bg-danger p-3 rounded-full inline-block">
            <LeafIcon className="w-8 h-8 text-white" />
          </div>
          <h1 className="text-3xl font-bold text-white tracking-wider">
            Configuration Needed
          </h1>
        </div>
        <h2 className="text-xl font-semibold text-danger">Firebase Is Not Configured</h2>
        <p className="text-gray-400">
          To use GreenCampus+, you need to set up a free Firebase project and add your project's configuration details to the app.
        </p>
        <div className="text-left bg-base-300 p-4 rounded-md border border-gray-700">
            <p className="text-gray-300 mb-2 font-medium">Please update the file <code className="bg-base-100 px-2 py-1 rounded text-primary">firebaseConfig.ts</code> with your credentials:</p>
            <pre className="bg-base-100 p-4 rounded-md overflow-x-auto text-sm text-gray-400">
                <code>
                    {configSnippet.trim()}
                </code>
            </pre>
        </div>
        <p className="text-sm text-gray-500">
          You can find these details in your Firebase project settings. This is a one-time setup step.
        </p>
         <a 
            href="https://console.firebase.google.com/" 
            target="_blank" 
            rel="noopener noreferrer"
            className="inline-block mt-4 py-2 px-4 bg-primary text-white font-semibold rounded-md hover:bg-emerald-500 transition duration-300"
        >
            Go to Firebase Console
        </a>
      </div>
    </div>
  );
};

export default FirebaseNotConfigured;
