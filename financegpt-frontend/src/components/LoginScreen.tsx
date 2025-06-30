import { useState } from 'react';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { LogIn, User } from 'lucide-react';
import { getApiUrl } from '@/config/api';

interface LoginScreenProps {
  onLogin: (username: string) => void;
  onSwitchToSignup: () => void;
}

const LoginScreen = ({ onLogin, onSwitchToSignup }: LoginScreenProps) => {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError(null);
    try {
      const res = await fetch(getApiUrl('LOGIN'), {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ email, password })
      });
      if (!res.ok) {
        const data = await res.json();
        setError(data.detail || 'Login failed');
        setLoading(false);
        return;
      }
      const data = await res.json();
      localStorage.setItem('token', data.access_token);
      setLoading(false);
      onLogin(data.name || email.split('@')[0]);
    } catch (err) {
      setError('Network error');
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen flex flex-col items-center justify-center px-4" style={{ background: 'linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%)' }}>
      <div className="w-full max-w-md space-y-8">
        <div className="text-center">
          <div className="flex justify-center mb-6">
            <div className="w-16 h-16 rounded-full flex items-center justify-center" style={{ background: 'linear-gradient(135deg, rgb(216, 170, 103) 0%, rgb(196, 150, 83) 100%)' }}>
              <LogIn className="w-8 h-8 text-white" />
            </div>
          </div>
          <h2 className="text-3xl font-light text-gray-800">Welcome Back</h2>
          <p className="mt-2 text-gray-600">Sign in to your <span className="font-semibold">Finance GPT</span> account</p>
          <p className="text-md text-gray-500 font-medium mt-1">powered by jio finance</p>
        </div>

        <form onSubmit={handleSubmit} className="bg-white rounded-2xl shadow-lg p-8 space-y-6">
          <div className="space-y-4">
            <div>
              <Label htmlFor="email" className="text-gray-700 font-medium">Email Address</Label>
              <Input
                id="email"
                type="email"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                placeholder="Enter your email"
                className="mt-1 h-12 rounded-xl border-gray-200 focus:border-[rgb(216,170,103)] focus:ring-[rgb(216,170,103)]"
                required
              />
            </div>
            <div>
              <Label htmlFor="password" className="text-gray-700 font-medium">Password</Label>
              <Input
                id="password"
                type="password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                placeholder="Enter your password"
                className="mt-1 h-12 rounded-xl border-gray-200 focus:border-[rgb(216,170,103)] focus:ring-[rgb(216,170,103)]"
                required
              />
            </div>
          </div>

          {error && <div className="text-red-500 text-center">{error}</div>}

          <Button
            type="submit"
            className="w-full h-12 text-white rounded-xl shadow-lg hover:shadow-xl transform hover:scale-105 transition-all duration-200"
            style={{ background: 'linear-gradient(135deg, rgb(216, 170, 103) 0%, rgb(196, 150, 83) 100%)' }}
            disabled={loading}
          >
            {loading ? 'Signing In...' : 'Sign In'}
          </Button>

          <div className="text-center">
            <p className="text-gray-600">
              Don't have an account?{' '}
              <button
                type="button"
                onClick={onSwitchToSignup}
                className="font-medium hover:underline"
                style={{ color: 'rgb(216, 170, 103)' }}
              >
                Sign up
              </button>
            </p>
          </div>
        </form>
      </div>
    </div>
  );
};

export default LoginScreen;
