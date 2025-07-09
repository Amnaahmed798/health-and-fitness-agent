import axios from 'axios';

const API_BASE_URL = 'http://localhost:8000';

// Create axios instance with default config
const apiClient = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Add request interceptor for logging
apiClient.interceptors.request.use(
  (config) => {
    console.log('Making request to:', config.url, config.data);
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Add response interceptor for error handling
apiClient.interceptors.response.use(
  (response) => {
    console.log('Response received:', response.data);
    return response;
  },
  (error) => {
    console.error('API Error:', error.response?.data || error.message);
    return Promise.reject(error);
  }
);

export interface UserInfo {
  age?: number;
  fitnessLevel?: string;
  healthGoals?: string;
  equipment?: string[];
}

export interface ChatRequest {
  prompt: string;
  userInfo?: UserInfo;
}

export interface ChatResponse {
  response: string;
  success: boolean;
  error?: string;
}

export const healthCoachAPI = {
  // Send a message to the health coach
  async sendMessage(prompt: string, userInfo?: UserInfo): Promise<ChatResponse> {
    try {
      const response = await apiClient.post('/ask', {
        prompt,
        userInfo
      });
      
      return {
        response: response.data.response || response.data,
        success: true
      };
    } catch (error: any) {
      return {
        response: 'Sorry, I encountered an error. Please try again.',
        success: false,
        error: error.response?.data?.error || error.message
      };
    }
  },

  // Get user profile
  async getUserProfile(): Promise<UserInfo> {
    try {
      const response = await apiClient.get('/profile');
      return response.data;
    } catch (error) {
      console.error('Error fetching user profile:', error);
      return {};
    }
  },

  // Update user profile
  async updateUserProfile(userInfo: UserInfo): Promise<boolean> {
    try {
      await apiClient.post('/profile', userInfo);
      return true;
    } catch (error) {
      console.error('Error updating user profile:', error);
      return false;
    }
  },

  // Get meal plan
  async getMealPlan(dietaryRestrictions?: string[]): Promise<any> {
    try {
      const response = await apiClient.post('/meal-plan', {
        dietaryRestrictions
      });
      return response.data;
    } catch (error) {
      console.error('Error getting meal plan:', error);
      return null;
    }
  },

  // Get workout routine
  async getWorkoutRoutine(userInfo: UserInfo): Promise<any> {
    try {
      const response = await apiClient.post('/workout', {
        userInfo
      });
      return response.data;
    } catch (error) {
      console.error('Error getting workout routine:', error);
      return null;
    }
  },

  // Track progress
  async trackProgress(data: any): Promise<any> {
    try {
      const response = await apiClient.post('/progress', data);
      return response.data;
    } catch (error) {
      console.error('Error tracking progress:', error);
      return null;
    }
  },

  // Set goal
  async setGoal(goalData: any): Promise<any> {
    try {
      const response = await apiClient.post('/goal', goalData);
      return response.data;
    } catch (error) {
      console.error('Error setting goal:', error);
      return null;
    }
  }
};

export default healthCoachAPI; 