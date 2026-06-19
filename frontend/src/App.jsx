import { useEffect, useState } from 'react';
import ActivityForm from './components/ActivityForm';
import ResultsPanel from './components/ResultsPanel';
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  BarElement,
  Title,
  Tooltip,
  Legend,
} from 'chart.js';
import {
  calculateCarbonFootprint,
  fetchReductionTips,
  wakeBackend,
} from './services/api';

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

  const clearResults = () => {
    setFootprintData(null);
    setTips('');
    setTipsSource('');
  };

  useEffect(() => {
    void wakeBackend();
  }, []);

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

      clearResults();

      return;
    }

    if (values.some((value) => value < 0)) {
      setErrorMessage(
        'Values cannot be negative. Please enter zero or a positive number.'
      );

      clearResults();

      return;
    }

    setErrorMessage('');
    setIsCalculating(true);

    try {
      const calculationResult =
        await calculateCarbonFootprint(formData);

      setFootprintData(calculationResult);

      setTips('Preparing your personalized eco action plan...');
      setTipsSource('loading');

      void fetchTips(calculationResult);
    } catch (error) {
      clearResults();

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
      const tipsResult = await fetchReductionTips(data);

      setTips(tipsResult.tips);
      setTipsSource(tipsResult.source || 'fallback');
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
          <ActivityForm
            formData={formData}
            errorMessage={errorMessage}
            isCalculating={isCalculating}
            onInputChange={handleInputChange}
            onCalculate={calculateFootprint}
          />

          {/* RIGHT SIDE */}
          <ResultsPanel
            footprintData={footprintData}
            chartData={chartData}
            tips={tips}
            tipsSource={tipsSource}
          />
        </div>
      </div>
    </div>
  );
};

export default App;
