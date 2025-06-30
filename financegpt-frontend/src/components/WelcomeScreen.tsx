import { Button } from '@/components/ui/button';

interface WelcomeScreenProps {
  onStartChat: () => void;
  username?: string;
}

const WelcomeScreen = ({ onStartChat, username }: WelcomeScreenProps) => {
  return (
    <div className="min-h-screen flex flex-col items-center justify-center px-4">
      <div className="text-center space-y-8 max-w-2xl mx-auto animate-fade-in">
        <div className="space-y-4">
          <h1 className="text-6xl font-light text-gray-800 tracking-tight">
            Finance <span className="bg-gradient-to-r from-amber-500 to-yellow-600 bg-clip-text text-transparent font-medium">GPT</span>
          </h1>
          <p className="text-lg text-gray-500 font-medium">powered by jio finance</p>
          <div className="h-px w-32 bg-gradient-to-r from-amber-400 to-yellow-400 mx-auto opacity-60"></div>
        </div>
        
        <div className="space-y-6">
          <h2 className="text-3xl font-light text-gray-700">
            Hello, <span className="text-amber-600 font-medium">Finance Explorer!</span>
          </h2>
          <p className="text-lg text-gray-600 leading-relaxed">
            Your intelligent financial assistant is ready to help you with market analysis, 
            investment strategies, and financial planning.
          </p>
        </div>

        <div className="pt-8">
          <Button 
            onClick={onStartChat}
            className="bg-gradient-to-r from-amber-500 to-yellow-600 hover:from-amber-600 hover:to-yellow-700 
                     text-white px-8 py-3 text-lg rounded-xl shadow-lg hover:shadow-xl 
                     transform hover:scale-105 transition-all duration-200"
          >
            Start Conversation
          </Button>
        </div>
      </div>

      <div className="absolute bottom-8 left-1/2 transform -translate-x-1/2">
        <div className="flex space-x-2">
          <div className="w-2 h-2 bg-amber-400 rounded-full animate-pulse"></div>
          <div className="w-2 h-2 bg-yellow-400 rounded-full animate-pulse" style={{ animationDelay: '0.2s' }}></div>
          <div className="w-2 h-2 bg-orange-400 rounded-full animate-pulse" style={{ animationDelay: '0.4s' }}></div>
        </div>
      </div>
    </div>
  );
};

export default WelcomeScreen;
