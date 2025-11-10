import React, { useState } from 'react';
import { useAuth } from './AuthContext';
import { LeafIcon } from './components/Icons';

interface SignupPageProps {
    onSwitchToLogin: () => void;
}

const SignupPage: React.FC<SignupPageProps> = ({ onSwitchToLogin }) => {
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    const [confirmPassword, setConfirmPassword] = useState('');
    const [error, setError] = useState('');
    const [loading, setLoading] = useState(false);
    const { signup } = useAuth();

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();
        if (password !== confirmPassword) {
            return setError('Passwords do not match');
        }
        setError('');
        setLoading(true);
        try {
            await signup(email, password);
             // No need to redirect, App.tsx will handle it based on auth state
        } catch (err: any) {
             if (err.code === 'auth/email-already-in-use') {
                setError('This email is already registered.');
            } else if (err.code === 'auth/weak-password') {
                setError('Password should be at least 6 characters.');
            } else {
                setError('Failed to create an account. Please try again.');
            }
            console.error(err);
        }
        setLoading(false);
    };

    return (
        <div className="min-h-screen flex items-center justify-center bg-base-300 p-4">
            <div className="w-full max-w-md p-8 space-y-6 bg-base-200 rounded-xl shadow-lg">
                <div className="text-center">
                    <div className="flex items-center justify-center space-x-3 mb-4">
                        <div className="bg-primary p-3 rounded-full inline-block">
                            <LeafIcon className="w-8 h-8 text-white"/>
                        </div>
                        <h1 className="text-3xl font-bold text-white tracking-wider">
                            Join GreenCampus+
                        </h1>
                    </div>
                    <p className="text-gray-400">Create an account to start your sustainability journey.</p>
                </div>
                <form onSubmit={handleSubmit} className="space-y-6">
                    {error && <p className="bg-danger/20 text-danger text-center p-3 rounded-md">{error}</p>}
                    <div>
                        <label htmlFor="email-signup" className="text-sm font-medium text-gray-300 block mb-2">Email Address</label>
                        <input
                            id="email-signup"
                            type="email"
                            value={email}
                            onChange={(e) => setEmail(e.target.value)}
                            required
                            className="w-full px-4 py-2 bg-base-300 border border-gray-700 rounded-md focus:ring-primary focus:border-primary text-white"
                        />
                    </div>
                    <div>
                        <label htmlFor="password-signup" className="text-sm font-medium text-gray-300 block mb-2">Password</label>
                        <input
                            id="password-signup"
                            type="password"
                            value={password}
                            onChange={(e) => setPassword(e.target.value)}
                            required
                            className="w-full px-4 py-2 bg-base-300 border border-gray-700 rounded-md focus:ring-primary focus:border-primary text-white"
                        />
                    </div>
                    <div>
                        <label htmlFor="confirm-password-signup" className="text-sm font-medium text-gray-300 block mb-2">Confirm Password</label>
                        <input
                            id="confirm-password-signup"
                            type="password"
                            value={confirmPassword}
                            onChange={(e) => setConfirmPassword(e.target.value)}
                            required
                            className="w-full px-4 py-2 bg-base-300 border border-gray-700 rounded-md focus:ring-primary focus:border-primary text-white"
                        />
                    </div>
                    <button type="submit" disabled={loading} className="w-full py-2 px-4 bg-primary text-white font-semibold rounded-md hover:bg-emerald-500 disabled:bg-gray-500 transition duration-300">
                        {loading ? 'Creating Account...' : 'Sign Up'}
                    </button>
                </form>
                <p className="text-center text-sm text-gray-400">
                    Already have an account?{' '}
                    <button onClick={onSwitchToLogin} className="font-medium text-primary hover:underline">
                        Log in
                    </button>
                </p>
            </div>
        </div>
    );
};

export default SignupPage;
