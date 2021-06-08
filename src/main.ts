import express, { Request, Response } from 'express'
import dotenv from 'dotenv'
import path from 'path'
import axios from 'axios'
import configService from './services/config.service'

dotenv.config()

const app = express()

app.use(express.json())
app.use(express.urlencoded({ extended: true }))

app.get('/', (req: Request, res: Response) => {
	res.sendFile(path.join(process.cwd(), 'public', 'index.html'))
})

app.post('/esp32', (req: Request, res: Response) => {
	console.log(req.socket.remoteAddress)
	res.sendStatus(200)
})

app.post('/', async (req: Request, res: Response) => {
	if (!process.env.ESP32_IP) return
	const command = req.body.command
	if (command === 'stiring') {
		const data = `stiring ${req.body.blink}`
		console.log(data)
		axios.post(process.env.ESP32_IP, data).catch(err => console.log(err.errno))
	} else if (command === 'autosampler') {
		const data = `autosampler ${req.body.direction} ${req.body.travel}`
		console.log(data)
		axios.post(process.env.ESP32_IP, data).catch(err => console.log(err.errno))
	} else if (command === 'syringepump') {
		const data = `syringepump ${req.body.direction} ${req.body.travel}`
		console.log(data)
		axios.post(process.env.ESP32_IP, data).catch(err => console.log(err.errno))
	}
	res.sendFile(path.join(process.cwd(), 'public', 'index.html'))
})

app.listen(configService.get('PORT', 3000))
