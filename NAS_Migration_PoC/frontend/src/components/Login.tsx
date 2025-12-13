import React, { useState } from 'react';
import { FolderOpen } from 'lucide-react';

interface LoginProps {
    onLogin: (token: string) => void;
}

export const Login: React.FC<LoginProps> = ({ onLogin }) => {
    const [username, setUsername] = useState('admin');
    const [password, setPassword] = useState('secret');
    const [error, setError] = useState('');

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();
        setError('');

        const formData = new URLSearchParams();
        formData.append('username', username);
        formData.append('password', password);

        try {
            const response = await fetch('http://127.0.0.1:8000/token', {
                method: 'POST',
                headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
                body: formData,
            });

            if (!response.ok) throw new Error('Invalid credentials');

            const data = await response.json();
            onLogin(data.access_token);
        } catch (err) {
            setError('Invalid username or password');
        }
    };

    return (
        <div className="flex items-center justify-center min-h-screen bg-[#f5f5f7]">
            <div className="w-full max-w-sm p-8 bg-white rounded-2xl shadow-2xl border border-gray-200">
                <div className="flex justify-center mb-6">
                    <div className="p-4 bg-blue-500 rounded-2xl">
                        <FolderOpen className="w-8 h-8 text-white" />
                    </div>
                </div>
                <h2 className="mb-2 text-xl font-semibold text-center text-gray-900">Sign in to Files</h2>
                <p className="mb-6 text-sm text-center text-gray-500">Enter your credentials to continue</p>

                <form onSubmit={handleSubmit} className="space-y-4">
                    <div>
                        <label className="block mb-1.5 text-sm font-medium text-gray-700">Username</label>
                        <input
                            className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500/40 focus:border-blue-500/40 focus:outline-none text-sm"
                            type="text"
                            value={username}
                            onChange={(e) => setUsername(e.target.value)}
                        />
                    </div>
                    <div>
                        <label className="block mb-1.5 text-sm font-medium text-gray-700">Password</label>
                        <input
                            className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500/40 focus:border-blue-500/40 focus:outline-none text-sm"
                            type="password"
                            value={password}
                            onChange={(e) => setPassword(e.target.value)}
                        />
                    </div>

                    {error && (
                        <div className="p-3 bg-red-50 border border-red-200 rounded-lg">
                            <p className="text-xs text-center text-red-600">{error}</p>
                        </div>
                    )}

                    <button
                        type="submit"
                        className="w-full py-2.5 font-medium text-white transition bg-blue-500 rounded-lg hover:bg-blue-600 active:bg-blue-700 text-sm"
                    >
                        Sign In
                    </button>
                </form>

                <p className="mt-6 text-xs text-center text-gray-400">Default: admin / secret</p>
            </div>
        </div>
    );
};
