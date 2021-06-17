const robot = require('robotjs')

robot.setMouseDelay(1)

const twoPI = Math.PI * 2.0
const screenSize = robot.getScreenSize()
const height = (screenSize.height / 2) - 10
const width = screenSize.width

for (let x = 0; x < width; x++) {
	const y = height * Math.sin((twoPI * x) / width) + height
	robot.moveMouse(x, y)
}
