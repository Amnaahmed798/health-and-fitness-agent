'use client';

import { useState } from 'react';
import { Heart, MessageCircle, Target, TrendingUp, Users, Zap } from 'lucide-react';
import { healthCoachAPI, UserInfo } from '@/services/api';
import ReactMarkdown from 'react-markdown';

export default function Home() {
  const [userInfo, setUserInfo] = useState<UserInfo>({});
  const [isOnboarded, setIsOnboarded] = useState(false);
  const [messages, setMessages] = useState<Array<{type: 'user' | 'assistant', content: string}>>([]);
  const [currentMessage, setCurrentMessage] = useState('');
  const [isLoading, setIsLoading] = useState(false);

  const handleOnboarding = async (info: UserInfo) => {
    try {
      // Save user info to backend
      await healthCoachAPI.updateUserProfile(info);
      setUserInfo(info);
      setIsOnboarded(true);
      // Add welcome message
      setMessages([{
        type: 'assistant',
        content: `Welcome! I'm your personal health and wellness coach. I can help you with fitness, nutrition, mental health, and overall wellness. What would you like to work on today?`
      }]);
    } catch (error) {
      console.error('Error saving user profile:', error);
      // Still proceed with onboarding even if backend save fails
      setUserInfo(info);
      setIsOnboarded(true);
      setMessages([{
        type: 'assistant',
        content: `Welcome! I'm your personal health and wellness coach. I can help you with fitness, nutrition, mental health, and overall wellness. What would you like to work on today?`
      }]);
    }
  };

  const handleSendMessage = async () => {
    if (!currentMessage.trim()) return;

    const userMessage = { type: 'user' as const, content: currentMessage };
    setMessages(prev => [...prev, userMessage]);
    setCurrentMessage('');
    setIsLoading(true);

    try {
      // Send message to backend
      const response = await healthCoachAPI.sendMessage(currentMessage, userInfo);
      
      const assistantMessage = {
        type: 'assistant' as const,
        content: response.success ? response.response : 'Sorry, I encountered an error. Please try again.'
      };
      setMessages(prev => [...prev, assistantMessage]);
    } catch (error) {
      console.error('Error sending message:', error);
      const assistantMessage = {
        type: 'assistant' as const,
        content: 'Sorry, I encountered an error. Please try again.'
      };
      setMessages(prev => [...prev, assistantMessage]);
    } finally {
      setIsLoading(false);
    }
  };

  if (!isOnboarded) {
    return <OnboardingForm onSubmit={handleOnboarding} />;
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-green-50">
      <div className="container mx-auto px-4 py-8">
        {/* Header */}
        <header className="text-center mb-8">
          <h1 className="text-4xl font-bold text-gray-800 mb-2">
            🏃‍♀️ Health & Wellness Coach
          </h1>
          <p className="text-gray-600">
            Your personal AI-powered health and fitness companion
          </p>
        </header>

        <div className="grid grid-cols-1 lg:grid-cols-4 gap-6">
          {/* Sidebar */}
          <div className="lg:col-span-1">
            <div className="bg-white rounded-lg shadow-lg p-6 mb-6">
              <h3 className="text-lg font-semibold mb-4 flex items-center">
                <Users className="w-5 h-5 mr-2" />
                Your Profile
              </h3>
              <div className="space-y-2 text-sm">
                <p><span className="font-medium">Age:</span> {userInfo.age || 'Not specified'}</p>
                <p><span className="font-medium">Fitness Level:</span> {userInfo.fitnessLevel || 'Not specified'}</p>
                <p><span className="font-medium">Goals:</span> {userInfo.healthGoals || 'Not specified'}</p>
                <p><span className="font-medium">Equipment:</span> {userInfo.equipment?.join(', ') || 'Not specified'}</p>
              </div>
            </div>

            <div className="bg-white rounded-lg shadow-lg p-6">
              <h3 className="text-lg font-semibold mb-4 flex items-center">
                <Zap className="w-5 h-5 mr-2" />
                Quick Actions
              </h3>
              <div className="space-y-3">
                <button className="w-full text-left p-3 rounded-lg bg-blue-50 hover:bg-blue-100 transition-colors">
                  <div className="font-medium">Set New Goal</div>
                  <div className="text-sm text-gray-600">Create SMART fitness goals</div>
                </button>
                <button className="w-full text-left p-3 rounded-lg bg-green-50 hover:bg-green-100 transition-colors">
                  <div className="font-medium">Create Meal Plan</div>
                  <div className="text-sm text-gray-600">Get personalized nutrition</div>
                </button>
                <button className="w-full text-left p-3 rounded-lg bg-purple-50 hover:bg-purple-100 transition-colors">
                  <div className="font-medium">Track Progress</div>
                  <div className="text-sm text-gray-600">Log measurements & workouts</div>
                </button>
                <button className="w-full text-left p-3 rounded-lg bg-orange-50 hover:bg-orange-100 transition-colors">
                  <div className="font-medium">Get Workout</div>
                  <div className="text-sm text-gray-600">Generate exercise routine</div>
                </button>
              </div>
            </div>
          </div>

          {/* Main Chat Area */}
          <div className="lg:col-span-3">
            <div className="bg-white rounded-lg shadow-lg h-[600px] flex flex-col">
              {/* Chat Header */}
              <div className="p-4 border-b border-gray-200">
                <h2 className="text-lg font-semibold flex items-center">
                  <MessageCircle className="w-5 h-5 mr-2" />
                  Chat with Your Health Coach
                </h2>
              </div>

              {/* Messages */}
              <div className="flex-1 overflow-y-auto p-4 space-y-4">
                {messages.map((message, index) => (
                  <div
                    key={index}
                    className={`flex ${message.type === 'user' ? 'justify-end' : 'justify-start'}`}
                  >
                    <div
                      className={`max-w-[70%] p-3 rounded-lg ${
                        message.type === 'user'
                          ? 'bg-blue-500 text-white'
                          : 'bg-gray-100 text-gray-800'
                      }`}
                    >
                      <FormattedMessage content={message.content} />
                    </div>
                  </div>
                ))}
                {isLoading && (
                  <div className="flex justify-start">
                    <div className="bg-gray-100 text-gray-800 p-3 rounded-lg">
                      <div className="flex space-x-1">
                        <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce"></div>
                        <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{animationDelay: '0.1s'}}></div>
                        <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{animationDelay: '0.2s'}}></div>
                      </div>
                    </div>
                  </div>
                )}
              </div>

              {/* Input */}
              <div className="p-4 border-t border-gray-200">
                <div className="flex space-x-2">
                  <input
                    type="text"
                    value={currentMessage}
                    onChange={(e) => setCurrentMessage(e.target.value)}
                    onKeyPress={(e) => e.key === 'Enter' && handleSendMessage()}
                    placeholder="Ask about fitness, nutrition, or wellness..."
                    className="flex-1 p-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                  />
                  <button
                    onClick={handleSendMessage}
                    disabled={!currentMessage.trim() || isLoading}
                    className="px-6 py-3 bg-blue-500 text-white rounded-lg hover:bg-blue-600 disabled:opacity-50 disabled:cursor-not-allowed"
                  >
                    Send
                  </button>
                </div>
              </div>
            </div>
          </div>
        </div>

        {/* Features Section */}
        <div className="mt-12">
          <h2 className="text-2xl font-bold text-center mb-8">Available Features</h2>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            <FeatureCard
              icon={<Target className="w-8 h-8" />}
              title="Goal Setting"
              description="Set and track SMART fitness goals with personalized recommendations"
            />
            <FeatureCard
              icon={<Heart className="w-8 h-8" />}
              title="Nutrition Planning"
              description="Get personalized meal plans based on your dietary preferences and goals"
            />
            <FeatureCard
              icon={<TrendingUp className="w-8 h-8" />}
              title="Progress Tracking"
              description="Monitor your fitness journey with detailed progress analytics"
            />
            <FeatureCard
              icon={<Zap className="w-8 h-8" />}
              title="Workout Generation"
              description="Receive customized workout routines based on your fitness level"
            />
            <FeatureCard
              icon={<Users className="w-8 h-8" />}
              title="Expert Support"
              description="Connect with specialized agents for injury support and nutrition advice"
            />
            <FeatureCard
              icon={<MessageCircle className="w-8 h-8" />}
              title="Human Escalation"
              description="Get connected to human support when needed"
            />
          </div>
        </div>
      </div>
    </div>
  );
}

function FormattedMessage({ content }: { content: string }) {
  return (
    <div className="prose prose-sm max-w-none">
      <ReactMarkdown
        components={{
          // Custom styling for different elements
          h1: ({ children }) => <h1 className="text-lg font-bold text-gray-800 mb-2">{children}</h1>,
          h2: ({ children }) => <h2 className="text-base font-semibold text-gray-700 mb-2">{children}</h2>,
          h3: ({ children }) => <h3 className="text-sm font-semibold text-gray-600 mb-1">{children}</h3>,
          p: ({ children }) => <p className="mb-2">{children}</p>,
          ul: ({ children }) => <ul className="list-disc list-inside mb-2 space-y-1">{children}</ul>,
          ol: ({ children }) => <ol className="list-decimal list-inside mb-2 space-y-1">{children}</ol>,
          li: ({ children }) => <li className="text-sm">{children}</li>,
          strong: ({ children }) => <strong className="font-semibold text-gray-800">{children}</strong>,
          em: ({ children }) => <em className="italic">{children}</em>,
        }}
      >
        {content}
      </ReactMarkdown>
    </div>
  );
}

function FeatureCard({ icon, title, description }: { icon: React.ReactNode, title: string, description: string }) {
  return (
    <div className="bg-white rounded-lg shadow-lg p-6 hover:shadow-xl transition-shadow">
      <div className="text-blue-500 mb-4">{icon}</div>
      <h3 className="text-lg font-semibold mb-2">{title}</h3>
      <p className="text-gray-600">{description}</p>
    </div>
  );
}

function OnboardingForm({ onSubmit }: { onSubmit: (info: UserInfo) => void }) {
  const [formData, setFormData] = useState({
    age: '',
    fitnessLevel: '',
    healthGoals: '',
    equipment: ''
  });

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    const info: UserInfo = {
      age: formData.age ? parseInt(formData.age) : undefined,
      fitnessLevel: formData.fitnessLevel || undefined,
      healthGoals: formData.healthGoals || undefined,
      equipment: formData.equipment ? [formData.equipment] : undefined
    };
    onSubmit(info);
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-green-50 flex items-center justify-center p-4">
      <div className="bg-white rounded-lg shadow-xl p-8 max-w-md w-full">
        <div className="text-center mb-8">
          <h1 className="text-3xl font-bold text-gray-800 mb-2">
            🏃‍♀️ Welcome to Your Health Coach
          </h1>
          <p className="text-gray-600">
            Let&apos;s get to know you better to provide personalized recommendations
          </p>
        </div>

        <form onSubmit={handleSubmit} className="space-y-6">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Age
            </label>
            <input
              type="number"
              value={formData.age}
              onChange={(e) => setFormData(prev => ({ ...prev, age: e.target.value }))}
              className="w-full p-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
              placeholder="Enter your age"
            />
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Fitness Level
            </label>
            <select
              value={formData.fitnessLevel}
              onChange={(e) => setFormData(prev => ({ ...prev, fitnessLevel: e.target.value }))}
              className="w-full p-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
            >
              <option value="">Select your fitness level</option>
              <option value="beginner">Beginner</option>
              <option value="intermediate">Intermediate</option>
              <option value="advanced">Advanced</option>
            </select>
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Health Goals
            </label>
            <input
              type="text"
              value={formData.healthGoals}
              onChange={(e) => setFormData(prev => ({ ...prev, healthGoals: e.target.value }))}
              className="w-full p-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
              placeholder="e.g., weight loss, muscle gain, general fitness"
            />
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Available Equipment
            </label>
            <select
              value={formData.equipment}
              onChange={(e) => setFormData(prev => ({ ...prev, equipment: e.target.value }))}
              className="w-full p-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
            >
              <option value="">Select your equipment</option>
              <option value="gym">Gym access</option>
              <option value="home">Home equipment</option>
              <option value="none">No equipment</option>
            </select>
          </div>

          <button
            type="submit"
            className="w-full bg-blue-500 text-white py-3 px-6 rounded-lg hover:bg-blue-600 transition-colors font-medium"
          >
            Start My Health Journey
          </button>
        </form>
      </div>
    </div>
  );
}
