
import React from 'react';
import { LeafIcon } from './Icons';
import { useAuth } from '../AuthContext';

const Header: React.FC = () => {
  const { user, logout } = useAuth();
  return (
    <header className="bg-base-200 shadow-md p-4 flex items-center justify-between">
      <div className="flex items-center space-x-3">
        <div className="bg-primary p-2 rounded-full">
            <LeafIcon className="w-6 h-6 text-white"/>
        </div>
        <h1 className="text-xl sm:text-2xl font-bold text-white tracking-wider">
          GreenCampus+
        </h1>
      </div>
       {user && (
        <div className="flex items-center space-x-4">
          <span className="text-sm text-gray-400 hidden sm:block">{user.email}</span>
          <button 
            onClick={logout}
            className="bg-danger text-white px-3 py-1.5 rounded-md text-sm font-semibold hover:bg-red-500 transition-colors"
          >
            Logout
          </button>
        </div>
      )}
    </header>
  );
};

export default Header;
