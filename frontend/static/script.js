// Frontend JS communicating with the backend API
// Since we'll use Nginx proxy or run on localhost:5000
const API_BASE = "http://localhost:5000/api";

document.addEventListener('DOMContentLoaded', () => {
    const counterDisplay = document.getElementById('counterValue');
    const decrementBtn = document.getElementById('decrementBtn');
    const incrementBtn = document.getElementById('incrementBtn');
    const resetBtn = document.getElementById('resetBtn');
    const saveBtn = document.getElementById('saveBtn');

    const updateUI = (data) => {
        counterDisplay.textContent = data.value;
        counterDisplay.classList.remove('pulse');
        void counterDisplay.offsetWidth; 
        counterDisplay.classList.add('pulse');
    };

    const fetchCounter = async () => {
        try {
            const response = await fetch(`${API_BASE}/counter`);
            const data = await response.json();
            updateUI(data);
        } catch (error) {
            console.error('Error:', error);
        }
    };

    const fetchAction = async (endpoint) => {
        try {
            const response = await fetch(`${API_BASE}/counter/${endpoint}`, { method: 'POST' });
            const data = await response.json();
            updateUI(data);
        } catch (error) {
            console.error('Error:', error);
        }
    };

    const save = async () => {
        saveBtn.textContent = 'SAVING...';
        saveBtn.disabled = true;
        try {
            const response = await fetch(`${API_BASE}/counter/save`, { method: 'POST' });
            const data = await response.json();
            if (data.success) {
                saveBtn.textContent = 'SAVED! ✓';
                saveBtn.classList.add('success');
                setTimeout(() => {
                    saveBtn.textContent = 'SAVE to DATABASE';
                    saveBtn.classList.remove('success');
                    saveBtn.disabled = false;
                }, 2000);
            } else {
                alert('Error: ' + data.message);
                saveBtn.textContent = 'SAVE to DATABASE';
                saveBtn.disabled = false;
            }
        } catch (error) {
            console.error('Error:', error);
            saveBtn.disabled = false;
        }
    };

    incrementBtn.addEventListener('click', () => fetchAction('increment'));
    decrementBtn.addEventListener('click', () => fetchAction('decrement'));
    resetBtn.addEventListener('click', () => fetchAction('reset'));
    saveBtn.addEventListener('click', save);

    fetchCounter();
});
