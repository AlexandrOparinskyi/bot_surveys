let numQuestion = 2;

function addQuestion() {
    const questions = document.getElementById("question-container"); // Получаем доступ к элементу с классом "questions"
    const questionContainer = document.createElement("div")
    questionContainer.classList.add(`questions`)
    questionContainer.innerHTML += `<br><label for="question-${numQuestion}">Вопрос ${numQuestion}</label><input id="question-${numQuestion}" type="text"><br>
            <label for="answer-q${numQuestion}-1">Ответ 1</label>
            <input id="answer-q${numQuestion}-1" type="text"><input id="correct-q${numQuestion}-1" type="checkbox">
            <label for="answer-q${numQuestion}-2">Ответ 2</label>
            <input id="answer-q${numQuestion}-2" type="text"><input id="correct-q${numQuestion}-2" type="checkbox">
            <label for="answer-q${numQuestion}-3">Ответ 3</label>
            <input id="answer-q${numQuestion}-3" type="text"><input id="correct-q${numQuestion}-3" type="checkbox"><br>`
    questions.append(questionContainer)
    const deleteButton = document.createElement("button")
    deleteButton.textContent = "Удалить вопрос"
    deleteButton.addEventListener("click", event => {
        event.preventDefault()
        questionContainer.remove()
    })
    questionContainer.appendChild(deleteButton)
    numQuestion++; // Увеличиваем счетчик вопросов
}

const addQuestionButton = document.getElementById("add-question");
    addQuestionButton.addEventListener("click", function(event) {
        event.preventDefault(); // Предотвращаем отправку формы
        addQuestion();
    });

const pollForm = document.getElementById("poll-form")
pollForm.addEventListener("submit", async event => {
    event.preventDefault();
    await savePoll();
})



async function savePoll() {
    let numQ = 1
    let hasErrorIsCorrect = false;
    let hasErrorAnswerValue = false;
    const pollName = document.getElementById("poll-name").value;
    const pollDescription = document.getElementById("poll-descr").value;
    const pollIsActive = document.getElementById("poll-active").checked;
    const questions = document.querySelectorAll(".questions");
    const pollData = {
        title: pollName,
        description: pollDescription,
        is_active: pollIsActive,
        questions: []
    };

    questions.forEach(() => {
        const questionText = document.getElementById(`question-${numQ}`).value;
        const answers = []
        let answerCorrect = 0

        for (let i = 1; i <= 3; i++) {
            const answerText = document.getElementById(`answer-q${numQ}-${i}`).value;
            if (answerText.length === 0) {
                hasErrorAnswerValue = true;
            }
            const answerCorrect = document.getElementById(`correct-q${numQ}-${i}`).checked;
            answers.push({text: answerText, is_correct: answerCorrect});
        }

        answers.forEach(answer => {
            if (answer.is_correct) {
                answerCorrect++;
            }
        })

        if (answerCorrect !== 1) {
            alert(`У вопроса ${numQ} должен быть 1 правильный ответ`)
            hasErrorIsCorrect = true;
        }

        pollData.questions.push({text: questionText, answers: answers})
        numQ++;
    })

    if (pollName.length === 0) {
        alert("Введите название опроса");
        return
    }
    if (hasErrorIsCorrect) {
        return;
    }
    if (hasErrorAnswerValue) {
        alert("Не все ответы заполнены");
        return
    }
    console.log(pollData)

    try {
        const response = await fetch("/create_poll", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify(pollData)
        });

        if (!response.ok) {
            throw new Error("Error")
        }

        alert("Опрос создан!")
        pollForm.reset();

    } catch (error) {
        console.log(`Ошибка при выполнении запроса ${error}`)
        alert("Error")
    }

}