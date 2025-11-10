import React, { useState } from 'react';
import { useAuth } from './AuthContext';
import { LeafIcon } from './components/Icons';

interface LoginPageProps {
    onSwitchToSignup: () => void;
}

const LoginPage: React.FC<LoginPageProps> = ({ onSwitchToSignup }) => {
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    const [error, setError] = useState('');
    const [loading, setLoading] = useState(false);
    const { login } = useAuth();

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();
        setError('');
        setLoading(true);
        try {
            await login(email, password);
            // No need to redirect, App.tsx will handle it based on auth state
        } catch (err: any) {
            setError('Failed to log in. Please check your credentials.');
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
                            GreenCampus+
                        </h1>
                    </div>
                    <p className="text-gray-400">Log in to monitor your campus environment.</p>
                </div>
                <form onSubmit={handleSubmit} className="space-y-6">
                    {error && <p className="bg-danger/20 text-danger text-center p-3 rounded-md">{error}</p>}
                    <div>
                        <label htmlFor="email" className="text-sm font-medium text-gray-300 block mb-2">Email Address</label>
                        <input
                            id="email"
                            type="email"
                            value={email}
                            onChange={(e) => setEmail(e.target.value)}
                            required
                            className="w-full px-4 py-2 bg-base-300 border border-gray-700 rounded-md focus:ring-primary focus:border-primary text-white"
                        />
                    </div>
                    <div>
                        <label htmlFor="password"className="text-sm font-medium text-gray-300 block mb-2">Password</label>
                        <input
                            id="password"
                            type="password"
                            value={password}
                            onChange={(e) => setPassword(e.target.value)}
                            required
                            className="w-full px-4 py-2 bg-base-300 border border-gray-700 rounded-md focus:ring-primary focus:border-primary text-white"
                        />
                    </div>
                    <button type="submit" disabled={loading} className="w-full py-2 px-4 bg-primary text-white font-semibold rounded-md hover:bg-emerald-500 disabled:bg-gray-500 transition duration-300">
                        {loading ? 'Logging In...' : 'Log In'}
                    </button>
                </form>
                <p className="text-center text-sm text-gray-400">
                    Don't have an account?{' '}
                    <button onClick={onSwitchToSignup} className="font-medium text-primary hover:underline">
                        Sign up
                    </button>
                </p>
            </div>
        </div>
    );
};

export default LoginPage;
