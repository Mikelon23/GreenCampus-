import React, { createContext, useContext, useEffect, useState } from 'react';
import { 
  User, 
  createUserWithEmailAndPassword, 
  signInWithEmailAndPassword, 
  signOut,
  onAuthStateChanged
} from 'firebase/auth';
import { auth, isFirebaseConfigured } from './firebaseConfig';
import FirebaseNotConfigured from './components/FirebaseNotConfigured';

// Define the shape of the context data
interface AuthContextType {
  user: User | null;
  loading: boolean;
  signup: (email: string, pass: string) => Promise<any>;
  login: (email: string, pass: string) => Promise<any>;
  logout: () => Promise<void>;
}

// Create the context with a default value
const AuthContext = createContext<AuthContextType | undefined>(undefined);

// AuthProvider component that wraps the application
export const AuthProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  // Mock user to bypass authentication.
  const mockUser = {
    email: 'guest@greencampus.plus',
  } as User;

  const value = {
    user: mockUser,
    loading: false, // App is never in an auth loading state
    signup: async () => {}, // Mock function
    login: async () => {}, // Mock function
    logout: async () => {}, // Mock function
  };
  
  // If Firebase isn't configured, show a helpful message instead of the app.
  // Note: With mock auth, this check is effectively bypassed for the main app flow.
  if (!isFirebaseConfigured) {
    return <FirebaseNotConfigured />;
  }


  return (
    <AuthContext.Provider value={value}>
      {children}
    </AuthContext.Provider>
  );
};

// Custom hook to use the AuthContext
export const useAuth = () => {
  const context = useContext(AuthContext);
  if (context === undefined) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
};