document.addEventListener('DOMContentLoaded', () => {
    const select = document.getElementById('category');
    const emojis = document.querySelectorAll('.emoji-box');

    select.addEventListener('change', () => {
        const selected = select.value;

        emojis.forEach(emoji => {
            if (emoji.dataset.category === selected) {
                emoji.classList.add('selected');    // light up the chosen emoji
            } else {
                emoji.classList.remove('selected'); // dim others
            }
        });
    });

    const emojisMap = {
        'Food': '🍔',
        'Social Life': '🎉',
        'Pets': '🐶',
        'Transport': '🚌',
        'Health': '💊',
        'Education': '📚',
        'Shopping': '🛍️',
        'Bills & Fees': '💳',
        'Gifts': '🎁',
        'Others': '❓'
    };

    let lastTransactions = [];

    const form = document.querySelector('form');
    const recentContainer = document.getElementById('recent-transactions');

    form.addEventListener('submit', async (event) => {
        event.preventDefault();
        const formData = new FormData(form);
        const amount = formData.get('amount');
        const category = formData.get('category');

        try {
            const response = await fetch(form.action, {
                method: form.method,
                body: formData,
            });

            if (response.ok) {
                lastTransactions.unshift({ category, amount });
                if (lastTransactions.length > 5) lastTransactions.pop();
                renderTransactions(recentContainer);
                form.reset();

                // Reset the emoji selection as well
                emojis.forEach(emoji => emoji.classList.remove('selected'));
            } else {
                alert("Failed to add expense");
            }
        } catch (error) {
            console.error("Error adding expense:", error);
            alert("Failed to add expense");
        }
    });

    function renderTransactions(container) {
        container.innerHTML = '';
        if (lastTransactions.length === 0) return;
        for (const tx of lastTransactions) {
            const box = document.createElement('div');
            box.className = 'transaction-card';
            Object.assign(box.style, {
                minWidth: '100px',
                height: '40px',
                background: "	#ffffffff",
                borderRadius: '8px',
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center',
                color : 'black',
                fontfamily : 'Segoe UI',
                fontWeight: '500',
                fontSize: '1rem',
                padding: '0 12px',
                boxShadow: '0 2px 8px rgba(0,0,0,0.05)'
            });
            box.textContent = `${emojisMap[tx.category] || ''} ${tx.category} ${tx.amount}`;
            container.appendChild(box);
        }
    }
});
