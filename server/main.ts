import express, { Request, Response } from 'express'
import dotenv from 'dotenv'
import path from 'path'
import axios from 'axios'
import configService from './services/config.service'

dotenv.config()

const app = express()

app.use(express.json())
app.use(express.urlencoded({ extended: true }))

app.get('/', (_req: Request, res: Response) => {
	res.sendFile(path.join(process.cwd(), 'public', 'index.html'))
})

app.get('/sequence', (_req: Request, res: Response) => {
	res.sendFile(path.join(process.cwd(), 'public', 'sequence', 'index.html'))
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
	} else if (command === 'valvecathode') {
		const data = `valvecathode ${req.body.duration}`
		console.log(data)
		axios.post(process.env.ESP32_IP, data).catch(err => console.log(err.errno))
	} else if (command === 'valveanode') {
		const data = `valveanode ${req.body.duration}`
		console.log(data)
		axios.post(process.env.ESP32_IP, data).catch(err => console.log(err.errno))
	} else if (command === 'peristalticpump') {
		const data = `peristalticpump ${req.body.duration}`
		console.log(data)
		axios.post(process.env.ESP32_IP, data).catch(err => console.log(err.errno))
	}
	res.sendFile(path.join(process.cwd(), 'public', 'index.html'))
})

app.post('/sequence', async (req: Request, res: Response) => {
	if (!process.env.ESP32_IP) return
	console.log('START SETUP')
	console.log('autosampler_zeroing')
	await axios.post(process.env.ESP32_IP, 'autosampler_zeroing')
	console.log('autosampler 0 128')
	await axios.post(process.env.ESP32_IP, 'autosampler 0 128')
	console.log('peristalticpump 7500')
	await axios.post(process.env.ESP32_IP, 'peristalticpump 7500')
	console.log('valvecathode 10000')
	await axios.post(process.env.ESP32_IP, 'valvecathode 10000')
	console.log('valveanode 10000')
	await axios.post(process.env.ESP32_IP, 'valveanode 10000')
	console.log('syringepump 0 12000')
	await axios.post(process.env.ESP32_IP, 'syringepump 0 12000')
	console.log('valvecathode 10000')
	await axios.post(process.env.ESP32_IP, 'valvecathode 10000')
	console.log('valveanode 10000')
	await axios.post(process.env.ESP32_IP, 'valveanode 10000')
	console.log('END SETUP')
	console.log('START EXPERIMENT')
	console.log('autosampler 1 128')
	await axios.post(process.env.ESP32_IP, 'autosampler 1 128')
	console.log('syringepump 0 8500')
	await axios.post(process.env.ESP32_IP, 'syringepump 0 8500')
	console.log('AUTOCLICKING')
	console.log()
	console.log(`stiring ${req.body.stiring}`)
	await axios.post(process.env.ESP32_IP, `stiring ${req.body.stiring}`)
	console.log('AUTOCLICKING')
	console.log('valvecathode 10000')
	await axios.post(process.env.ESP32_IP, 'valvecathode 10000')
	console.log('valveanode 10000')
	await axios.post(process.env.ESP32_IP, 'valveanode 10000')
	console.log('END EXPERIMENT')
	console.log('START CLEANING')
	console.log('autosampler 0 128')
	await axios.post(process.env.ESP32_IP, 'autosampler 0 128')
	console.log('peristalticpump 8250')
	await axios.post(process.env.ESP32_IP, 'peristalticpump 8250')
	console.log('stiring 10000')
	await axios.post(process.env.ESP32_IP, 'stiring 10000')
	console.log('valvecathode 10000')
	await axios.post(process.env.ESP32_IP, 'valvecathode 10000')
	console.log('valveanode 10000')
	await axios.post(process.env.ESP32_IP, 'valveanode 10000')
	console.log('END CLEANING')
	res.sendFile(path.join(process.cwd(), 'public', 'sequence', 'index.html'))
})

app.listen(configService.get('PORT', 3000))
