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
	switch (req.body.command) {
		case 'stiring':
			if (process.env.ESP32_IP) {
				console.log(`stiring ${req.body.blink}`)
				axios.post(process.env.ESP32_IP, `stiring ${req.body.blink}`).catch(err => console.log(err.errno))
			}
			break
		case 'autosampler':
			if (process.env.ESP32_IP) {
				console.log(`autosampler ${req.body.direction} ${req.body.travel}`)
				axios.post(process.env.ESP32_IP, `autosampler ${req.body.direction} ${req.body.travel}`).catch(err => console.log(err.errno))
			}
			break
		default:
			break
	}
	res.sendFile(path.join(process.cwd(), 'public', 'index.html'))
})

app.listen(configService.get('PORT', 3000))
