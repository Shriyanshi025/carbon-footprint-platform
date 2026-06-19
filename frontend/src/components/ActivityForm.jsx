
const ActivityForm = ({
  formData,
  errorMessage,
  isCalculating,
  onInputChange,
  onCalculate,
}) => {
  const handleSubmit = (event) => {
    event.preventDefault();
    onCalculate();
  };

  const errorDescription = errorMessage
    ? 'form-error'
    : undefined;

  return (
    <div>
      <h2 className="text-2xl font-semibold text-gray-700 mb-4">
        Log Your Activities
      </h2>

      <form onSubmit={handleSubmit} noValidate>
        <div className="space-y-4">
          <fieldset>
            <legend className="text-lg font-medium text-gray-600 mb-2">
              Transport
            </legend>

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
              onChange={onInputChange}
              required
              aria-describedby={errorDescription}
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
              onChange={onInputChange}
              className="w-full p-2 border rounded"
            >
              <option value="car">Car</option>
              <option value="bus">Bus</option>
              <option value="train">Train</option>
              <option value="plane">Plane</option>
              <option value="motorcycle">Motorcycle</option>
            </select>
          </fieldset>

          <fieldset>
            <legend className="text-lg font-medium text-gray-600 mb-2">
              Food
            </legend>

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
              onChange={onInputChange}
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
              onChange={onInputChange}
              required
              aria-describedby={errorDescription}
              className="w-full p-2 border rounded"
            />
          </fieldset>

          <fieldset>
            <legend className="text-lg font-medium text-gray-600 mb-2">
              Electricity
            </legend>

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
              onChange={onInputChange}
              required
              aria-describedby={errorDescription}
              className="w-full p-2 border rounded"
            />
          </fieldset>

          <fieldset>
            <legend className="text-lg font-medium text-gray-600 mb-2">
              Shopping
            </legend>

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
              onChange={onInputChange}
              required
              aria-describedby={errorDescription}
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
              onChange={onInputChange}
              className="w-full p-2 border rounded"
            >
              <option value="electronics">Electronics</option>
              <option value="clothing">Clothing</option>
              <option value="groceries">Groceries</option>
              <option value="other">Other</option>
            </select>
          </fieldset>
        </div>

        {errorMessage && (
          <div
            id="form-error"
            role="alert"
            aria-live="assertive"
            className="mt-5 rounded-lg border border-red-300 bg-red-50 p-3 text-sm font-medium text-red-700"
          >
            {errorMessage}
          </div>
        )}

        <button
          type="submit"
          disabled={isCalculating}
          aria-disabled={isCalculating}
          className="w-full bg-blue-500 text-white font-bold py-2 px-4 rounded mt-6 hover:bg-blue-700 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-blue-700 disabled:cursor-not-allowed disabled:opacity-60"
        >
          {isCalculating
            ? 'Calculating...'
            : 'Calculate Footprint'}
        </button>
      </form>
    </div>
  );
};

export default ActivityForm;

