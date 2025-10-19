import axios from 'axios';

const API_BASE_URL = 'https://api.example.com'; // Replace with your actual API base URL

export const fetchEventData = async (eventId) => {
    try {
        const response = await axios.get(`${API_BASE_URL}/events/${eventId}`);
        return response.data;
    } catch (error) {
        console.error('Error fetching event data:', error);
        throw error;
    }
};

export const fetchMarketData = async () => {
    try {
        const response = await axios.get(`${API_BASE_URL}/market-data`);
        return response.data;
    } catch (error) {
        console.error('Error fetching market data:', error);
        throw error;
    }
};

export const submitEventAssessment = async (eventAssessment) => {
    try {
        const response = await axios.post(`${API_BASE_URL}/assessments`, eventAssessment);
        return response.data;
    } catch (error) {
        console.error('Error submitting event assessment:', error);
        throw error;
    }
};