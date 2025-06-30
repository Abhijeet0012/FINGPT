import React from 'react';

interface WelcomeAnimationProps {
  username?: string;
}

const WelcomeAnimation: React.FC<WelcomeAnimationProps> = ({ username }) => {
  return (
    <div className="min-h-screen flex flex-col items-center justify-center bg-gradient-to-br from-slate-50 via-blue-50 to-indigo-100 animate-fade-in">
      <div className="flex flex-col items-center space-y-8">
        <div className="flex items-center space-x-4">
          <div className="w-20 h-20 rounded-full bg-gradient-to-r from-amber-500 to-yellow-600 flex items-center justify-center shadow-lg animate-bounce">
            <svg width="48" height="48" viewBox="0 0 48 48" fill="none" xmlns="http://www.w3.org/2000/svg">
              <circle cx="24" cy="24" r="24" fill="url(#paint0_linear)" />
              <text x="50%" y="55%" textAnchor="middle" fill="#fff" fontSize="20" fontWeight="bold" dy=".3em">GPT</text>
              <defs>
                <linearGradient id="paint0_linear" x1="0" y1="0" x2="48" y2="48" gradientUnits="userSpaceOnUse">
                  <stop stopColor="#fbbf24" />
                  <stop offset="1" stopColor="#f59e42" />
                </linearGradient>
              </defs>
            </svg>
          </div>
        </div>
        <h1 className="text-4xl font-bold text-gray-800 tracking-tight animate-fade-in">
          Welcome, <span className="bg-gradient-to-r from-amber-500 to-yellow-600 bg-clip-text text-transparent font-extrabold">{username || 'User'}</span>!
        </h1>
        <p className="text-lg text-gray-600 animate-fade-in">Finance GPT is ready to assist you.</p>
        <div className="flex space-x-2 pt-4">
          <div className="w-3 h-3 bg-amber-400 rounded-full animate-pulse"></div>
          <div className="w-3 h-3 bg-yellow-400 rounded-full animate-pulse" style={{ animationDelay: '0.2s' }}></div>
          <div className="w-3 h-3 bg-orange-400 rounded-full animate-pulse" style={{ animationDelay: '0.4s' }}></div>
        </div>
      </div>
    </div>
  );
};

export default WelcomeAnimation; 