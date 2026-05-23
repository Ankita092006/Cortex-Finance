import axios from 'axios';
import MockAdapter from 'axios-mock-adapter';

// Create a new instance of axios for our API calls
export const api = axios.create({
  baseURL: 'https://api.cortexfinance.com/v1',
  timeout: 5000,
});

// Setup mock adapter
const mock = new MockAdapter(api, { delayResponse: 1500 }); // 1.5s delay to simulate network

// --- Mock Data ---

const dashboardData = {
  totalIncome: 85000,
  totalExpenses: 24532,
  healthStatus: "Good",
  savingsRate: 35,
  categoryBreakdown: [
    { name: 'Food', value: 35 },
    { name: 'Rent', value: 40 },
    { name: 'Travel', value: 10 },
    { name: 'Shopping', value: 15 },
  ]
};

const transactionsData = [
  { id: 1, type: 'Expense', category: 'Food', asset: 'Swiggy', amount: '-', value: '₹450.00', status: 'Completed', date: 'Today, 10:23 AM' },
  { id: 2, type: 'Expense', category: 'Rent', asset: 'Landlord Transfer', amount: '-', value: '₹15,000.00', status: 'Completed', date: 'Yesterday, 14:45 PM' },
  { id: 3, type: 'Income', category: 'Salary', asset: 'Tech Corp Ltd', amount: '+', value: '₹85,000.00', status: 'Completed', date: 'Oct 24, 09:12 AM' },
  { id: 4, type: 'Expense', category: 'Subscriptions', asset: 'Netflix', amount: '-', value: '₹649.00', status: 'Completed', date: 'Oct 23, 11:30 AM' },
];

const insightsData = {
  overspending: {
    category: "Food/Dining",
    percentage: 40,
    message: "You spent 40% more on Food/Dining this weekend compared to last month.",
    items: [
      { name: "Swiggy Delivery", amount: 1250, date: "Sat, 8:00 PM" },
      { name: "Starbucks", amount: 840, date: "Sun, 10:30 AM" },
      { name: "Zomato", amount: 950, date: "Sun, 9:00 PM" }
    ]
  },
  recurring: [
    { service: "Netflix", amount: 649 },
    { service: "Spotify", amount: 119 },
    { service: "Amazon Prime", amount: 299 }
  ],
  totalRecurring: 1067
};

// --- API Endpoints Mocking ---

// 1. POST /upload
mock.onPost('/upload').reply(200, {
  message: "Bank statement successfully uploaded and analyzed.",
  status: "success"
});

// 2. GET /dashboard
mock.onGet('/dashboard').reply(200, dashboardData);

// 3. GET /transactions
mock.onGet('/transactions').reply(200, { transactions: transactionsData });

// 4. GET /insights
mock.onGet('/insights').reply(200, insightsData);

// 5. POST /chat
mock.onPost('/chat').reply(config => {
  const { message } = JSON.parse(config.data);
  const q = message.toLowerCase();
  let aiResponse = "I can help you analyze your finances using AI. Try clicking one of the suggested prompts or ask me about your spending patterns!";
  
  if (q.includes('spending') || q.includes('expenses')) {
    aiResponse = "### 📊 Spending Analysis\nYou spent **₹24,532** last week.\n\nHere is your top spending breakdown:\n1. **Rent**: 40%\n2. **Food/Dining**: 35%\n3. **Shopping**: 15%\n\n> *AI Tip: To save more, consider reducing food delivery frequency.*";
  } else if (q.includes('subscriptions') || q.includes('recurring')) {
    aiResponse = "I found **3 active subscriptions** in your statement:\n\n| Service | Amount |\n| --- | --- |\n| Netflix | ₹649 |\n| Spotify | ₹119 |\n| Amazon Prime | ₹299 |\n\n**Total:** ₹1,067/month.";
  } else if (q.includes('unusual')) {
    aiResponse = "⚠️ **Alert:** There is one unusual transaction detected:\n\n- **Swiggy (₹450)** at 10:23 AM today. \n\nThis is **40% higher** than your average weekday food delivery order.";
  }
  
  return [200, { reply: aiResponse }];
});

export default api;
