const robot = require('robotjs')
const readline = require('readline')

function askQuestion(query) {
	const rl = readline.createInterface({
		input: process.stdin,
		output: process.stdout,
	})

	return new Promise(resolve => rl.question(query, ans => {
		rl.close()
		resolve(ans)
	}))
}

async function x() {
	while (true) {
		const ans = await askQuestion('')
		const mouse = robot.getMousePos()
		console.log([mouse.x, mouse.y])
	}
}

console.log(robot.getScreenSize())
x()
