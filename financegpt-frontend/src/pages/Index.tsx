import { useState } from 'react';
import WelcomeScreen from '../components/WelcomeScreen';
import ChatWindow from '../components/ChatWindow';
import LoginScreen from '../components/LoginScreen';
import SignupScreen from '../components/SignupScreen';
import WelcomeAnimation from '../components/WelcomeAnimation';

type Screen = 'welcome' | 'login' | 'signup' | 'welcomeAnimation' | 'chat';

const Index = () => {
  const [currentScreen, setCurrentScreen] = useState<Screen>('welcome');
  const [username, setUsername] = useState<string>('');

  const handleStartChat = () => {
    setCurrentScreen('login');
  };

  const handleLogin = (name?: string) => {
    if (name) setUsername(name);
    setCurrentScreen('welcomeAnimation');
    setTimeout(() => setCurrentScreen('chat'), 2200);
  };

  const handleSignup = (name?: string) => {
    if (name) setUsername(name);
    setCurrentScreen('welcomeAnimation');
    setTimeout(() => setCurrentScreen('chat'), 2200);
  };

  const switchToLogin = () => {
    setCurrentScreen('login');
  };

  const switchToSignup = () => {
    setCurrentScreen('signup');
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-50 via-blue-50 to-indigo-100">
      {currentScreen === 'welcome' && (
        <WelcomeScreen onStartChat={handleStartChat} />
      )}
      {currentScreen === 'login' && (
        <LoginScreen onLogin={handleLogin} onSwitchToSignup={switchToSignup} />
      )}
      {currentScreen === 'signup' && (
        <SignupScreen onSignup={handleSignup} onSwitchToLogin={switchToLogin} />
      )}
      {currentScreen === 'welcomeAnimation' && (
        <WelcomeAnimation username={username} />
      )}
      {currentScreen === 'chat' && (
        <ChatWindow username={username} />
      )}
    </div>
  );
};

export default Index;
