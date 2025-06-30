
const AnalyzingAnimation = () => {
  return (
    <div className="flex items-center space-x-2">
      <div className="flex space-x-1">
        <div className="w-2 h-2 bg-amber-500 rounded-full animate-pulse"></div>
        <div className="w-2 h-2 bg-yellow-500 rounded-full animate-pulse" style={{ animationDelay: '0.2s' }}></div>
        <div className="w-2 h-2 bg-orange-500 rounded-full animate-pulse" style={{ animationDelay: '0.4s' }}></div>
      </div>
      <span className="text-gray-600 text-sm">Analyzing your request...</span>
    </div>
  );
};

export default AnalyzingAnimation;
