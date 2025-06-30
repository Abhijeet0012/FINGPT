import { useState } from 'react';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { RadioGroup, RadioGroupItem } from '@/components/ui/radio-group';
import { Textarea } from '@/components/ui/textarea';
import { User } from 'lucide-react';
import { getApiUrl } from '@/config/api';

interface SignupScreenProps {
  onSignup: (name: string) => void;
  onSwitchToLogin: () => void;
}

const SignupScreen = ({ onSignup, onSwitchToLogin }: SignupScreenProps) => {
  const [formData, setFormData] = useState({
    email: '',
    password: '',
    name: '',
    age: '',
    income: '',
    employmentType: '',
    riskAppetite: '',
    financialGoals: '',
    creditScore: '',
    kycVerified: 'false'
  });
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError(null);
    try {
      const res = await fetch(getApiUrl('SIGNUP'), {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          email: formData.email,
          password: formData.password,
          name: formData.name,
          age: Number(formData.age),
          income: Number(formData.income),
          employment_type: formData.employmentType,
          risk_appetite: formData.riskAppetite,
          financial_goals: formData.financialGoals,
          credit_score: Number(formData.creditScore),
          kyc_verified: formData.kycVerified
        })
      });
      if (!res.ok) {
        const data = await res.json();
        setError(data.detail || 'Signup failed');
        setLoading(false);
        return;
      }
      const data = await res.json();
      localStorage.setItem('token', data.access_token);
      setLoading(false);
      onSignup(formData.name);
    } catch (err) {
      setError('Network error');
      setLoading(false);
    }
  };

  const handleInputChange = (field: string, value: string) => {
    setFormData(prev => ({ ...prev, [field]: value }));
  };

  return (
    <div className="min-h-screen py-8 px-4" style={{ background: 'linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%)' }}>
      <div className="max-w-2xl mx-auto">
        <div className="text-center mb-8">
          <div className="flex justify-center mb-6">
            <div className="w-16 h-16 rounded-full flex items-center justify-center" style={{ background: 'linear-gradient(135deg, rgb(216, 170, 103) 0%, rgb(196, 150, 83) 100%)' }}>
              <User className="w-8 h-8 text-white" />
            </div>
          </div>
          <h2 className="text-3xl font-light text-gray-800">Create Account</h2>
          <p className="mt-2 text-gray-600">Join <span className="font-semibold">Finance GPT</span> and start your financial journey</p>
          <p className="text-md text-gray-500 font-medium mt-1">powered by jio finance</p>
        </div>

        <form onSubmit={handleSubmit} className="bg-white rounded-2xl shadow-lg p-8 space-y-6">
          {/* Account Information */}
          <div className="space-y-4">
            <h3 className="text-lg font-medium text-gray-800 pb-2 border-b border-gray-200">Account Information</h3>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div>
                <Label htmlFor="email" className="text-gray-700 font-medium">Email Address</Label>
                <Input
                  id="email"
                  type="email"
                  value={formData.email}
                  onChange={(e) => handleInputChange('email', e.target.value)}
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
                  value={formData.password}
                  onChange={(e) => handleInputChange('password', e.target.value)}
                  placeholder="Create a password"
                  className="mt-1 h-12 rounded-xl border-gray-200 focus:border-[rgb(216,170,103)] focus:ring-[rgb(216,170,103)]"
                  required
                />
              </div>
            </div>
          </div>

          {/* Personal Information */}
          <div className="space-y-4">
            <h3 className="text-lg font-medium text-gray-800 pb-2 border-b border-gray-200">Personal Information</h3>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div>
                <Label htmlFor="name" className="text-gray-700 font-medium">Full Name</Label>
                <Input
                  id="name"
                  type="text"
                  value={formData.name}
                  onChange={(e) => handleInputChange('name', e.target.value)}
                  placeholder="Enter your full name"
                  className="mt-1 h-12 rounded-xl border-gray-200 focus:border-[rgb(216,170,103)] focus:ring-[rgb(216,170,103)]"
                  required
                />
              </div>
              <div>
                <Label htmlFor="age" className="text-gray-700 font-medium">Age</Label>
                <Input
                  id="age"
                  type="number"
                  value={formData.age}
                  onChange={(e) => handleInputChange('age', e.target.value)}
                  placeholder="Enter your age"
                  className="mt-1 h-12 rounded-xl border-gray-200 focus:border-[rgb(216,170,103)] focus:ring-[rgb(216,170,103)]"
                  required
                />
              </div>
            </div>
          </div>

          {/* Financial Information */}
          <div className="space-y-4">
            <h3 className="text-lg font-medium text-gray-800 pb-2 border-b border-gray-200">Financial Information</h3>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div>
                <Label htmlFor="income" className="text-gray-700 font-medium">Annual Income</Label>
                <Input
                  id="income"
                  type="number"
                  step="0.01"
                  value={formData.income}
                  onChange={(e) => handleInputChange('income', e.target.value)}
                  placeholder="Enter annual income"
                  className="mt-1 h-12 rounded-xl border-gray-200 focus:border-[rgb(216,170,103)] focus:ring-[rgb(216,170,103)]"
                  required
                />
              </div>
              <div>
                <Label htmlFor="creditScore" className="text-gray-700 font-medium">Credit Score</Label>
                <Input
                  id="creditScore"
                  type="number"
                  value={formData.creditScore}
                  onChange={(e) => handleInputChange('creditScore', e.target.value)}
                  placeholder="Enter credit score"
                  className="mt-1 h-12 rounded-xl border-gray-200 focus:border-[rgb(216,170,103)] focus:ring-[rgb(216,170,103)]"
                  required
                />
              </div>
            </div>

            <div>
              <Label className="text-gray-700 font-medium">Employment Type</Label>
              <RadioGroup
                value={formData.employmentType}
                onValueChange={(value) => handleInputChange('employmentType', value)}
                className="mt-2"
              >
                <div className="flex items-center space-x-2">
                  <RadioGroupItem value="full-time" id="full-time" />
                  <Label htmlFor="full-time">Full-time</Label>
                </div>
                <div className="flex items-center space-x-2">
                  <RadioGroupItem value="part-time" id="part-time" />
                  <Label htmlFor="part-time">Part-time</Label>
                </div>
                <div className="flex items-center space-x-2">
                  <RadioGroupItem value="self-employed" id="self-employed" />
                  <Label htmlFor="self-employed">Self-employed</Label>
                </div>
                <div className="flex items-center space-x-2">
                  <RadioGroupItem value="unemployed" id="unemployed" />
                  <Label htmlFor="unemployed">Unemployed</Label>
                </div>
              </RadioGroup>
            </div>

            <div>
              <Label className="text-gray-700 font-medium">Risk Appetite</Label>
              <RadioGroup
                value={formData.riskAppetite}
                onValueChange={(value) => handleInputChange('riskAppetite', value)}
                className="mt-2"
              >
                <div className="flex items-center space-x-2">
                  <RadioGroupItem value="conservative" id="conservative" />
                  <Label htmlFor="conservative">Conservative</Label>
                </div>
                <div className="flex items-center space-x-2">
                  <RadioGroupItem value="moderate" id="moderate" />
                  <Label htmlFor="moderate">Moderate</Label>
                </div>
                <div className="flex items-center space-x-2">
                  <RadioGroupItem value="aggressive" id="aggressive" />
                  <Label htmlFor="aggressive">Aggressive</Label>
                </div>
              </RadioGroup>
            </div>

            <div>
              <Label htmlFor="financialGoals" className="text-gray-700 font-medium">Financial Goals</Label>
              <Textarea
                id="financialGoals"
                value={formData.financialGoals}
                onChange={(e) => handleInputChange('financialGoals', e.target.value)}
                placeholder="Describe your financial goals..."
                className="mt-1 rounded-xl border-gray-200 focus:border-[rgb(216,170,103)] focus:ring-[rgb(216,170,103)]"
                rows={3}
                required
              />
            </div>
          </div>

          <Button
            type="submit"
            className="w-full h-12 text-white rounded-xl shadow-lg hover:shadow-xl transform hover:scale-105 transition-all duration-200"
            style={{ background: 'linear-gradient(135deg, rgb(216, 170, 103) 0%, rgb(196, 150, 83) 100%)' }}
          >
            Create Account
          </Button>

          <div className="text-center">
            <p className="text-gray-600">
              Already have an account?{' '}
              <button
                type="button"
                onClick={onSwitchToLogin}
                className="font-medium hover:underline"
                style={{ color: 'rgb(216, 170, 103)' }}
              >
                Sign in
              </button>
            </p>
          </div>
        </form>
      </div>
    </div>
  );
};

export default SignupScreen;
