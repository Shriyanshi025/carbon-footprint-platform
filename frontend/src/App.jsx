import React, { useState } from 'react';
import axios from 'axios';
import { Bar } from 'react-chartjs-2';
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  BarElement,
  Title,
  Tooltip,
  Legend,
} from 'chart.js';

ChartJS.register(
  CategoryScale,
  LinearScale,
  BarElement,
  Title,
  Tooltip,
  Legend
);

const App = () => {
  const [footprintData, setFootprintData] = useState(null);
  const [tips, setTips] = useState('');
  const [tipsSource, setTipsSource] = useState('');
  const [errorMessage, setErrorMessage] = useState('');
  const [isCalculating, setIsCalculating] = useState(false);
  const [formData, setFormData] = useState({
    transport: { distance: '', vehicle_type: 'car' },
    food: { food_type: 'red_meat', consumption: '' },
    electricity: { kwh: '' },
    shopping: { amount_spent: '', category: 'other' },
  });

  const handleInputChange = (e) => {
    const { name, value, type } = e.target;
    const section = e.target.dataset.section;

    setErrorMessage('');

    setFormData((prev) => ({
      ...prev,
      [section]: {
        ...prev[section],
        [name]:
          type === 'number'
            ? value === ''
              ? ''
              : Number(value)
            : value,
      },
    }));
  };

  const calculateFootprint = async () => {
    const values = [
      formData.transport.distance,
      formData.food.consumption,
      formData.electricity.kwh,
      formData.shopping.amount_spent,
    ];

    if (values.some((value) => value === '')) {
      setErrorMessage('Please fill in all activity fields before calculating.');

      setFootprintData(null);
      setTips('');
      setTipsSource('');

      return;
    }

    if (values.some((value) => value < 0)) {
      setErrorMessage(
        'Values cannot be negative. Please enter zero or a positive number.'
      );

      setFootprintData(null);
      setTips('');
      setTipsSource('');

      return;
    }

    setErrorMessage('');
    setIsCalculating(true);

    try {
      const res = await axios.post('/api/calculate', formData);

      setFootprintData(res.data);
      await fetchTips(res.data);
    } catch (error) {
      setFootprintData(null);
      setTips('');
      setTipsSource('');

      if (error.response?.status === 422) {
        setErrorMessage(
          'Some entered values are invalid or outside the allowed range.'
        );
      } else {
        setErrorMessage(
          'Unable to calculate your footprint right now. Please try again.'
        );
      }
    } finally {
      setIsCalculating(false);
    }
  };

  const fetchTips = async (data) => {
    try {
      const res = await axios.post('/api/tips', {
        footprint_data: data,
      });

      setTips(res.data.tips);
      setTipsSource(res.data.source || 'fallback');
    } catch (error) {
      console.error('Error fetching tips:', error);
      setTips('Personalized tips are temporarily unavailable.');
      setTipsSource('error');
    }
  };

  const chartData = {
    labels: Object.keys(footprintData?.breakdown || {}),
    datasets: [
      {
        label: 'Carbon Footprint (kg CO2e)',
        data: Object.values(footprintData?.breakdown || {}),
        backgroundColor: 'rgba(75, 192, 192, 0.6)',
      },
    ],
  };

  return (
    <div className="min-h-screen bg-gray-100 p-8">
      <div className="max-w-4xl mx-auto bg-white rounded-lg shadow-md p-8">
        <h1 className="text-4xl font-bold text-center text-gray-800 mb-8">
          Carbon Footprint Dashboard
        </h1>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
          {/* LEFT SIDE */}
          <div>
            <h2 className="text-2xl font-semibold text-gray-700 mb-4">
              Log Your Activities
            </h2>

            <div className="space-y-4">
              {/* Transport */}
              <div>
                <h3 className="text-lg font-medium text-gray-600 mb-2">
                  Transport
                </h3>

                <label
                  htmlFor="distance"
                  className="block text-sm font-medium text-gray-700 mb-1"
                >
                  Distance travelled (km)
                </label>

                <input
                  id="distance"
                  type="number"
                  min="0"
                  step="0.1"
                  name="distance"
                  data-section="transport"
                  value={formData.transport.distance}
                  placeholder="Example: 10"
                  onChange={handleInputChange}
                  required
                  aria-describedby={errorMessage ? 'form-error' : undefined}
                  className="w-full p-2 border rounded"
                />

                <label
                  htmlFor="vehicle-type"
                  className="block text-sm font-medium text-gray-700 mt-2 mb-1"
                >
                  Vehicle type
                </label>

                <select
                  id="vehicle-type"
                  name="vehicle_type"
                  data-section="transport"
                  value={formData.transport.vehicle_type}
                  onChange={handleInputChange}
                  className="w-full p-2 border rounded"
                >
                  <option value="car">Car</option>
                  <option value="bus">Bus</option>
                  <option value="train">Train</option>
                  <option value="plane">Plane</option>
                  <option value="motorcycle">Motorcycle</option>
                </select>
              </div>

              {/* Food */}
              <div>
                <h3 className="text-lg font-medium text-gray-600 mb-2">
                  Food
                </h3>

                <label
                  htmlFor="food-type"
                  className="block text-sm font-medium text-gray-700 mb-1"
                >
                  Food type
                </label>

                <select
                  id="food-type"
                  name="food_type"
                  data-section="food"
                  value={formData.food.food_type}
                  onChange={handleInputChange}
                  className="w-full p-2 border rounded"
                >
                  <option value="red_meat">Red Meat</option>
                  <option value="white_meat">White Meat</option>
                  <option value="fish">Fish</option>
                  <option value="dairy">Dairy</option>
                  <option value="vegan">Vegan</option>
                </select>

                <label
                  htmlFor="food-consumption"
                  className="block text-sm font-medium text-gray-700 mt-2 mb-1"
                >
                  Food consumption (kg)
                </label>

                <input
                  id="food-consumption"
                  type="number"
                  min="0"
                  step="0.1"
                  name="consumption"
                  data-section="food"
                  value={formData.food.consumption}
                  placeholder="Example: 1"
                  onChange={handleInputChange}
                  required
                  aria-describedby={errorMessage ? 'form-error' : undefined}
                  className="w-full p-2 border rounded"
                />
              </div>

              {/* Electricity */}
              <div>
                <h3 className="text-lg font-medium text-gray-600 mb-2">
                  Electricity
                </h3>

                <label
                  htmlFor="electricity"
                  className="block text-sm font-medium text-gray-700 mb-1"
                >
                  Electricity consumption (kWh)
                </label>

                <input
                  id="electricity"
                  type="number"
                  min="0"
                  step="0.1"
                  name="kwh"
                  data-section="electricity"
                  value={formData.electricity.kwh}
                  placeholder="Example: 5"
                  onChange={handleInputChange}
                  required
                  aria-describedby={errorMessage ? 'form-error' : undefined}
                  className="w-full p-2 border rounded"
                />
              </div>

              {/* Shopping */}
              <div>
                <h3 className="text-lg font-medium text-gray-600 mb-2">
                  Shopping
                </h3>

                <label
                  htmlFor="shopping-amount"
                  className="block text-sm font-medium text-gray-700 mb-1"
                >
                  Amount spent
                </label>

                <input
                  id="shopping-amount"
                  type="number"
                  min="0"
                  step="0.01"
                  name="amount_spent"
                  data-section="shopping"
                  value={formData.shopping.amount_spent}
                  placeholder="Example: 10"
                  onChange={handleInputChange}
                  required
                  aria-describedby={errorMessage ? 'form-error' : undefined}
                  className="w-full p-2 border rounded"
                />

                <label
                  htmlFor="shopping-category"
                  className="block text-sm font-medium text-gray-700 mt-2 mb-1"
                >
                  Shopping category
                </label>

                <select
                  id="shopping-category"
                  name="category"
                  data-section="shopping"
                  value={formData.shopping.category}
                  onChange={handleInputChange}
                  className="w-full p-2 border rounded"
                >
                  <option value="electronics">Electronics</option>
                  <option value="clothing">Clothing</option>
                  <option value="groceries">Groceries</option>
                  <option value="other">Other</option>
                </select>
              </div>
            </div>

            {errorMessage && (
              <div
                id="form-error"
                role="alert"
                aria-live="polite"
                className="mt-5 rounded-lg border border-red-300 bg-red-50 p-3 text-sm font-medium text-red-700"
              >
                {errorMessage}
              </div>
            )}

            <button
              type="button"
              onClick={calculateFootprint}
              disabled={isCalculating}
              className="w-full bg-blue-500 text-white font-bold py-2 px-4 rounded mt-6 hover:bg-blue-700 disabled:cursor-not-allowed disabled:opacity-60"
            >
              {isCalculating ? 'Calculating...' : 'Calculate Footprint'}
            </button>
          </div>

          {/* RIGHT SIDE */}
          <div>
            {footprintData && (
              <div className="bg-green-100 p-6 rounded-lg">
                <h2 className="text-2xl font-semibold text-gray-700 mb-4">
                  Your Carbon Score
                </h2>

                <p className="text-5xl font-bold text-green-700 text-center">
                  {footprintData.total_footprint.toFixed(2)}
                </p>

                <p className="text-lg text-gray-600 text-center">
                  kg CO2e
                </p>
              </div>
            )}

            {footprintData && (
              <div className="mt-8">
                <h2 className="text-2xl font-semibold text-gray-700 mb-4">
                  Footprint Breakdown
                </h2>

                <Bar data={chartData} />
              </div>
            )}

            {tips && (
              <div className="mt-8 bg-yellow-100 p-6 rounded-lg">
                <div className="flex items-center justify-between gap-3 mb-3">
                  <h2 className="text-2xl font-semibold text-gray-700">
                    Personalized Reduction Tips
                  </h2>

                  {tipsSource !== 'error' && (
                    <span className="text-xs font-semibold px-3 py-1 rounded-full bg-white text-gray-600">
                      {tipsSource === 'gemini'
                        ? 'Gemini AI'
                        : 'Smart Fallback'}
                    </span>
                  )}
                </div>

                <p className="text-sm text-gray-600 mb-4">
                  {tipsSource === 'gemini'
                    ? 'Personalized recommendations generated using Gemini AI.'
                    : tipsSource === 'fallback'
                      ? 'Reliable recommendations generated by the built-in sustainability engine.'
                      : 'The recommendation service is temporarily unavailable.'}
                </p>

                <div className="text-gray-800 whitespace-pre-wrap">
                  {tips}
                </div>
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
};

export default App;
