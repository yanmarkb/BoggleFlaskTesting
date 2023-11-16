class BoggleGame {
	/* make a new game at this DOM id */

	constructor(boardId, secs = 60) {
		this.secs = secs; // game length
		this.showTimer(); // show the timer on the page

		this.score = 0; // initialize the score to 0
		this.words = new Set(); // initialize an empty set to store words
		this.board = $("#" + boardId); // get the game board element using the boardId

		// every 1000 msec, "tick"
		this.timer = setInterval(this.tick.bind(this), 1000); // set up a timer to call the tick method every second

		$(".add-word", this.board).on("submit", this.handleSubmit.bind(this)); // add an event listener to the form to handle word submissions
	}

	/* show word in list of words */

	showWord(word) {
		$(".words", this.board).append($("<li>", { text: word })); // add the word to the list of words on the page
	}

	/* show score in html */

	showScore() {
		$(".score", this.board).text(this.score); // update the score on the page
	}

	/* show a status message */

	showMessage(msg, cls) {
		$(".msg", this.board).text(msg).removeClass().addClass(`msg ${cls}`); // update the status message on the page
	}

	/* handle submission of word: if unique and valid, score & show */

	async handleSubmit(evt) {
		evt.preventDefault(); // prevent the default form submission behavior
		const $word = $(".word", this.board); // get the word input element

		let word = $word.val(); // get the value of the word input
		if (!word) return; // if the word is empty, do nothing

		if (this.words.has(word)) {
			// if the word has already been submitted, show an error message
			this.showMessage(`Already found ${word}`, "err");
			return;
		}

		// check server for validity
		const resp = await axios.get("/check-word", { params: { word: word } }); // send a request to the server to check if the word is valid
		if (resp.data.result === "not-word") {
			// if the word is not valid, show an error message
			this.showMessage(`${word} is not a valid English word`, "err");
		} else if (resp.data.result === "not-on-board") {
			// if the word is not on the board, show an error message
			this.showMessage(`${word} is not a valid word on this board`, "err");
		} else {
			// if the word is valid, add it to the list of words and update the score
			this.showWord(word);
			this.score += word.length;
			this.showScore();
			this.words.add(word);
			this.showMessage(`Added: ${word}`, "ok");
		}

		$word.val("").focus(); // clear the word input and focus on it
	}

	/* Update timer in DOM */

	showTimer() {
		$(".timer", this.board).text(this.secs); // update the timer on the page
	}

	/* Tick: handle a second passing in game */

	async tick() {
		this.secs -= 1; // decrement the timer
		this.showTimer(); // update the timer on the page

		if (this.secs === 0) {
			// if the timer has run out, end the game
			clearInterval(this.timer);
			await this.scoreGame();
		}
	}

	/* end of game: score and update message. */

	async scoreGame() {
		$(".add-word", this.board).hide(); // hide the word input form
		const resp = await axios.post("/post-score", { score: this.score }); // send a request to the server to post the score
		if (resp.data.brokeRecord) {
			// if the score is a new record, show a success message
			this.showMessage(`New record: ${this.score}`, "ok");
		} else {
			// otherwise, show the final score
			this.showMessage(`Final score: ${this.score}`, "ok");
		}
	}
}
