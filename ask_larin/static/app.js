function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.startsWith(name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

const csrftoken = getCookie('csrftoken');

const questions = document.getElementsByClassName('question');

for (const card of questions) {
    const likeButton = card.querySelector('.like');
    const dislikeButton = card.querySelector('.dislike');
    const rating = card.querySelector('.rating');
    const id = card.dataset.id;

    likeButton.addEventListener('click', async (event) => {
        const response = await fetch(`/question_like/${id}`, {
            method: 'POST',
            headers: {
                'X-CSRFToken': csrftoken,
                'Content-Type': 'application/json'
            },
            body: '{ "rating": 1 }'
        });

        if (response.ok) {
            const data = await response.json();
            rating.textContent = data.rating;
        }
    });

    dislikeButton.addEventListener('click', async (event) => {
        const response = await fetch(`/question_like/${id}`, {
            method: 'POST',
            headers: {
                'X-CSRFToken': csrftoken,
                'Content-Type': 'application/json'
            },
            body: '{ "rating": -1 }'
        });

        if (response.ok) {
            const data = await response.json();
            rating.textContent = data.rating;
        }
    });
}

const answers = document.getElementsByClassName('answer');
for (const card of answers) {
    const likeButton = card.querySelector('.like');
    const dislikeButton = card.querySelector('.dislike');
    const rating = card.querySelector('.rating');
    const id = card.dataset.id;
    const checkbox = card.querySelector('.find-checkbox');
    console.log(checkbox)
    console.log(likeButton)

    likeButton.addEventListener('click', async (event) => {
        const response = await fetch(`/answer_like/${id}`, {
            method: 'POST',
            headers: {
                'X-CSRFToken': csrftoken,
                'Content-Type': 'application/json'
            },
            body: '{ "rating": 1 }'
        });

        if (response.ok) {
            const data = await response.json();
            rating.textContent = data.rating;
        }
    });

    dislikeButton.addEventListener('click', async (event) => {
        const response = await fetch(`/answer_like/${id}`, {
            method: 'POST',
            headers: {
                'X-CSRFToken': csrftoken,
                'Content-Type': 'application/json'
            },
            body: '{ "rating": -1 }'
        });

        if (response.ok) {
            const data = await response.json();
            rating.textContent = data.rating;
        }
    });

    checkbox.addEventListener('click', async (event) => {
        const response = await fetch(`/answer_correct/${id}`, {
            method: 'POST',
            headers: {
                'X-CSRFToken': csrftoken,
                'Content-Type': 'application/json'
            }
        });
    
        if (response.ok) {
            return;
        }
    });

}