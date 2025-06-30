import { useState, useRef, useEffect } from 'react';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Send, Sparkles } from 'lucide-react';
import AnalyzingAnimation from './AnalyzingAnimation';
import { getApiUrl } from '@/config/api';
import { toast } from '@/components/ui/use-toast';
import ReactMarkdown from 'react-markdown';

interface Message {
  id: number;
  text: string;
  isUser: boolean;
  timestamp: Date;
  recommendations?: string[];
}

interface ChatWindowProps {
  username?: string;
}

const ChatWindow = ({ username }: ChatWindowProps) => {
  const [messages, setMessages] = useState<Message[]>([
    {
      id: 1,
      text: "Welcome to Finance GPT! Ask me anything about investments, products, or your financial goals.",
      isUser: false,
      timestamp: new Date(),
      recommendations: [
        "which all services do jio finance offer",
        "I am plaaning for some retiral benifits.",
        "i am looking for low risk investments. can you help me?"
      ]
    }
  ]);
  const [inputValue, setInputValue] = useState('');
  const [isAnalyzing, setIsAnalyzing] = useState(false);
  const messagesEndRef = useRef<HTMLDivElement>(null);
  const hasReceivedFirstChunk = useRef(false);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  // Helper to send a message (used for both input and recommendations)
  const sendMessage = async (query: string) => {
    if (!query.trim()) return;

    const newMessage: Message = {
      id: messages.length + 1,
      text: query,
      isUser: true,
      timestamp: new Date()
    };

    setMessages(prev => [...prev, newMessage]);
    setInputValue('');
    setIsAnalyzing(true);
    hasReceivedFirstChunk.current = false;

    // WebSocket streaming logic
    let ws: WebSocket | null = null;
    let aiMessageText = '';
    let aiMessageId = messages.length + 2;
    let aiRecommendations: string[] = [];
    try {
      // Always use ws://localhost:8000/ws/stream for chat
      const wsUrl = window.location.protocol === 'https:'
        ? 'wss://localhost:8000/ws/stream'
        : 'ws://localhost:8000/ws/stream';
      ws = new WebSocket(wsUrl);
      ws.onopen = () => {
        const token = localStorage.getItem('token');
        ws!.send(JSON.stringify({ query, token: token }));
      };
      ws.onmessage = (event) => {
        try {
          const data = event.data;
          console.log('WS received:', data);
          // If error JSON, show toast
          if (data.startsWith('{') && data.includes('error')) {
            const err = JSON.parse(data);
            toast({
              title: 'Error',
              description: err.error || 'Streaming error',
              variant: 'destructive',
            });
            setIsAnalyzing(false);
            ws?.close();
            return;
          }
          // If JSON with recommendations (end of stream)
          if (data.startsWith('{') && data.includes('recommendations')) {
            const obj = JSON.parse(data);
            aiRecommendations = obj.recommendations || [];
            setMessages(prev => {
              // Try to attach to the current streaming AI message
              let found = false;
              const updated = prev.map(m => {
                if (m.id === aiMessageId) {
                  found = true;
                  return { ...m, recommendations: aiRecommendations };
                }
                return m;
              });
              // If not found, attach to the last AI message
              if (!found) {
                for (let i = updated.length - 1; i >= 0; i--) {
                  if (!updated[i].isUser) {
                    updated[i] = { ...updated[i], recommendations: aiRecommendations };
                    break;
                  }
                }
              }
              return [...updated];
            });
            return;
          }
          // Hide analyzing animation as soon as the first word arrives (only once)
          if (!hasReceivedFirstChunk.current) {
            setIsAnalyzing(false);
            hasReceivedFirstChunk.current = true;
          }
          aiMessageText += data;
          setMessages(prev => {
            // If message already exists, update it
            const exists = prev.find(m => m.id === aiMessageId);
            if (exists) {
              return prev.map(m => m.id === aiMessageId ? { ...m, text: aiMessageText } : m);
            } else {
              return [...prev, {
                id: aiMessageId,
                text: aiMessageText,
                isUser: false,
                timestamp: new Date(),
                recommendations: []
              }];
            }
          });
        } catch (err) {
          // Ignore parse errors for non-JSON chunks
        }
      };
      ws.onerror = (event) => {
        toast({
          title: 'WebSocket Error',
          description: 'Failed to connect or stream response.',
          variant: 'destructive',
        });
        setIsAnalyzing(false);
      };
      ws.onclose = () => {
        setIsAnalyzing(false);
      };
    } catch (error) {
      console.error('Error:', error);
      toast({
        title: 'Error',
        description: error instanceof Error ? error.message : 'Failed to get response from the server. Please try again.',
        variant: 'destructive',
      });
      setIsAnalyzing(false);
    }
  };

  // Update handleSendMessage to use sendMessage
  const handleSendMessage = () => {
    sendMessage(inputValue);
  };

  // Handler for recommendation button click
  const handleRecommendationClick = (rec: string) => {
    sendMessage(rec);
  };

  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSendMessage();
    }
  };

  return (
    <div className="min-h-screen flex flex-col">
      {/* Header */}
      <header className="bg-white/80 backdrop-blur-md border-b border-gray-200 px-6 py-4">
        <div className="flex items-center space-x-3">
          <div className="w-8 h-8 bg-gradient-to-r from-amber-500 to-yellow-600 rounded-lg flex items-center justify-center">
            <Sparkles className="w-5 h-5 text-white" />
          </div>
          <div>
            <h1 className="text-xl font-semibold text-gray-800">Finance GPT</h1>
            <p className="text-sm text-gray-500">powered by jio finance</p>
          </div>
        </div>
      </header>

      {/* Messages */}
      <div className="flex-1 overflow-y-auto p-6">
        <div className="max-w-[70%] mx-auto space-y-6">
          {messages.map((message) => (
            <div
              key={message.id}
              className={`flex ${message.isUser ? 'justify-end' : 'justify-start'} animate-fade-in`}
            >
              <div className={`max-w-3xl ${message.isUser ? 'order-2' : 'order-1'}`}>
                <div
                  className={`px-6 py-4 rounded-2xl shadow-sm ${
                    message.isUser
                      ? 'bg-gradient-to-r from-amber-500 to-yellow-600 text-white ml-auto'
                      : 'bg-white border border-gray-200 text-gray-800'
                  }`}
                >
                  <p className="text-base leading-relaxed">
                    {message.isUser ? (
                      message.text
                    ) : (
                      <ReactMarkdown>{message.text}</ReactMarkdown>
                    )}
                  </p>
                </div>
                <div className={`mt-2 text-xs text-gray-500 ${message.isUser ? 'text-right' : 'text-left'}`}>
                  {message.timestamp.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
                </div>
                {/* Render recommendations for AI messages */}
                {!message.isUser && message.recommendations && message.recommendations.length > 0 && (
                  <div className="flex flex-wrap gap-2 mt-3">
                    {message.recommendations.map((rec, idx) => (
                      <Button
                        key={idx}
                        variant="outline"
                        className="rounded-full border-amber-400 text-amber-700 hover:bg-amber-50 px-4 py-1 text-sm shadow"
                        onClick={() => handleRecommendationClick(rec)}
                      >
                        {rec}
                      </Button>
                    ))}
                  </div>
                )}
              </div>
            </div>
          ))}

          {isAnalyzing && (
            <div className="flex justify-start animate-fade-in">
              <div className="max-w-3xl">
                <div className="bg-white border border-gray-200 px-6 py-4 rounded-2xl shadow-sm">
                  <AnalyzingAnimation />
                </div>
              </div>
            </div>
          )}
          
          <div ref={messagesEndRef} />
        </div>
      </div>

      {/* Input */}
      <div className="bg-white/80 backdrop-blur-md border-t border-gray-200 p-6">
        <div className="max-w-[70%] mx-auto">
          <div className="flex space-x-4">
            <div className="flex-1">
              <Input
                value={inputValue}
                onChange={(e) => setInputValue(e.target.value)}
                onKeyPress={handleKeyPress}
                placeholder="Ask Finance GPT anything..."
                className="w-full px-6 py-4 text-base border-gray-300 rounded-xl focus:ring-2 focus:ring-amber-500 focus:border-transparent"
                disabled={isAnalyzing}
              />
            </div>
            <Button
              onClick={handleSendMessage}
              disabled={!inputValue.trim() || isAnalyzing}
              className="bg-gradient-to-r from-amber-500 to-yellow-600 hover:from-amber-600 hover:to-yellow-700 
                       text-white px-6 py-4 rounded-xl shadow-lg hover:shadow-xl 
                       transform hover:scale-105 transition-all duration-200 disabled:opacity-50 disabled:cursor-not-allowed disabled:transform-none"
            >
              <Send className="w-5 h-5" />
            </Button>
          </div>
        </div>
      </div>
    </div>
  );
};

export default ChatWindow;
