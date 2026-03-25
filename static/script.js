document.addEventListener('DOMContentLoaded', () => {
    const counterDisplay = document.getElementById('counterValue');
    const decrementBtn = document.getElementById('decrementBtn');
    const incrementBtn = document.getElementById('incrementBtn');
    const resetBtn = document.getElementById('resetBtn');
    const saveBtn = document.getElementById('saveBtn');

    const updateUI = (data) => {
        counterDisplay.textContent = data.value;
        
        // Add pulse effect when value changes
        counterDisplay.classList.remove('pulse');
        void counterDisplay.offsetWidth; 
        counterDisplay.classList.add('pulse');
    };

    const fetchCounter = async () => {
        try {
            const response = await fetch('/api/counter');
            const data = await response.json();
            updateUI(data);
        } catch (error) {
            console.error('Error fetching counter:', error);
        }
    };

    const increment = async () => {
        try {
            const response = await fetch('/api/counter/increment', { method: 'POST' });
            const data = await response.json();
            updateUI(data);
        } catch (error) {
            console.error('Error incrementing counter:', error);
        }
    };

    const decrement = async () => {
        try {
            const response = await fetch('/api/counter/decrement', { method: 'POST' });
            const data = await response.json();
            updateUI(data);
        } catch (error) {
            console.error('Error decrementing counter:', error);
        }
    };

    const reset = async () => {
        try {
            const response = await fetch('/api/counter/reset', { method: 'POST' });
            const data = await response.json();
            updateUI(data);
        } catch (error) {
            console.error('Error resetting counter:', error);
        }
    };

    const save = async () => {
        saveBtn.textContent = 'SAVING...';
        saveBtn.disabled = true;
        
        try {
            const response = await fetch('/api/counter/save', { method: 'POST' });
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
            console.error('Error saving counter:', error);
            saveBtn.textContent = 'SAVE to DATABASE';
            saveBtn.disabled = false;
        }
    };

    incrementBtn.addEventListener('click', increment);
    decrementBtn.addEventListener('click', decrement);
    resetBtn.addEventListener('click', reset);
    saveBtn.addEventListener('click', save);

    // Initial fetch
    fetchCounter();
});
