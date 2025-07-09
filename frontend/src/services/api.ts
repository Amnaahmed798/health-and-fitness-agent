import axios from 'axios';

const API_BASE_URL = 'https://health-and-fitness-agent-production.up.railway.app';

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

export interface MealPlanResponse {
  mealPlan?: string;
  success: boolean;
  error?: string;
}

export interface WorkoutResponse {
  workout?: string;
  success: boolean;
  error?: string;
}

export interface ProgressResponse {
  message?: string;
  success: boolean;
  error?: string;
}

export interface GoalResponse {
  message?: string;
  success: boolean;
  error?: string;
}

export interface WorkoutLogData {
  date: string;
  workout_type: string;
  notes?: string;
}

export const healthCoachAPI = {
  // Send a message to the health coach
  async sendMessage(prompt: string, userInfo?: UserInfo): Promise<ChatResponse> {
    try {
      const response = await apiClient.post<ChatResponse>('/ask', {
        prompt,
        userInfo
      });
      
      return {
        response: typeof response.data === 'string' ? response.data : response.data.response || '',
        success: true
      };
    } catch (error: unknown) {
      const axiosError = error as { response?: { data?: { error?: string } }; message?: string };
      return {
        response: 'Sorry, I encountered an error. Please try again.',
        success: false,
        error: axiosError.response?.data?.error || axiosError.message
      };
    }
  },

  // Get user profile
  async getUserProfile(): Promise<UserInfo> {
    try {
      const response = await apiClient.get<UserInfo>('/profile');
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
  async getMealPlan(dietaryRestrictions?: string[]): Promise<MealPlanResponse | null> {
    try {
      const response = await apiClient.post<MealPlanResponse>('/meal-plan', {
        dietaryRestrictions
      });
      return response.data;
    } catch (error) {
      console.error('Error getting meal plan:', error);
      return null;
    }
  },

  // Get workout routine
  async getWorkoutRoutine(userInfo: UserInfo): Promise<WorkoutResponse | null> {
    try {
      const response = await apiClient.post<WorkoutResponse>('/workout', {
        userInfo
      });
      return response.data;
    } catch (error) {
      console.error('Error getting workout routine:', error);
      return null;
    }
  },

  // Track progress
  async trackProgress(data: {
    date: string;
    weight?: number;
    bodyFat?: number;
    chest?: number;
    waist?: number;
    notes?: string;
  }): Promise<ProgressResponse | null> {
    try {
      const response = await apiClient.post<ProgressResponse>('/progress', data);
      return response.data;
    } catch (error) {
      console.error('Error tracking progress:', error);
      return null;
    }
  },

  // Set goal
  async setGoal(goalData: {
    goalType: string;
    target: string;
    timeframe: string;
    userInfo?: UserInfo;
  }): Promise<GoalResponse | null> {
    try {
      const response = await apiClient.post<GoalResponse>('/goal', goalData);
      return response.data;
    } catch (error) {
      console.error('Error setting goal:', error);
      return null;
    }
  },

  // Log workout
  async logWorkout(data: WorkoutLogData): Promise<{ message: string; success: boolean; error?: string } | null> {
    try {
      const response = await apiClient.post<{ message: string; success: boolean; error?: string }>('/log-workout', data);
      return response.data;
    } catch (error) {
      console.error('Error logging workout:', error);
      return null;
    }
  }
};

export default healthCoachAPI; 