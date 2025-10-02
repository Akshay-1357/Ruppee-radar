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